<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getSchool, peerSchools, tagLabels } from '../data/schools'
import { ratiosOf } from '../data/ratios'
import { evalSchoolNames } from '../data/evalMapping.js'
import { useCollection } from '../composables/useCollection'
import SchoolCard from '../components/SchoolCard.vue'

const route = useRoute()
const school = computed(() => getSchool(route.params.id))

// 近 5 年复试线（retest.js 全量数据，懒加载）
const RETEST_OFFICIAL_URL = 'https://yz.chsi.com.cn/kyzx/zt/kyfs.shtml'
const RETEST_YEARS = [2021, 2022, 2023, 2024, 2025]
const retestYear = ref(2025)
const retestFilter = ref('')
const retestLines = ref(null)
const retestRows = computed(() => {
  if (!school.value || !retestLines.value) return []
  const rows = retestLines.value[school.value.id] || []
  const kw = retestFilter.value.trim()
  return kw ? rows.filter((r) => r.major.includes(kw)) : rows
})
const baiduUrl = computed(
  () => `https://www.baidu.com/s?wd=${encodeURIComponent((school.value?.name || '') + ' 复试分数线')}`
)

const { toggleFav, isFav, toggleCompare, isCompared } = useCollection()

const peers = computed(() => (school.value ? peerSchools(school.value, 3) : []))
const ratios = computed(() =>
  school.value ? ratiosOf(school.value.id).filter((r) => r.year === 2025) : []
)

const tagClass = {
  '985': 'badge-985',
  '211': 'badge-211',
  '双一流': 'badge-syl',
  '自划线': 'badge-zhu'
}

const totalA = computed(() => {
  if (!school.value) return 0
  const { ap, a, am } = school.value.evalA
  return ap + a + am
})

// 该校各一级学科评估等级（真实数据，懒加载）
const gradeOrder = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']
const schoolSubjects = ref(null)
onMounted(async () => {
  if (!school.value?.evalKnown) return
  const mod = await import('../data/eval4th.js')
  const evalName = evalSchoolNames[school.value.id]
  const subjects = mod.bySchool[evalName] || {}
  schoolSubjects.value = Object.entries(subjects)
    .map(([name, grade]) => ({ name, grade, rank: gradeOrder.indexOf(grade) }))
    .sort((a, b) => a.rank - b.rank || a.name.localeCompare(b.name, 'zh'))
})

// 复试线全量数据懒加载
onMounted(async () => {
  const mod = await import('../data/retest.js')
  retestLines.value = mod.retestLines
})

function onToggleCompare() {
  const r = toggleCompare(school.value.id)
  if (!r.ok) alert(r.reason)
}
</script>

