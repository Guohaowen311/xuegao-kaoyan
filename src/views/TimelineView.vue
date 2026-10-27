<script setup>
import { computed, onMounted, ref } from 'vue'
import { stages, examYear, stageStatus, statusText } from '../data/timeline'
import { getRemoteData } from '../api'

const activeStage = computed(() => stages.find((s) => stageStatus(s) === 'active'))

const doneCount = computed(() => stages.filter((s) => stageStatus(s) === 'done').length)

// 远程调剂贴士（kaoyan-site 每周更新）
const adjustTips = ref([])
onMounted(async () => {
  const { data } = await getRemoteData('adjust')
  adjustTips.value = data.items || []
})

function fmtDate(dateStr) {
  const [y, m, d] = dateStr.split('-')
  return `${y} 年 ${Number(m)} 月 ${Number(d)} 日`
}
</script>

<template>
  <div class="container section">
    <div class="page-head">
      <h1 class="page-title">{{ examYear }} 考研全流程</h1>
      <p class="page-sub">从大纲发布到录取入学，时间节点为历年惯例的预计安排，请以研招网官方通知为准</p>
    </div>

    <!-- 当前进度 -->
    <div class="progress-card card">
      <div class="progress-text">
        <span class="progress-label">当前进度</span>
        <p v-if="activeStage" class="progress-now">
          正在进行：<strong>{{ activeStage.title }}</strong>（{{ fmtDate(activeStage.start) }} ~
          {{ fmtDate(activeStage.end) }}）
        </p>
        <p v-else class="progress-now">
          已完成 {{ doneCount }} / {{ stages.length }} 个阶段
        </p>
      </div>
      <div class="progress-track">
        <div class="progress-fill" :style="{ width: `${((doneCount + (activeStage ? 0.5 : 0)) / stages.length) * 100}%` }"></div>
      </div>
      <p class="progress-tip">
        {{ activeStage ? activeStage.desc : '全部阶段已结束，祝各位研友顺利上岸！' }}
      </p>
    </div>

    <!-- 时间轴 -->
    <div class="timeline">
      <div
        v-for="(stage, i) in stages"
        :key="stage.title"
        class="tl-item"
        :class="`tl-${stageStatus(stage)}`"
      >
        <div class="tl-rail">
          <span class="tl-dot"></span>
          <span v-if="i < stages.length - 1" class="tl-line"></span>
        </div>
        <div class="tl-content card card-hover">
          <div class="tl-head">
            <span class="tl-index">第 {{ i + 1 }} 步</span>
            <span class="badge" :class="`badge-${stageStatus(stage)}`">
              {{ statusText[stageStatus(stage)] }}
            </span>
          </div>
          <h3 class="tl-title">{{ stage.title }}</h3>
          <p class="tl-date">📅 {{ fmtDate(stage.start) }} ~ {{ fmtDate(stage.end) }}</p>
          <p class="tl-desc">{{ stage.desc }}</p>
        </div>
      </div>
    </div>

    <!-- 调剂贴士（远程数据） -->
    <div v-if="adjustTips.length" class="tips-section">
      <h2 class="tips-title">💡 调剂贴士（远程同步 · 每周更新）</h2>
      <div class="tips-grid">
        <div v-for="tip in adjustTips" :key="tip.title" class="tip-card card">
          <div class="tip-head">
            <span class="badge" :class="`badge-${tip.tag === 'tag-important' ? '985' : tip.tag === 'tag-hot' ? 'syl' : 'zhu'}`">
              {{ tip.meta }}
            </span>
            <span class="tip-cat">{{ tip.category }}</span>
          </div>
          <p class="tip-text">{{ tip.title }}</p>
        </div>
      </div>
    </div>

    <div class="note" style="margin-top: 32px">
      ⚠️ 以上时间节点依据历年惯例整理，每年具体安排以教育部及中国研究生招生信息网（yz.chsi.com.cn）
      当年发布的通知为准。建议收藏研招网并关注目标院校研究生院公众号，避免错过关键节点。
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

.progress-card {
  padding: 24px;
  margin-bottom: 36px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  background: linear-gradient(135deg, #eff6ff, #ffffff);
}

.progress-label {
  font-size: 13px;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: 2px;
}

.progress-now {
  font-size: 16px;
  margin-top: 4px;
}

.progress-now strong {
  color: var(--primary);
}

.progress-track {
  height: 10px;
  border-radius: 999px;
  background: #e2e8f0;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--primary), #60a5fa);
  transition: width 0.4s ease;
}

.progress-tip {
  font-size: 13.5px;
  color: var(--text-2);
  line-height: 1.7;
}

.timeline {
  display: flex;
  flex-direction: column;
}

.tl-item {
  display: flex;
  gap: 18px;
}

.tl-rail {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  width: 24px;
}

.tl-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #cbd5e1;
  border: 3px solid #fff;
  box-shadow: 0 0 0 2px #cbd5e1;
  margin-top: 26px;
}

.tl-line {
  flex: 1;
  width: 2px;
  background: #e2e8f0;
  margin: 4px 0;
}

.tl-active .tl-dot {
  background: var(--accent);
  box-shadow: 0 0 0 2px var(--accent);
  animation: pulse 1.6s ease infinite;
}

.tl-done .tl-dot {
  background: #10b981;
  box-shadow: 0 0 0 2px #10b981;
}

.tl-done .tl-line {
  background: #a7f3d0;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 2px var(--accent);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(245, 158, 11, 0.3);
  }
}

.tl-content {
  flex: 1;
  padding: 22px;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tl-active .tl-content {
  border-color: var(--accent);
  box-shadow: 0 4px 20px rgba(245, 158, 11, 0.18);
}

.tl-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tl-index {
  font-size: 12px;
  font-weight: 700;
  color: var(--primary);
  background: var(--primary-light);
  padding: 2px 10px;
  border-radius: 999px;
}

.tl-title {
  font-size: 18px;
  font-weight: 700;
}

.tl-date {
  font-size: 13px;
  color: var(--primary);
  font-weight: 600;
}

.tl-desc {
  font-size: 13.5px;
  color: var(--text-2);
  line-height: 1.8;
}

.tips-section {
  margin-top: 36px;
}

.tips-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 14px;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.tip-card {
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tip-head {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tip-cat {
  font-size: 12px;
  color: #9ca3af;
}

.tip-text {
  font-size: 14px;
  line-height: 1.7;
  font-weight: 600;
}

@media (max-width: 768px) {
  .tips-grid {
    grid-template-columns: 1fr;
  }
}
</style>
