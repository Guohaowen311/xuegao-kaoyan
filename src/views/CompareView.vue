<script setup>
import { computed } from 'vue'
import { getSchool } from '../data/schools'
import { tagLabels } from '../data/schools'
import { ratiosOf } from '../data/ratios'
import { useCollection } from '../composables/useCollection'

const { compareIds, toggleCompare, clearCompare, MAX_COMPARE } = useCollection()

const schools = computed(() =>
  compareIds.value.map((id) => getSchool(id)).filter(Boolean)
)

const minRetest = computed(() =>
  schools.value.length
    ? Math.min(...schools.value.map((s) => (s.retest.length ? 1 : 0)))
    : 0
)

function maxRatio(school) {
  const list = ratiosOf(school.id).filter((r) => r.year === 2025)
  if (!list.length) return null
  return list.reduce((max, r) => (r.ratio > max.ratio ? r : max))
}
</script>

<template>
  <div class="container section">
    <div class="page-head">
      <h1 class="page-title">⚖️ 院校对比</h1>
      <p class="page-sub">
        已选 {{ schools.length }} / {{ MAX_COMPARE }} 所，在院校库卡片右上角点击 ⚖ 添加
      </p>
    </div>

    <div v-if="schools.length" class="compare-wrap">
      <div class="compare-head">
        <span class="compare-tip">横向滑动查看完整对比 →</span>
        <button class="btn btn-light" @click="clearCompare">清空对比</button>
      </div>

      <div class="compare-scroll">
        <table class="compare-table">
          <thead>
            <tr>
              <th class="col-label">对比项</th>
              <th v-for="s in schools" :key="s.id" class="col-school">
                <div class="cmp-name">{{ s.name }}</div>
                <button class="remove-btn" @click="toggleCompare(s.id)">✕ 移除</button>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="col-label">基本信息</td>
              <td v-for="s in schools" :key="s.id">
                <div class="cmp-line">{{ s.region }} · {{ s.city }}</div>
                <div class="cmp-line">{{ s.type }}类院校</div>
              </td>
            </tr>
            <tr>
              <td class="col-label">层次标签</td>
              <td v-for="s in schools" :key="s.id">
                <div class="cmp-tags">
                  <span
                    v-for="tag in s.tags"
                    :key="tag"
                    class="badge"
                    :class="`badge-${tag === '985' ? '985' : tag === '211' ? '211' : tag === '双一流' ? 'syl' : 'zhu'}`"
                  >
                    {{ tagLabels[tag] }}
                  </span>
                  <span v-if="!s.tags.length" class="cmp-none">—</span>
                </div>
              </td>
            </tr>
            <tr>
              <td class="col-label">A+ 学科数<br /><span class="th-sub">第四轮评估</span></td>
              <td v-for="s in schools" :key="s.id">
                <span v-if="s.evalKnown" class="cmp-strong" :class="{ 'cmp-hot': s.evalA.ap > 0 }">
                  {{ s.evalA.ap }}
                </span>
                <span v-else class="cmp-none">未收录</span>
              </td>
            </tr>
            <tr>
              <td class="col-label">A 类学科总数</td>
              <td v-for="s in schools" :key="s.id">
                <span v-if="s.evalKnown" class="cmp-strong">
                  {{ s.evalA.ap + s.evalA.a + s.evalA.am }}
                </span>
                <span v-else class="cmp-none">未收录</span>
              </td>
            </tr>
            <tr v-if="minRetest">
              <td class="col-label">复试线示例<br /><span class="th-sub">2025 最高分专业</span></td>
              <td v-for="s in schools" :key="s.id">
                <template v-if="s.retest.length">
                  <div class="cmp-line">
                    {{ s.retest[0].major }}
                    <span class="cmp-strong">{{ s.retest[0].score }}</span> 分
                  </div>
                </template>
                <span v-else class="cmp-none">未收录</span>
              </td>
            </tr>
            <tr>
              <td class="col-label">报录比示例<br /><span class="th-sub">2025 热门专业</span></td>
              <td v-for="s in schools" :key="s.id">
                <template v-if="maxRatio(s)">
                  <div class="cmp-line">{{ maxRatio(s).major }}</div>
                  <div class="cmp-strong">{{ maxRatio(s).ratio }} : 1</div>
                  <div class="cmp-sub">
                    报考 {{ maxRatio(s).applicants }} / 录取 {{ maxRatio(s).admitted }}
                  </div>
                </template>
                <span v-else class="cmp-none">未收录</span>
              </td>
            </tr>
            <tr>
              <td class="col-label">院校简介</td>
              <td v-for="s in schools" :key="s.id" class="cmp-intro">{{ s.intro }}</td>
            </tr>
            <tr>
              <td class="col-label">操作</td>
              <td v-for="s in schools" :key="s.id">
                <RouterLink :to="`/schools/${s.id}`" class="btn btn-light cmp-detail-btn">
                  查看详情 →
                </RouterLink>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="note" style="margin-top: 16px">
        ⚠️ 学科评估为第四轮结果（约数），复试线、报录比为示例数据，仅供参考。
        择校请综合历年数据、招生名额与自身实力，以官方发布为准。
      </div>
    </div>

    <div v-else class="empty card">
      <p class="empty-icon">⚖️</p>
      <p>还没有选择对比院校</p>
      <p class="empty-sub">在院校库卡片右上角点击 ⚖ 添加院校（最多 {{ MAX_COMPARE }} 所）</p>
      <RouterLink to="/schools" class="btn btn-primary" style="margin-top: 16px">去选择院校</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.page-head {
  margin-bottom: 24px;
}