<template>
  <div class="container section">
    <div v-if="school">
      <RouterLink to="/schools" class="back-link">← 返回院校库</RouterLink>

      <!-- 头部 -->
      <div class="detail-head card">
        <div class="head-left">
          <div class="head-name-row">
            <h1 class="school-name">{{ school.name }}</h1>
            <span class="badge badge-region">{{ school.region }} · {{ school.city }}</span>
            <span class="badge badge-type">{{ school.type }}类</span>
          </div>
          <div class="head-tags">
            <span
              v-for="tag in school.tags"
              :key="tag"
              class="badge"
              :class="tagClass[tag]"
            >
              {{ tagLabels[tag] }}
            </span>
          </div>
          <p class="school-intro">{{ school.intro }}</p>
        </div>
        <div class="head-actions">
          <button
            class="btn"
            :class="isFav(school.id) ? 'btn-fav-on' : 'btn-light'"
            @click="toggleFav(school.id)"
          >
            {{ isFav(school.id) ? '⭐ 已收藏' : '☆ 收藏' }}
          </button>
          <button
            class="btn"
            :class="isCompared(school.id) ? 'btn-cmp-on' : 'btn-light'"
            @click="onToggleCompare"
          >
            {{ isCompared(school.id) ? '⚖ 已加入对比' : '⚖ 加入对比' }}
          </button>
          <RouterLink v-if="ratios.length" to="/ratios" class="btn btn-primary">
            📊 查看报录比
          </RouterLink>
        </div>
      </div>

      <!-- 学科评估 -->
      <div class="detail-section">
        <h2 class="detail-title">学科评估（第四轮 · 完整数据）</h2>
        <div v-if="school.evalKnown" class="eval-grid">
          <div class="eval-card card">
            <span class="eval-grade" style="color: #dc2626">A+</span>
            <span class="eval-num">{{ school.evalA.ap }}</span>
            <span class="eval-desc">前 2% 顶尖学科</span>
          </div>
          <div class="eval-card card">
            <span class="eval-grade" style="color: #f59e0b">A</span>
            <span class="eval-num">{{ school.evalA.a }}</span>
            <span class="eval-desc">前 2%~5%</span>
          </div>
          <div class="eval-card card">
            <span class="eval-grade" style="color: #3b82f6">A-</span>
            <span class="eval-num">{{ school.evalA.am }}</span>
            <span class="eval-desc">前 5%~10%</span>
          </div>
          <div class="eval-card card">
            <span class="eval-grade" style="color: #10b981">B+</span>
            <span class="eval-num">{{ school.evalA.bp }}</span>
            <span class="eval-desc">前 10%~20%</span>
          </div>
          <div class="eval-card card">
            <span class="eval-grade" style="color: #10b981">B</span>
            <span class="eval-num">{{ school.evalA.b }}</span>
            <span class="eval-desc">前 20%~30%</span>
          </div>
          <div class="eval-card card">
            <span class="eval-grade" style="color: #10b981">B-</span>
            <span class="eval-num">{{ school.evalA.bm }}</span>
            <span class="eval-desc">前 30%~40%</span>
          </div>
          <div class="eval-card card">
            <span class="eval-grade" style="color: #64748b">C+</span>
            <span class="eval-num">{{ school.evalA.cp }}</span>
            <span class="eval-desc">前 40%~50%</span>
          </div>
          <div class="eval-card card">
            <span class="eval-grade" style="color: #64748b">C</span>
            <span class="eval-num">{{ school.evalA.c }}</span>
            <span class="eval-desc">前 50%~60%</span>
          </div>
          <div class="eval-card card">
            <span class="eval-grade" style="color: #64748b">C-</span>
            <span class="eval-num">{{ school.evalA.cm }}</span>
            <span class="eval-desc">前 60%~70%</span>
          </div>
        </div>
        <div v-else class="no-data card">
          <p>📚 该校未参加或未收录于第四轮学科评估</p>
          <p class="no-data-sub">（第四轮评估未覆盖部分新设立高校及个别合并统计口径）</p>
        </div>
        <p v-if="school.evalKnown" class="eval-note">
          数据来源：教育部学位与研究生教育发展中心第四轮学科评估（2017）官方公开结果，共 9 档（A+ 至 C-）
        </p>

        <!-- 该校各学科评估等级明细 -->
        <div v-if="schoolSubjects && schoolSubjects.length" class="subject-list card">
          <h3 class="subject-list-title">📋 {{ school.name }} 参评学科等级明细（{{ schoolSubjects.length }} 个）</h3>
          <div class="subject-chips">
            <RouterLink
              v-for="s in schoolSubjects"
              :key="s.name"
              :to="{ path: '/majors', query: { subject: s.name } }"
              class="subject-chip"
              :class="`grade-${s.grade.replace('+', 'p').replace('-', 'm')}`"
              :title="`查看「${s.name}」各校评估排名`"
            >
              <span class="subject-grade">{{ s.grade }}</span>
              <span class="subject-name">{{ s.name }}</span>
            </RouterLink>
          </div>
          <p class="subject-list-note">点击学科可跳转专业目录，查看该学科所有参评学校的评估排名</p>
        </div>
      </div>

      <!-- 复试线（近 5 年 · 全专业） -->
      <div class="detail-section">
        <h2 class="detail-title">近 5 年复试线（2021–2025 · 覆盖全部参评学科）</h2>
        <div v-if="retestLines && retestRows.length" class="table-wrap">
          <div class="retest-controls">
            <div class="year-tabs">
              <button
                v-for="y in RETEST_YEARS"
                :key="y"
                class="year-tab"
                :class="{ 'year-tab-on': retestYear === y }"
                @click="retestYear = y"
              >
                {{ y }} 年
              </button>
            </div>
            <input
              v-model="retestFilter"
              class="retest-filter"
              type="text"
              placeholder="🔍 筛选专业，如「计算机」"
            />
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>专业方向</th>
                <th>学位类型</th>
                <th>{{ retestYear }} 年复试线（总分）</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="line in retestRows" :key="line.major">
                <td>{{ line.major }}</td>
                <td>{{ line.level }}</td>
                <td><span class="num">{{ line.scores[retestYear] }}</span> 分</td>
              </tr>
            </tbody>
          </table>
          <p v-if="retestFilter && !retestRows.length" class="no-data-sub" style="text-align: center">
            没有匹配「{{ retestFilter }}」的专业
          </p>
          <div class="official-links">
            <a :href="RETEST_OFFICIAL_URL" target="_blank" rel="noopener" class="btn btn-light">
              研招网复试分数线专题 ↗
            </a>
            <a :href="baiduUrl" target="_blank" rel="noopener" class="btn btn-light">
              🔍 搜索「{{ school.name }} 复试分数线」
            </a>
          </div>
        </div>
        <div v-else-if="retestLines" class="no-data card">
          <p>📋 该校复试线示例数据暂未收录</p>
          <p class="no-data-sub">请通过研招网专题页或该校研究生招生网查看历年复试分数线</p>
          <div class="official-links" style="justify-content: center">
            <a :href="RETEST_OFFICIAL_URL" target="_blank" rel="noopener" class="btn btn-light">
              研招网复试分数线专题 ↗
            </a>
            <a :href="baiduUrl" target="_blank" rel="noopener" class="btn btn-light">
              🔍 搜索「{{ school.name }} 复试分数线」
            </a>
          </div>
        </div>
        <div v-if="retestLines && retestRows.length" class="note" style="margin-top: 14px">
          ⚠️ 以上为示例数据：专业列表取自第四轮学科评估真实参评学科，分数为演示生成。
          研招网各校复试线由招生单位以公告形式发布、无结构化公开数据集，
          实际分数线请以 {{ school.name }} 研究生招生网发布的官方通知为准。
        </div>
      </div>

      <!-- 报录比 -->
      <div v-if="ratios.length" class="detail-section">
        <div class="detail-title-row">
          <h2 class="detail-title">2025 年热门专业报录比（示例数据）</h2>
          <RouterLink to="/ratios" class="btn btn-light">完整查询（2023-2025）→</RouterLink>
        </div>
        <div class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>专业</th>
                <th>报考人数</th>
                <th>录取人数</th>
                <th>报录比</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in ratios" :key="r.major">
                <td>{{ r.major }}</td>
                <td>{{ r.applicants }}</td>
                <td>{{ r.admitted }}</td>
                <td><span class="num">{{ r.ratio }}</span> : 1</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 同地区院校 -->
      <div v-if="peers.length" class="detail-section">
        <h2 class="detail-title">同地区院校推荐</h2>
        <div class="peer-grid">
          <SchoolCard v-for="p in peers" :key="p.id" :school="p" />
        </div>
      </div>
    </div>

    <div v-else class="empty card">
      <p class="empty-icon">🏫</p>
      <p>未找到该院校信息</p>
      <RouterLink to="/schools" class="btn btn-primary" style="margin-top: 12px">返回院校库</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.back-link {
  display: inline-block;
  color: var(--text-2);
  font-size: 14px;
  margin-bottom: 18px;
  transition: color 0.2s;
}

