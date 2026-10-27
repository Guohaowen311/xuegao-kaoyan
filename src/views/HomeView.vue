<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { schools } from '../data/schools'
import { majorCategories } from '../data/majors'
import { stages, stageStatus } from '../data/timeline'
import { useCountdown } from '../composables/useCountdown'
import { useCollection } from '../composables/useCollection'
import SchoolCard from '../components/SchoolCard.vue'

const router = useRouter()
const keyword = ref('')

const { countdown, examYear } = useCountdown()
const { favIds, compareIds } = useCollection()

const hotSchools = computed(() =>
  [...schools]
    .filter((s) => s.evalKnown)
    .sort((a, b) => b.evalA.ap - a.evalA.ap)
    .slice(0, 8)
)

const totalA = computed(() =>
  schools.filter((s) => s.evalKnown).reduce((sum, s) => sum + s.evalA.ap, 0)
)

const steps = computed(() => stages.filter((_, i) => [2, 4, 7, 8].includes(i)))

const pad = (n) => String(n).padStart(2, '0')

function goSearch() {
  router.push({ path: '/schools', query: keyword.value.trim() ? { q: keyword.value.trim() } : {} })
}
</script>

<template>
  <div>
    <!-- Hero -->
    <section class="hero">
      <div class="container hero-inner">
        <p class="hero-badge">🍦 {{ examYear }} 考研备考进行中</p>
        <h1 class="hero-title">雪糕考研</h1>
        <p class="hero-sub">
          考研院校、专业目录、历年国家线、报录比、报考流程<br />一站式查询，让每一分努力都更有方向
        </p>

        <!-- 备考倒计时 -->
        <div class="countdown card">
          <span class="cd-label">距 {{ examYear }} 考研初试还有</span>
          <div class="cd-units">
            <div class="cd-unit">
              <span class="cd-num">{{ pad(countdown.days) }}</span>
              <span class="cd-text">天</span>
            </div>
            <div class="cd-unit">
              <span class="cd-num">{{ pad(countdown.hours) }}</span>
              <span class="cd-text">时</span>
            </div>
            <div class="cd-unit">
              <span class="cd-num">{{ pad(countdown.minutes) }}</span>
              <span class="cd-text">分</span>
            </div>
            <div class="cd-unit">
              <span class="cd-num">{{ pad(countdown.seconds) }}</span>
              <span class="cd-text">秒</span>
            </div>
          </div>
        </div>

        <form class="hero-search" @submit.prevent="goSearch">
          <input
            v-model="keyword"
            type="text"
            placeholder="搜索院校名称、城市、类型，如「计算机」「上海」…"
          />
          <button type="submit" class="btn">搜索院校</button>
        </form>
        <div class="hero-stats">
          <div class="stat">
            <span class="stat-num">{{ schools.length }}</span>
            <span class="stat-label">收录院校</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat">
            <span class="stat-num">14</span>
            <span class="stat-label">学科门类</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat">
            <span class="stat-num">4</span>
            <span class="stat-label">年国家线数据</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat">
            <span class="stat-num">{{ totalA }}</span>
            <span class="stat-label">A+ 学科</span>
          </div>
        </div>
        <div class="hero-actions">
          <RouterLink to="/schools" class="btn btn-primary">浏览院校库</RouterLink>
          <RouterLink to="/ratios" class="btn btn-ghost">查报录比</RouterLink>
          <RouterLink to="/timeline" class="btn btn-ghost">考研流程</RouterLink>
        </div>
      </div>
    </section>

    <!-- 我的工具 -->
    <section class="section tools-section">
      <div class="container">
        <div class="tools-grid">
          <RouterLink to="/compare" class="tool-card card card-hover">
            <span class="tool-icon">⚖️</span>
            <div>
              <h3 class="tool-title">院校对比</h3>
              <p class="tool-desc">
                已选 {{ compareIds.length }} 所 · 横向对比层次、学科评估、复试线与报录比
              </p>
            </div>
          </RouterLink>
          <RouterLink to="/favorites" class="tool-card card card-hover">
            <span class="tool-icon">⭐</span>
            <div>
              <h3 class="tool-title">我的收藏</h3>
              <p class="tool-desc">已收藏 {{ favIds.length }} 所 · 心仪院校一键归档，本地保存</p>
            </div>
          </RouterLink>
          <RouterLink to="/ratios" class="tool-card card card-hover">
            <span class="tool-icon">📊</span>
            <div>
              <h3 class="tool-title">报录比查询</h3>
              <p class="tool-desc">报考人数 ÷ 录取人数 · 一眼看穿专业竞争激烈程度</p>
            </div>
          </RouterLink>
          <RouterLink to="/lines" class="tool-card card card-hover">
            <span class="tool-icon">📈</span>
            <div>
              <h3 class="tool-title">历年国家线</h3>
              <p class="tool-desc">2023-2026 年国家线 · 2026 年数据每周远程同步更新</p>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- 热门院校 -->
    <section class="section">
      <div class="container">
        <div class="section-head">
          <div>
            <h2 class="section-title">热门院校</h2>
            <p class="section-sub">按学科评估 A+ 学科数量精选，点击卡片查看详情</p>
          </div>
          <RouterLink to="/schools" class="btn btn-light">全部院校 →</RouterLink>
        </div>
        <div class="school-grid">
          <SchoolCard v-for="school in hotSchools" :key="school.id" :school="school" />
        </div>
      </div>
    </section>

    <!-- 考研流程速览 -->
    <section class="section timeline-section">
      <div class="container">
        <div class="section-head">
          <div>
            <h2 class="section-title">{{ examYear }} 考研关键节点</h2>
            <p class="section-sub">从报名到录取，掌握每个时间节点</p>
          </div>
          <RouterLink to="/timeline" class="btn btn-light">完整时间轴 →</RouterLink>
        </div>
        <div class="steps-grid">
          <div v-for="step in steps" :key="step.title" class="step-card card">
            <div class="step-status">
              <span class="badge" :class="`badge-${stageStatus(step)}`">
                {{ stageStatus(step) === 'done' ? '已完成' : stageStatus(step) === 'active' ? '进行中' : '未开始' }}
              </span>
            </div>
            <h3 class="step-title">{{ step.title }}</h3>
            <p class="step-date">{{ step.start.slice(5) }} ~ {{ step.end.slice(5) }}</p>
            <p class="step-desc">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 学科门类 -->
    <section class="section">
      <div class="container">
        <div class="section-head">
          <div>
            <h2 class="section-title">学科门类</h2>
            <p class="section-sub">学术学位共 14 个学科门类，选择你的目标方向</p>
          </div>
          <RouterLink to="/majors" class="btn btn-light">查看专业目录 →</RouterLink>
        </div>
        <div class="major-chips">
          <RouterLink
            v-for="m in majorCategories"
            :key="m.code"
            to="/majors"
            class="major-chip card card-hover"
          >
            <span class="major-code">{{ m.code }}</span>
            <span class="major-name">{{ m.name }}</span>
            <span v-if="m.popular" class="hot-dot" title="热门门类">🔥</span>
          </RouterLink>
        </div>
        <div class="note note-blue" style="margin-top: 24px">
          ⚠️ 本站学科评估、院校复试线、报录比等为示例数据，国家线 2026 年数据远程同步自开源项目
          kaoyan-site（每周更新）。报考信息请以
          <strong>中国研究生招生信息网（yz.chsi.com.cn）</strong> 及各高校研招网官方发布为准。
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Hero */
.hero {
  background: linear-gradient(135deg, #0f2a5f 0%, #1e40af 55%, #1d4ed8 100%);
  color: #fff;
  padding: 64px 0 60px;
  text-align: center;
}

.hero-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
}

