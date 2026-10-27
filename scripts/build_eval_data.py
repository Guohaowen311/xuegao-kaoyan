# -*- coding: utf-8 -*-
"""
将第四轮学科评估 CSV（教育部学位中心官方公开数据）
转换为前端数据模块 src/data/eval4th.js
"""
import csv
import io
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

RAW_PATH = r'E:/web/.tmp-eval/raw.csv'
OUT_PATH = r'E:/web/src/data/eval4th.js'

GRADES = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']

with open(RAW_PATH, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

records = []  # (code, name, grade, school)
for row in rows:
    code = (row.get('一级学科代码') or '').strip()
    name = (row.get('一级学科名称') or '').strip()
    grade = (row.get('评估结果') or '').strip()
    for i in range(1, 28):
        school = (row.get(f'学校名称{i}') or '').strip()
        if school:
            records.append((code, name, grade, school))

print('total records:', len(records))

# 按学科聚合
by_subject = {}
for code, name, grade, school in records:
    d = by_subject.setdefault(name, {})
    d.setdefault(grade, []).append(school)

# 按学校聚合
by_school = {}
for code, name, grade, school in records:
    by_school.setdefault(school, {})[name] = grade

# 每校 9 档数量
school_counts = {}
for code, name, grade, school in records:
    c = school_counts.setdefault(school, [0] * 9)
    c[GRADES.index(grade)] += 1

all_schools = sorted(by_school.keys())
print('schools:', len(all_schools), '| subjects:', len(by_subject))

# 导出
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write('/**\n')
    f.write(' * 教育部学位与研究生教育发展中心 · 第四轮学科评估（2017）完整数据\n')
    f.write(' * 由 scripts/build_eval_data.py 从官方公开 CSV 生成，请勿手改\n')
    f.write(' * 记录数：%d 条（学校 × 一级学科），覆盖 %d 所高校、%d 个一级学科\n' % (
        len(records), len(all_schools), len(by_subject)))
    f.write(' */\n\n')
    f.write('export const gradeOrder = %s\n\n' % json.dumps(GRADES, ensure_ascii=False))

    f.write('// 学科名称 -> { 等级: [学校列表] }\n')
    f.write('export const bySubject = ')
    f.write(json.dumps(by_subject, ensure_ascii=False, separators=(',', ':')))
    f.write('\n\n')

    f.write('// 学校名称 -> { 学科名称: 等级 }\n')
    f.write('export const bySchool = ')
    f.write(json.dumps(by_school, ensure_ascii=False, separators=(',', ':')))
    f.write('\n\n')

    f.write('// 学校名称 -> [A+, A, A-, B+, B, B-, C+, C, C- 数量]\n')
    f.write('export const schoolGradeCounts = ')
    f.write(json.dumps(school_counts, ensure_ascii=False, separators=(',', ':')))
    f.write('\n')

print('written:', OUT_PATH)

# 打印与院校库可能不一致的名称，供人工核对
import re
print('\n--- 需人工核对的学校名（含括号/简称等） ---')
for s in all_schools:
    if any(ch in s for ch in '（）()·'):
        print(repr(s))