.back-link:hover {
  color: var(--primary);
}

.detail-head {
  padding: 28px;
  display: flex;
  gap: 24px;
  justify-content: space-between;
  flex-wrap: wrap;
}

.head-left {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
  min-width: 280px;
}

.head-name-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.school-name {
  font-size: 30px;
  font-weight: 800;
}

.head-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.school-intro {
  font-size: 15px;
  color: var(--text-2);
  line-height: 1.8;
  max-width: 720px;
}

.head-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
}

.btn-fav-on {
  background: #fef3c7;
  color: #b45309;
  border: 1px solid #fcd34d;
}

.btn-cmp-on {
  background: var(--primary-light);
  color: var(--primary);
  border: 1px solid #bfdbfe;
}

.detail-section {
  margin-top: 36px;
}

.detail-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 16px;
}

.detail-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
}

.detail-title-row .detail-title {
  margin-bottom: 0;
}

.eval-grid {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
  gap: 10px;
}

.eval-card {
  padding: 16px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.eval-grade {
  font-size: 14px;
  font-weight: 800;
}

.eval-num {
  font-size: 26px;
  font-weight: 800;
}

.eval-desc {
  font-size: 11px;
  color: var(--text-2);
}

.eval-note {
  margin-top: 10px;
  font-size: 12px;
  color: #9ca3af;
}

/* 学科等级明细 */
.subject-list {
  margin-top: 18px;
  padding: 22px;
}

.subject-list-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 14px;
}

