# -*- coding: utf-8 -*-
"""
生成 src/data/ratios.js：全部 137 所院校的报录比示例数据（2023-2025）
- 专业列表：该校第四轮评估排名靠前的学科（至多 6 个）+ 考研热门专业（至多 4 个），每校至多 10 个
- ⚠️ 示例数据：报录比按「院校层次 + 学科等级 + 热门度」锚定生成，仅用于功能演示；
    真实报录比需以各校研招网《报考人数统计》与拟录取名单核对，接入官方数据源后此文件可由远程 API 覆盖
"""
import hashlib
import json
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

GRADE_ORDER = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']

HOT = ['计算机科学与技术', '软件工程', '金融', '法学', '新闻传播学', '教育学',
       '会计', '电子信息', '应用经济学', '工商管理']

# 未参加第四轮评估院校的回退专业（按学校名）
FALLBACK_BY_NAME = {
    '中国矿业大学（北京）': ['矿业工程', '安全科学与工程', '计算机科学与技术'],
    '中国石油大学（北京）': ['石油与天然气工程', '化学工程与技术', '计算机科学与技术'],
    '中国地质大学（北京）': ['地质学', '环境科学与工程', '计算机科学与技术'],
    '上海科技大学': ['计算机科学与技术', '物理学', '化学', '生物学'],
    '南方科技大学': ['计算机科学与技术', '数学', '物理学', '材料科学与工程'],
    '西藏大学': ['生态学', '中国语言文学', '教育学']
}

# 锚定模型：ratio = (院校层次 + 学科等级 + 热门度) × 年份系数 × 抖动
GRADE_RATIO_BONUS = {'A+': 6.0, 'A': 4.5, 'A-': 3.0, 'B+': 1.5, 'B': 0.5,
                     'B-': 0.0, 'C+': -0.5, 'C': -1.0, 'C-': -1.5}

# 热门专业加成按院校层次分级（普通院校热门专业热度有限）
HOT_RATIO_BONUS = {3: 8.0, 2: 6.0, 1: 3.0}

# B 区院校（按所在城市判断，竞争热度整体低于 A 区同层次院校）
B_ZONE_CITIES = {'呼和浩特', '南宁', '海口', '贵阳', '昆明', '拉萨', '兰州', '西宁', '银川', '乌鲁木齐', '石河子'}

YEARS = [2023, 2024, 2025]
YEAR_FACTOR = {2023: 0.9, 2024: 0.95, 2025: 1.0}


def tier_base(tags, city=''):
    if '985' in tags:
        return 7.5 if city in B_ZONE_CITIES else 11.0  # B 区 985 按 211 档
    if '211' in tags or '双一流' in tags:
        return 4.0 if city in B_ZONE_CITIES else 7.5
    return 4.0


def jitter(seed, lo, hi):
    h = int(hashlib.md5(seed.encode()).hexdigest()[:6], 16)
    return lo + (h % (hi - lo + 1))


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

raw = {}
total_rows = 0
for s in schools_list:
    sid, name, tags = s['id'], s['name'], s['tags']
    eval_name = eval_names.get(sid)
    if eval_name and eval_name in by_school:
        subjects = by_school[eval_name]  # {学科: 等级}
        # 按等级排名取前 6
        ranked = sorted(subjects.items(), key=lambda kv: GRADE_ORDER.index(kv[1]) if kv[1] in GRADE_ORDER else 9)
        majors = [m for m, _ in ranked[:6]]
    else:
        majors = list(FALLBACK_BY_NAME.get(name, HOT[:3]))

    # 补充热门专业
    for m in HOT:
        if len(majors) >= 10:
            break
        if m not in majors:
            majors.append(m)

    rows = []
    for major in majors:
        grade = subjects.get(major) if subjects else None
        hot = major in HOT
        tier = 3 if '985' in tags else (2 if ('211' in tags or '双一流' in tags) else 1)
        if s['city'] in B_ZONE_CITIES:
            tier = max(1, tier - 1)  # B 区院校热度降一档
        base = tier_base(tags, s['city']) + GRADE_RATIO_BONUS.get(grade, 0) + (HOT_RATIO_BONUS[tier] if hot else 0)
        base = max(2.5, base)
        for y in YEARS:
            ratio = round(base * YEAR_FACTOR[y] * (1 + jitter(f'{sid}|{major}|{y}', 0, 15) / 100.0), 1)
            admitted = 30 + jitter(f'{sid}|{major}|{y}|adm', 0, 55)
            applicants = int(round(admitted * ratio))
            rows.append([major, y, applicants, admitted])
    raw[sid] = rows
    total_rows += len(rows)

print('院校覆盖:', len(raw), '/', len(schools_list))
print('数据行数:', total_rows)

with open(r'E:/web/src/data/ratios.js', 'w', encoding='utf-8') as f:
    f.write('/**\n')
    f.write(' * 报录比数据：全部院校 × 优势学科/热门专业 × 2023-2025\n')
    f.write(' * ⚠️ 示例数据，仅用于功能演示。真实报录比请以各校研招网公布的\n')
    f.write(' *   《报考人数统计》与拟录取名单核对计算；接入官方数据源后可实时更新。\n')
    f.write(' * 由 scripts/build_ratios_data.py 生成，请勿手改\n')
    f.write(' */\n\n')
    f.write('export const ratioYears = [2023, 2024, 2025]\n\n')
    f.write('// 各校报录比示例：[专业, 年份, 报考人数, 录取人数]\n')
    f.write('const RAW = ')
    f.write(json.dumps(raw, ensure_ascii=False, separators=(',', ':')))
    f.write('\n\n')
    f.write('/** 计算报录比（保留一位小数） */\n')
    f.write('export function toRatioEntries(rows) {\n')
    f.write('  return rows.map(([major, year, applicants, admitted]) => ({\n')
    f.write('    major,\n    year,\n    applicants,\n    admitted,\n')
    f.write('    ratio: Math.round((applicants / admitted) * 10) / 10\n')
    f.write('  }))\n')
    f.write('}\n\n')
    f.write('/** 获取某校报录比数据（可能为空数组） */\n')
    f.write('export function ratiosOf(schoolId) {\n')
    f.write('  const rows = RAW[schoolId]\n')
    f.write('  return rows ? toRatioEntries(rows) : []\n')
    f.write('}\n\n')
    f.write('/** 有报录比数据的院校 id 列表 */\n')
    f.write('export const schoolsWithRatios = Object.keys(RAW).filter((id) => RAW[id])\n')

import os
size = os.path.getsize(r'E:/web/src/data/ratios.js')
print(f'written: src/data/ratios.js ({size/1024:.0f} KB)')
