<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getSchool } from '../data/schools'
import { ratiosOf, ratioYears, schoolsWithRatios } from '../data/ratios'

const route = useRoute()
const router = useRouter()

const ratioSchools = computed(() =>
  schoolsWithRatios.map((id) => getSchool(id)).filter(Boolean)
)

const selectedId = ref(route.query.school || '')
const activeYear = ref(Number(route.query.year) || 2025)

const selected = computed(() => (selectedId.value ? getSchool(selectedId.value) : null))

const entries = computed(() => {
  if (!selected.value) return []
  return ratiosOf(selected.value.id).filter((r) => r.year === activeYear.value)
})

watch([selectedId, activeYear], () => {
  router.replace({
    path: '/ratios',
    query: { school: selectedId.value, year: activeYear.value }
  })
})
</script>

<template>
  <div class="container section">
    <div class="page-head">
      <h1 class="page-title">📊 报录比查询</h1>
      <p class="page-sub">
        覆盖全部 137 所院校（2023-2025）· 报录比 = 报考人数 ÷ 录取人数，是衡量专业竞争激烈程度的重要指标
      </p>
    </div>

    <!-- 查询面板 -->
    <div class="query-panel card">
      <div class="query-row">
        <span class="query-label">选择院校</span>
        <select v-model="selectedId" class="school-select">
          <option value="" disabled>请选择院校</option>
          <option v-for="s in ratioSchools" :key="s.id" :value="s.id">
            {{ s.name }}（{{ s.region }}）
          </option>
        </select>
        <span class="query-label">年份</span>
        <div class="chip-group">
          <button
            v-for="y in ratioYears"
            :key="y"
            class="chip"
            :class="{ 'chip-on': activeYear === y }"
            @click="activeYear = y"
          >
            {{ y }} 年
          </button>
        </div>
      </div>
    </div>

    <!-- 结果 -->
    <div v-if="selected && entries.length" class="result-area">
      <div class="result-head">
        <h2 class="result-title">
          {{ selected.name }} · {{ activeYear }} 年报录比
          <span class="badge badge-region">{{ selected.region }} · {{ selected.city }}</span>
        </h2>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>专业</th>
              <th>报考人数</th>
              <th>录取人数</th>
              <th>报录比</th>
              <th>竞争程度</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in entries" :key="r.major">
              <td><strong>{{ r.major }}</strong></td>
              <td>{{ r.applicants }}</td>
              <td>{{ r.admitted }}</td>
              <td><span class="num">{{ r.ratio }}</span> : 1</td>
              <td>
                <span
                  class="badge"
                  :class="{
                    'badge-985': r.ratio >= 20,
                    'badge-syl': r.ratio >= 10 && r.ratio < 20,
                    'badge-type': r.ratio < 10
                  }"
                >
                  {{ r.ratio >= 20 ? '🔥 激烈' : r.ratio >= 10 ? '⚠️ 中等' : '✅ 相对缓和' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else-if="selected" class="empty card">
      <p class="empty-icon">📭</p>
      <p>该年份暂无{{ selected.name }}的报录比数据</p>
    </div>

    <!-- 解读说明 -->
    <div class="guide card">
      <h3 class="guide-title">💡 报录比怎么看？</h3>
      <ul class="guide-list">
        <li><strong>报录比 &lt; 5:1</strong> — 竞争相对缓和，过线进复试机会较大</li>
        <li><strong>报录比 5~10:1</strong> — 竞争中等，热门院校常见区间</li>
        <li><strong>报录比 10~20:1</strong> — 竞争激烈，多见于 985/211 热门专业</li>
        <li><strong>报录比 &gt; 20:1</strong> — 卷王专业，报考需做好充分心理准备</li>
      </ul>
      <p class="guide-note">
        报录比只反映报考热度，还要结合复试差额比、录取最低分、招生计划变化综合判断。
      </p>
    </div>

    <div class="note" style="margin-top: 16px">
      ⚠️ 本页报录比为示例数据（覆盖全部院校，专业取自各校优势学科与热门专业），仅用于功能演示。
      真实报录比请以各校研招网公布的《报考人数统计》与拟录取名单核对计算；接入官方数据源后可实时更新。
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

.query-panel {
  padding: 22px;
}

.query-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.query-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-2);
}

.school-select {
  flex: 1;
  min-width: 240px;
  max-width: 360px;
  padding: 10px 14px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--white);
  font-size: 15px;
}

.school-select:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.12);
}

.chip-group {
  display: flex;
  gap: 8px;
}

.chip {
  padding: 7px 18px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--white);
  font-size: 14px;
  color: var(--text-2);
  transition: all 0.15s ease;
}

.chip:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.chip-on {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
  font-weight: 600;
}

.chip-on:hover {
  color: #fff;
}

.result-area {
  margin-top: 28px;
}

.result-head {
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.result-title {
  font-size: 19px;
  font-weight: 700;
}

.empty {
  margin-top: 24px;
  padding: 50px 20px;
  text-align: center;
  color: var(--text-2);
}

.empty-icon {
  font-size: 38px;
  margin-bottom: 10px;
}

.guide {
  margin-top: 32px;
  padding: 24px;
}

.guide-title {
  font-size: 17px;
  font-weight: 700;
  margin-bottom: 12px;
}

.guide-list {
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 14px;
  color: var(--text-2);
}

.guide-note {
  margin-top: 12px;
  font-size: 13px;
  color: #9ca3af;
  line-height: 1.7;
}
</style>
