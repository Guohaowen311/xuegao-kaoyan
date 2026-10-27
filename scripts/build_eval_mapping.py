# -*- coding: utf-8 -*-
"""
生成 eval4th.js 数据到院校库 schools.js 的映射文件
输出：src/data/evalMapping.js
  { 院校库id: [A+, A, A-, B+, B, B-, C+, C, C- 数量] }
"""
import json
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

text = open(r'E:/web/src/data/eval4th.js', encoding='utf-8').read()

def extract(anchor):
    pos = text.index(anchor) + len(anchor)
    obj, _ = json.JSONDecoder().raw_decode(text[pos:])
    return obj

counts = extract('export const schoolGradeCounts = ')

# 院校库名称 -> 评估数据集中的合并名称
MERGE_MAP = {
    '中国石油大学（华东）': '中国石油大学',
    '中国地质大学（武汉）': '中国地质大学'
}

# 读取院校库学校名单
node_script = """
import('file:///E:/web/src/data/schools.js').then(m => {
  console.log(JSON.stringify(m.schools.map(x => ({ id: x.id, name: x.name }))))
})
"""
out = subprocess.run(['node', '-e', node_script], capture_output=True, text=True, encoding='utf-8')
schools_list = json.loads(out.stdout)

mapping = {}
name_resolve = {}  # 院校库 id -> 评估数据集中的学校名称
unmatched = []
for s in schools_list:
    name = s['name']
    if name in counts:
        mapping[s['id']] = counts[name]
        name_resolve[s['id']] = name
    elif name in MERGE_MAP:
        mapping[s['id']] = counts[MERGE_MAP[name]]
        name_resolve[s['id']] = MERGE_MAP[name]
    else:
        unmatched.append(name)

print('映射成功:', len(mapping), '/', len(schools_list))
print('未匹配（显示为未收录）:', unmatched)

with open(r'E:/web/src/data/evalMapping.js', 'w', encoding='utf-8') as f:
    f.write('/**\n')
    f.write(' * 院校库 id -> 第四轮学科评估 9 档数量 [A+, A, A-, B+, B, B-, C+, C, C-]\n')
    f.write(' * 以及 id -> 评估数据集中的学校名称（用于查学科明细）\n')
    f.write(' * 由 scripts/build_eval_mapping.py 生成，请勿手改\n')
    f.write(' */\n')
    f.write('export const gradeCounts = ')
    f.write(json.dumps(mapping, ensure_ascii=False, separators=(',', ':')))
    f.write('\n\n')
    f.write('export const evalSchoolNames = ')
    f.write(json.dumps(name_resolve, ensure_ascii=False, separators=(',', ':')))
    f.write('\n')

print('written: src/data/evalMapping.js')
