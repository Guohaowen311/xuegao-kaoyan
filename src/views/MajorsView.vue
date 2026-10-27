<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { majorCategories } from '../data/majors'
import { lines2025 } from '../data/scoreLines'
import { schools } from '../data/schools'

const route = useRoute()
const router = useRouter()

const expanded = ref(null)
const activeSubject = ref('')

const bySubject = ref(null)
const gradeOrder = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']

async function loadEval() {
  if (bySubject.value) return
  const mod = await import('../data/eval4th.js')
  bySubject.value = mod.bySubject
}

const subjectData = computed(() => {
  if (!bySubject.value || !activeSubject.value) return null
  return bySubject.value[activeSubject.value] || null
})

const subjectCategory = computed(() => {
  if (!activeSubject.value) return null
  return majorCategories.find((c) => c.firstLevels.includes(activeSubject.value)) || null
})

// 评估数据集中的学校名 -> 院校库 id
const nameToId = computed(() => {
  const map = {}
  for (const s of schools) map[s.name] = s.id
  return map
})

function schoolIdOf(name) {
  return nameToId.value[name] || null
}

async function openSubject(name) {
  activeSubject.value = name
  await loadEval()
  router.replace({ path: '/majors', query: name ? { subject: name } : {} })
}

function closeSubject() {
  activeSubject.value = ''
  router.replace('/majors')
}

// 支持从院校详情页 /majors?subject=xxx 直接跳入
onMounted(async () => {
  const q = route.query.subject
  if (q) {
    activeSubject.value = String(q)
    await loadEval()
  }
})

function lineOf(code) {
  return lines2025.find((l) => l.code === code)
}

function toggle(code) {
  expanded.value = expanded.value === code ? null : code
}

function gradeCount(data, grade) {
  return data[grade]?.length || 0
}

function totalSchools(data) {
  return Object.values(data).reduce((sum, arr) => sum + arr.length, 0)
}
</script>

<template>
  <div class="container section">
    <div class="page-head">
      <h1 class="page-title">专业目录</h1>
      <p class="page-sub">
        学术学位共 14 个学科门类 · 点击一级学科查看该学科所有参评学校的第四轮评估等级
      </p>
    </div>

    <!-- 学科排名面板 -->
    <div v-if="activeSubject" class="subject-panel card">
      <div class="panel-head">
        <div>
          <h2 class="panel-title">
            🏆 「{{ activeSubject }}」各校评估排名
            <span v-if="subjectCategory" class="panel-cat">
              {{ subjectCategory.name }}门类（{{ subjectCategory.code }}）
            </span>
          </h2>
          <p v-if="subjectData" class="panel-sub">
            共 {{ totalSchools(subjectData) }} 所高校参评 · 数据来源：教育部第四轮学科评估（2017）
          </p>
        </div>
        <button class="panel-close" @click="closeSubject">✕ 关闭</button>
      </div>

      <template v-if="subjectData">
        <div v-for="grade in gradeOrder" :key="grade" class="grade-section">
          <div class="grade-head">
            <span class="grade-badge" :class="`gb-${grade.replace('+', 'p').replace('-', 'm')}`">
              {{ grade }}
            </span>
            <span class="grade-count">{{ gradeCount(subjectData, grade) }} 所</span>
          </div>
          <div class="grade-schools">
            <RouterLink
              v-for="name in subjectData[grade]"
              v-show="schoolIdOf(name)"
              :key="name"
              :to="`/schools/${schoolIdOf(name)}`"
              class="school-chip"
            >
              {{ name }}
            </RouterLink>
            <span
              v-for="name in subjectData[grade]"
              v-show="!schoolIdOf(name)"
              :key="'x' + name"
              class="school-chip school-chip-muted"
            >
              {{ name }}
            </span>
          </div>
        </div>
      </template>
      <div v-else class="panel-empty">
        <p>📭 「{{ activeSubject }}」未参加第四轮学科评估</p>
        <p v-if="subjectCategory?.evalNote" class="panel-empty-sub">{{ subjectCategory.evalNote }}</p>
        <p v-else class="panel-empty-sub">
          军事学门类、2022 年新设交叉学科等未纳入第四轮评估范围
        </p>
      </div>

      <div class="panel-legend">
        <span class="lg-item"><span class="lg-dot" style="background: #dc2626"></span>A+ 前 2%</span>
        <span class="lg-item"><span class="lg-dot" style="background: #f59e0b"></span>A 前 2%~5%</span>
        <span class="lg-item"><span class="lg-dot" style="background: #3b82f6"></span>A- 前 5%~10%</span>
        <span class="lg-item"><span class="lg-dot" style="background: #10b981"></span>B 档 前 10%~40%</span>
        <span class="lg-item"><span class="lg-dot" style="background: #64748b"></span>C 档 前 40%~70%</span>
      </div>
    </div>

    <!-- 门类卡片 -->
    <div class="major-grid">
      <div
        v-for="m in majorCategories"
        :key="m.code"
        class="major-card card card-hover"
        :class="{ expanded: expanded === m.code }"
        @click="toggle(m.code)"
      >
        <div class="major-head">
          <span class="major-code">{{ m.code }}</span>
          <h2 class="major-name">{{ m.name }}</h2>
          <span v-if="m.popular" class="hot-tag">🔥 热门</span>
          <span class="line-2025">
            2025 国家线 <strong>{{ lineOf(m.code)?.a }}</strong> 分
          </span>
        </div>
        <p class="major-desc">{{ m.desc }}</p>
        <transition name="fade">
          <div v-if="expanded === m.code" class="major-levels" @click.stop>
            <span class="levels-label">一级学科（点击查看各校评估排名）：</span>
            <button
              v-for="lv in m.firstLevels"
              :key="lv"
              class="level-chip"
              :class="{ 'level-chip-on': activeSubject === lv }"
              @click="openSubject(lv)"
            >
              {{ lv }}
            </button>
          </div>
        </transition>
      </div>
    </div>

    <div class="note" style="margin-top: 32px">
      💡 专业学位（专硕）如金融[0251]、法律[0351]、电子信息[0854] 等另设类别目录，
      本页仅列学术学位门类。学科评估等级源自教育部学位与研究生教育发展中心第四轮学科评估
      （2017）官方公开结果，第五轮评估官方未完整公开，故未收录。
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