.hero-badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.28);
  padding: 5px 16px;
  border-radius: 999px;
  font-size: 13px;
}

.hero-title {
  font-size: 46px;
  font-weight: 800;
  letter-spacing: 6px;
}

.hero-sub {
  font-size: 17px;
  color: rgba(255, 255, 255, 0.85);
  line-height: 1.9;
}

/* 倒计时 */
.countdown {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 14px 28px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 14px;
  box-shadow: none;
  flex-wrap: wrap;
  justify-content: center;
}

.cd-label {
  font-size: 15px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.cd-units {
  display: flex;
  gap: 10px;
}

.cd-unit {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(255, 255, 255, 0.16);
  border-radius: 10px;
  padding: 6px 14px;
  min-width: 62px;
}

.cd-num {
  font-size: 24px;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
}

.cd-text {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.75);
}

.hero-search {
  display: flex;
  width: 100%;
  max-width: 560px;
  gap: 10px;
}

.hero-search input {
  flex: 1;
  padding: 13px 18px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.96);
  font-size: 15px;
}

.hero-search .btn {
  padding: 13px 26px;
  background: var(--accent);
  color: #78350f;
  font-weight: 700;
}

.hero-search .btn:hover {
  background: #fbbf24;
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 28px;
  margin-top: 10px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.stat-num {
  font-size: 26px;
  font-weight: 800;
}

.stat-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.75);
}

.stat-divider {
  width: 1px;
  height: 36px;
  background: rgba(255, 255, 255, 0.25);
}

.hero-actions {
  display: flex;
  gap: 14px;
  margin-top: 8px;
  flex-wrap: wrap;
  justify-content: center;
}

/* 工具入口 */
.tools-section {
  padding-bottom: 24px;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.tool-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
}

.tool-icon {
  font-size: 28px;
}

.tool-title {
  font-size: 16px;
  font-weight: 700;
}

.tool-desc {
  font-size: 12.5px;
  color: var(--text-2);
  margin-top: 3px;
  line-height: 1.6;
}

/* 院校网格 */
.school-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

/* 流程速览 */
.timeline-section {
  background: var(--white);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.step-card {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.step-title {
  font-size: 16px;
  font-weight: 700;
}

.step-date {
  font-size: 13px;
  color: var(--primary);
  font-weight: 600;
}

.step-desc {
  font-size: 13px;
  color: var(--text-2);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 学科门类 */
.major-chips {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
}

.major-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px;
}

.major-code {
  font-size: 13px;
  font-weight: 700;
  color: var(--primary);
  background: var(--primary-light);
  border-radius: 6px;
  padding: 2px 7px;
}

.major-name {
  font-size: 14px;
  font-weight: 600;
  flex: 1;
}

/* 响应式 */
@media (max-width: 1024px) {
  .school-grid,
  .steps-grid,
  .tools-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .major-chips {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 34px;
  }

  .hero-search {
    flex-direction: column;
  }

  .hero-stats {
    flex-wrap: wrap;
    justify-content: center;
    gap: 16px;
  }

  .school-grid,
  .steps-grid,
  .tools-grid {
    grid-template-columns: 1fr;
  }

  .major-chips {
    grid-template-columns: repeat(2, 1fr);
  }

  .cd-units {
    gap: 6px;
  }

  .cd-unit {
    min-width: 52px;
    padding: 5px 10px;
  }
}
</style>