.subject-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.subject-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: #fff;
  font-size: 13px;
  transition: all 0.15s ease;
}

.subject-chip:hover {
  border-color: var(--primary);
  box-shadow: 0 2px 8px rgba(29, 78, 216, 0.15);
  transform: translateY(-1px);
}

.subject-grade {
  font-weight: 800;
  font-size: 12px;
  padding: 1px 7px;
  border-radius: 5px;
  color: #fff;
}

.subject-name {
  font-weight: 600;
  color: var(--text);
}

.subject-list-note {
  margin-top: 12px;
  font-size: 12px;
  color: #9ca3af;
}

/* 等级颜色 */
.grade-Ap .subject-grade {
  background: #dc2626;
}

.grade-A .subject-grade {
  background: #f59e0b;
}

.grade-Am .subject-grade {
  background: #3b82f6;
}

.grade-Bp .subject-grade,
.grade-B .subject-grade,
.grade-Bm .subject-grade {
  background: #10b981;
}

.grade-Cp .subject-grade,
.grade-C .subject-grade,
.grade-Cm .subject-grade {
  background: #64748b;
}

.no-data {
  padding: 36px 20px;
  text-align: center;
  color: var(--text-2);
}

/* 复试线年份切换 */
.retest-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}

.year-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.retest-filter {
  padding: 8px 14px;
  border: 1px solid var(--border);
  border-radius: 999px;
  font-size: 13px;
  width: 220px;
}

.retest-filter:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.12);
}

.year-tab {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-2);
  background: #f1f5f9;
  border: 1px solid transparent;
  border-radius: 999px;
  padding: 6px 18px;
  transition: all 0.15s ease;
}

.year-tab:hover {
  color: var(--primary);
  border-color: #bfdbfe;
}

.year-tab-on {
  background: var(--primary);
  color: #fff;
}

.year-tab-on:hover {
  background: var(--primary-dark);
  color: #fff;
}

.official-links {
  display: flex;
  gap: 10px;
  margin-top: 14px;
  flex-wrap: wrap;
}

.no-data-sub {
  font-size: 13px;
  color: #9ca3af;
  margin-top: 4px;
}

.peer-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.empty {
  padding: 60px 20px;
  text-align: center;
  color: var(--text-2);
}

.empty-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

@media (max-width: 900px) {
  .eval-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .peer-grid {
    grid-template-columns: 1fr;
  }
}
</style>