/* 学科排名面板 */
.subject-panel {
  padding: 24px;
  margin-bottom: 26px;
  border: 2px solid var(--primary);
  box-shadow: var(--shadow-lg);
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 18px;
}

.panel-title {
  font-size: 20px;
  font-weight: 800;
}

.panel-cat {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-2);
  background: #f1f5f9;
  border-radius: 999px;
  padding: 3px 10px;
  margin-left: 8px;
}

.panel-sub {
  font-size: 13px;
  color: var(--text-2);
  margin-top: 4px;
}

.panel-close {
  font-size: 13px;
  color: var(--text-2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 14px;
  flex-shrink: 0;
}

.panel-close:hover {
  color: #dc2626;
  border-color: #fecaca;
  background: #fef2f2;
}

.grade-section {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 10px 0;
  border-top: 1px dashed var(--border);
}

.grade-head {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  width: 74px;
  padding-top: 5px;
}

.grade-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 34px;
  height: 26px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 800;
  color: #fff;
}

.gb-Ap {
  background: #dc2626;
}

.gb-A {
  background: #f59e0b;
}

.gb-Am {
  background: #3b82f6;
}

.gb-Bp,
.gb-B,
.gb-Bm {
  background: #10b981;
}

.gb-Cp,
.gb-C,
.gb-Cm {
  background: #64748b;
}

.grade-count {
  font-size: 12px;
  color: #9ca3af;
}

.grade-schools {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  flex: 1;
}

.school-chip {
  display: inline-flex;
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: #fff;
  font-size: 13px;
  transition: all 0.15s ease;
}

.school-chip:hover {
  border-color: var(--primary);
  color: var(--primary);
  background: var(--primary-light);
}

.school-chip-muted {
  color: #9ca3af;
  border-style: dashed;
}

.panel-empty {
  padding: 30px 0;
  text-align: center;
  color: var(--text-2);
}

.panel-empty-sub {
  font-size: 13px;
  color: #9ca3af;
  margin-top: 6px;
}

.panel-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px solid var(--border);
}

.lg-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-2);
}

.lg-dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
}

/* 门类卡片 */
.major-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.major-card {
  padding: 22px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.major-head {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.major-code {
  font-size: 13px;
  font-weight: 700;
  color: var(--primary);
  background: var(--primary-light);
  border-radius: 6px;
  padding: 3px 9px;
}

.major-name {
  font-size: 19px;
  font-weight: 700;
}

.hot-tag {
  font-size: 12px;
  background: #fef2f2;
  color: #dc2626;
  border-radius: 999px;
  padding: 2px 10px;
  font-weight: 600;
}

.line-2025 {
  margin-left: auto;
  font-size: 13px;
  color: var(--text-2);
}

.line-2025 strong {
  color: var(--primary);
  font-size: 15px;
}

.major-desc {
  font-size: 13.5px;
  color: var(--text-2);
  line-height: 1.75;
}

.major-levels {
  border-top: 1px dashed var(--border);
  padding-top: 12px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.levels-label {
  font-size: 13px;
  color: var(--text-2);
  width: 100%;
}

.level-chip {
  font-size: 13px;
  background: #f1f5f9;
  color: #475569;
  border-radius: 6px;
  padding: 5px 12px;
  border: 1px solid transparent;
  transition: all 0.15s ease;
}

.level-chip:hover {
  background: var(--primary-light);
  color: var(--primary);
  border-color: #bfdbfe;
}

.level-chip-on {
  background: var(--primary);
  color: #fff;
}

.level-chip-on:hover {
  background: var(--primary-dark);
  color: #fff;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .major-grid {
    grid-template-columns: 1fr;
  }

  .grade-section {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