.page-title {
  font-size: 30px;
  font-weight: 800;
}

.page-sub {
  color: var(--text-2);
  font-size: 14px;
  margin-top: 6px;
}

.compare-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.compare-tip {
  font-size: 13px;
  color: #9ca3af;
}

.compare-scroll {
  overflow-x: auto;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--white);
}

.compare-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
  min-width: 720px;
}

.compare-table th,
.compare-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  border-right: 1px solid #f1f5f9;
  text-align: left;
  vertical-align: top;
  min-width: 150px;
}

.compare-table th:last-child,
.compare-table td:last-child {
  border-right: none;
}

.compare-table thead th {
  background: #f1f5f9;
}

.compare-table .col-label {
  background: #f8fafc;
  font-weight: 600;
  color: var(--text-2);
  min-width: 110px;
  white-space: nowrap;
}

.cmp-name {
  font-size: 16px;
  font-weight: 800;
  margin-bottom: 6px;
}

.remove-btn {
  font-size: 12px;
  color: #dc2626;
  border: 1px solid #fecaca;
  background: #fef2f2;
  border-radius: 6px;
  padding: 3px 9px;
}

.remove-btn:hover {
  background: #dc2626;
  color: #fff;
  border-color: #dc2626;
}

.cmp-line {
  margin-bottom: 4px;
}

.cmp-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.cmp-strong {
  font-weight: 800;
  font-size: 16px;
  color: var(--primary);
}

.cmp-hot {
  color: #dc2626;
}

.cmp-sub {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 3px;
}

.cmp-none {
  color: #cbd5e1;
}

.cmp-intro {
  color: var(--text-2);
  line-height: 1.7;
  min-width: 200px;
}

.th-sub {
  font-size: 11px;
  font-weight: 400;
  color: #9ca3af;
}

.cmp-detail-btn {
  padding: 6px 14px;
  font-size: 13px;
}

.empty {
  padding: 70px 20px;
  text-align: center;
  color: var(--text-2);
}

.empty-icon {
  font-size: 44px;
  margin-bottom: 12px;
}

.empty-sub {
  font-size: 13px;
  color: #9ca3af;
  margin-top: 6px;
}
</style>
