# -*- coding: utf-8 -*-
"""
生成 src/data/retest.js：全部院校 × 全部参评学科 × 近 5 年（2021-2025）复试线
- 专业列表取自第四轮学科评估真实参评学科（eval4th.js bySchool），未参评院校用回退专业列表
- ⚠️ 分数为示例数据：按「2025 年门类国家线 + 院校层次 + 学科评估等级 + 热门度」锚定生成，
    研招网各校复试线由招生单位以公告形式发布、无结构化公开数据集，接入真实数据时替换本文件即可
"""
import hashlib
import json
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 2025 学硕 A 区国家线（总分），来自 src/data/scoreLines.js
LINES2025 = {
    '01': 321, '02': 323, '03': 323, '04': 341, '05': 351, '06': 336,
    '07': 274, '08': 260, '09': 245, '10': 293, '11': 260, '12': 333,
    '13': 351, '14': 266
}

HOT = {'计算机科学与技术', '软件工程', '电子科学与技术', '信息与通信工程',
       '控制科学与工程', '电气工程', '应用经济学', '新闻传播学', '教育学',
       '法学', '工商管理', '金融', '会计'}

# 未参加第四轮评估院校的回退专业（按学校名）
FALLBACK_BY_NAME = {
    '中国矿业大学（北京）': ['矿业工程', '安全科学与工程', '测绘科学与技术', '土木工程'],
    '中国石油大学（北京）': ['石油与天然气工程', '化学工程与技术', '地质资源与地质工程', '机械工程'],
    '中国地质大学（北京）': ['地质学', '地质资源与地质工程', '环境科学与工程', '土木工程'],
    '上海科技大学': ['物理学', '化学', '生物学', '计算机科学与技术', '材料科学与工程'],
    '南方科技大学': ['数学', '物理学', '化学', '材料科学与工程', '生物学', '计算机科学与技术'],
    '西藏大学': ['生态学', '中国语言文学', '民族学', '教育学']
}

# 锚定模型：score = 门类国家线 + (院校层次 + 学科等级 + 热门度) × 学科上浮系数
# 系数依据公开复试线的真实差距校准（工科计算机类头部校超国家线 100+，文史类超 30-60）
GRADE_BONUS = {'A+': 25, 'A': 18, 'A-': 12, 'B+': 6, 'B': 2, 'B-': 0,
               'C+': -4, 'C': -8, 'C-': -12}

TIER_BONUS = {3: 40, 2: 22, 1: 6}  # 985 / 211·双一流 / 普通
HOT_BONUS = 12

# B 区院校（按所在城市判断，复试线普遍贴近 B 区国家线）
B_ZONE_CITIES = {'呼和浩特', '南宁', '海口', '贵阳', '昆明', '拉萨', '兰州', '西宁', '银川', '乌鲁木齐', '石河子'}

SPREAD = {
    '计算机科学与技术': 1.6, '软件工程': 1.5, '信息与通信工程': 1.3, '电子科学与技术': 1.3,
    '电气工程': 1.25, '控制科学与工程': 1.2, '应用经济学': 1.2, '工商管理': 1.2,
    '新闻传播学': 1.1, '法学': 1.1, '教育学': 1.05, '心理学': 1.05,
    '中国语言文学': 0.85, '外国语言文学': 0.85, '哲学': 0.8, '考古学': 0.8,
    '中国史': 0.8, '世界史': 0.8, '艺术学理论': 0.8, '音乐与舞蹈学': 0.75,
    '美术学': 0.8, '设计学': 0.85, '戏剧与影视学': 0.85, '体育学': 0.9
}


def tier_of(tags):
    if '985' in tags:
        return 3
    if '211' in tags or '双一流' in tags:
        return 2
    return 1


def jitter(seed, lo, hi):
    h = int(hashlib.md5(seed.encode()).hexdigest()[:6], 16)
    return lo + h % (hi - lo + 1)


def round5(n):
    return max(0, int(round(n / 5.0) * 5))


# ---- 读取院校库 ----
node_script = """
import('file:///E:/web/src/data/schools.js').then(m => {
  console.log(JSON.stringify(m.schools.map(x => ({ id: x.id, name: x.name, tags: x.tags, city: x.city }))))
})
"""
out = subprocess.run(['node', '-e', node_script], capture_output=True, text=True, encoding='utf-8')
schools_list = json.loads(out.stdout)

# ---- 读取评估映射与参评学科 ----
node_script2 = """
import('file:///E:/web/src/data/evalMapping.js').then(async (em) => {
  const ev = await import('file:///E:/web/src/data/eval4th.js')
  console.log(JSON.stringify({ names: em.evalSchoolNames, bySchool: ev.bySchool }))
})
"""
out2 = subprocess.run(['node', '-e', node_script2], capture_output=True, text=True, encoding='utf-8')
eval_data = json.loads(out2.stdout)
eval_names = eval_data['names']
by_school = eval_data['bySchool']

# ---- 学科 -> 门类代码（解析 majors.js firstLevels）----
majors_js = open(r'E:/web/src/data/majors.js', encoding='utf-8').read()
subject_cat = {}
for m in re.finditer(r"code:\s*'(\d+)'.*?firstLevels:\s*\[(.*?)\]", majors_js, re.S):
    code, names = m.group(1), m.group(2)
    for name in re.findall(r"'([^']+)'", names):
        if name not in subject_cat:
            subject_cat[name] = code

YEARS = ['2021', '2022', '2023', '2024', '2025']

out_data = {}
total_majors = 0
unmatched_subjects = set()
for s in schools_list:
    sid, name, tags = s['id'], s['name'], s['tags']
    tier = tier_of(tags)
    eval_name = eval_names.get(sid)
    if eval_name and eval_name in by_school:
        subjects = by_school[eval_name]  # {学科: 等级}
    else:
        subjects = {m: 'B' for m in FALLBACK_BY_NAME.get(name, ['计算机科学与技术', '教育学', '应用经济学'])}

    rows = []
    for subject, grade in subjects.items():
        cat = subject_cat.get(subject)
        if cat is None and subject not in FALLBACK_BY_NAME.get(name, []):
            unmatched_subjects.add(subject)
        floor = LINES2025.get(cat, 270)
        hot = subject in HOT
        spread = SPREAD.get(subject, 1.0)
        raw = TIER_BONUS[tier] + GRADE_BONUS.get(grade, 0) + (HOT_BONUS if hot else 0) \
            + jitter(f'{sid}|{subject}|anchor', 0, 8)
        score2025 = round5(floor + raw * spread)
        score2025 = min(score2025, floor + 150)  # 上限：国家线 +150
        if s['city'] in B_ZONE_CITIES:
            score2025 = max(floor + 5, score2025 - 20)  # B 区院校整体下修
        step = 4 if hot else 2
        scores = {}
        for y in YEARS:
            if y == '2025':
                scores[y] = score2025
            else:
                back = (2025 - int(y)) * step + jitter(f'{sid}|{subject}|{y}', -2, 3)
                scores[y] = max(floor + 5, round5(score2025 - back))
        rows.append({'major': subject, 'level': '学硕', 'scores': scores})
    rows.sort(key=lambda r: -r['scores']['2025'])
    out_data[sid] = rows
    total_majors += len(rows)

print('院校覆盖:', len(out_data), '/', len(schools_list))
print('专业行数:', total_majors, '× 5 年 =', total_majors * 5, '个分数')

with open(r'E:/web/src/data/retest.js', 'w', encoding='utf-8') as f:
    f.write('/**\n')
    f.write(' * 近 5 年院校复试线（2021-2025）：全部院校 × 全部参评学科\n')
    f.write(' * ⚠️ 示例数据：专业列表取自第四轮学科评估真实参评学科，分数按「2025 门类国家线 +\n')
    f.write(' *    院校层次 + 学科等级 + 热门度」锚定生成。研招网各校复试线由招生单位以公告形式\n')
    f.write(' *    发布、无结构化公开数据集，接入真实数据源时直接替换本文件即可。\n')
    f.write(' * 由 scripts/build_retest_data.py 生成，请勿手改\n')
    f.write(' */\n')
    f.write('export const RETEST_YEARS = [2021, 2022, 2023, 2024, 2025]\n\n')
    f.write('// 院校id -> [{ major, level, scores: { 年份: 总分 } }]\n')
    f.write('export const retestLines = ')
    f.write(json.dumps(out_data, ensure_ascii=False, separators=(',', ':')))
    f.write('\n')
    f.write('export const RETEST_OFFICIAL_URL = "https://yz.chsi.com.cn/kyzx/zt/kyfs.shtml"\n')

import os
size = os.path.getsize(r'E:/web/src/data/retest.js')
print(f'written: src/data/retest.js ({size/1024:.0f} KB)')
