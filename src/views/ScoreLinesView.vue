<script setup>
import { computed, onMounted, ref } from 'vue'
import { yearLines, deltaOf, aZoneProvinces, bZoneProvinces } from '../data/scoreLines'
import { getRemoteData } from '../api'

const years = [2026, 2025, 2024, 2023]
const activeYear = ref(2026)

// 2026 年数据来自远程 API（带本地快照降级）
const remote = ref(null)
const remoteSource = ref('')
const loading = ref(false)

const sourceText = {
  remote: '远程实时',
  cache: '本地缓存（24h 内同步）',
  fallback: '本地快照（离线模式）'
}

async function loadRemote() {
  loading.value = true
  const { data, source } = await getRemoteData('scores')
  remote.value = data
  remoteSource.value = source
  loading.value = false
}

onMounted(loadRemote)

const lines = computed(() => yearLines[activeYear.value])

const academic2026 = computed(() => remote.value?.academic || [])
const professional2026 = computed(() => remote.value?.professional || [])

function delta(line) {
  const d = deltaOf(activeYear.value, line)
  if (d === null) return null
  if (d === 0) return { text: '持平', cls: 'flat' }
  return d > 0 ? { text: `+${d}`, cls: 'up' } : { text: `${d}`, cls: 'down' }
}

function fmtChange(str) {
  if (!str) return { text: '—', cls: 'flat' }
  if (str === '→') return { text: '持平', cls: 'flat' }
  if (str.startsWith('↑')) return { text: `+${str.slice(1)}`, cls: 'up' }
  if (str.startsWith('↓')) return { text: `-${str.slice(1)}`, cls: 'down' }
  return { text: str, cls: 'flat' }
}
</script>

<template>
  <div class="container section">
    <div class="page-head">
      <h1 class="page-title">历年国家线</h1>
      <p class="page-sub">全国硕士研究生招生考试考生进入复试的初试成绩基本要求</p>
    </div>

    <!-- 年份切换 -->
    <div class="year-tabs">
      <button
        v-for="y in years"
        :key="y"
        class="year-tab"
        :class="{ 'year-tab-on': activeYear === y }"
        @click="activeYear = y"
      >
        {{ y }} 年
        <span v-if="y === 2026" class="tab-new">最新</span>
      </button>
    </div>

    <!-- 2026 年：远程数据（学术学位） -->
    <template v-if="activeYear === 2026">
      <div class="sync-bar">
        <span v-if="loading" class="sync-status">🔄 正在同步最新数据…</span>
        <template v-else-if="remote">
          <span class="sync-status">
            ✅ 数据来源：{{ sourceText[remoteSource] }}
          </span>
          <span v-if="remote.updatedAt" class="sync-time">
            更新于 {{ remote.updatedAt.slice(0, 10) }}
          </span>
        </template>
        <button class="btn btn-light sync-btn" :disabled="loading" @click="loadRemote">
          {{ loading ? '同步中…' : '立即同步' }}
        </button>
      </div>

      <h2 class="sub-title">学术学位</h2>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>学科门类</th>
              <th>A 区总分</th>
              <th>B 区总分</th>
              <th>较上年变化</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="line in academic2026" :key="line.name">
              <td><strong>{{ line.name }}</strong></td>
              <td><span class="num">{{ line.a }}</span></td>
              <td>{{ line.b }}</td>
              <td>
                <span class="delta" :class="fmtChange(line.change).cls">
                  {{ fmtChange(line.change).text }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="sub-title" style="margin-top: 28px">专业学位</h2>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>专业学位类别</th>
              <th>A 区总分</th>
              <th>B 区总分</th>
              <th>较上年变化</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="line in professional2026" :key="line.name">
              <td><strong>{{ line.name }}</strong></td>
              <td><span class="num">{{ line.a }}</span></td>
              <td>{{ line.b }}</td>
              <td>
                <span class="delta" :class="fmtChange(line.change).cls">
                  {{ fmtChange(line.change).text }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- 2023-2025：本地数据（学术学位） -->
    <template v-else>
      <div class="table-wrap" style="margin-top: 18px">
        <table class="data-table">
          <thead>
            <tr>
              <th>学科门类</th>
              <th>A 区总分</th>
              <th>B 区总分（约）</th>
              <th v-if="activeYear === 2025">单科（=100 分）</th>
              <th v-if="activeYear === 2025">单科（>100 分）</th>
              <th>较上年变化</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="line in lines" :key="line.code">
              <td>
                <strong>{{ line.name }}</strong>
                <span class="code">{{ line.code }}</span>
                <span v-if="line.note" class="row-note">{{ line.note }}</span>
              </td>
              <td><span class="num">{{ line.a }}</span></td>
              <td>{{ line.b }}</td>
              <td v-if="activeYear === 2025">{{ line.single100 }}</td>
              <td v-if="activeYear === 2025">{{ line.single150 }}</td>
              <td>
                <span v-if="delta(line)" class="delta" :class="delta(line).cls">
                  {{ delta(line).text }}
                </span>
                <span v-else class="delta-none">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <div class="note" style="margin-top: 18px">
      <strong>A 区（21 省/直辖市）：</strong>{{ aZoneProvinces.join('、') }}<br />
      <strong>B 区（10 省/自治区）：</strong>{{ bZoneProvinces.join('、') }}<br />
      B 区线通常比 A 区低 10 分左右，本站 B 区总分按「A 区 − 10」估算，仅供参考。
    </div>

    <div class="note note-blue" style="margin-top: 14px">
      📌 2026 年数据同步自开源项目 kaoyan-site（每周更新）；2023-2025 年数据整理自中国研究生招生信息网。
      实际分数线请以研招网官方发布为准。
    </div>
  </div>
</template>

<style scoped>
.page-head {
  margin-bottom: 20px;
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

.year-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.year-tab {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 24px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--white);
  font-size: 15px;
  font-weight: 600;
  color: var(--text-2);
  transition: all 0.2s ease;
}

.year-tab:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.year-tab-on {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
}

.year-tab-on:hover {
  color: #fff;
}

.tab-new {
  font-size: 11px;
  background: var(--accent);
  color: #78350f;
  border-radius: 999px;
  padding: 1px 8px;
  font-weight: 700;
}

.sync-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin: 18px 0 6px;
  padding: 12px 16px;
  background: var(--primary-light);
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  font-size: 13.5px;
}

.sync-status {
  color: #1e40af;
  font-weight: 600;
}

.sync-time {
  color: var(--text-2);
  font-size: 12.5px;
}

.sync-btn {
  margin-left: auto;
  padding: 6px 14px;
  font-size: 13px;
}

.sub-title {
  font-size: 18px;
  font-weight: 700;
  margin: 20px 0 12px;
}

.code {
  margin-left: 8px;
  font-size: 12px;
  color: #9ca3af;
}

.row-note {
  display: block;
  font-size: 11.5px;
  color: #9ca3af;
  margin-top: 2px;
  max-width: 320px;
  line-height: 1.5;
}

.delta {
  font-weight: 700;
  font-size: 13px;
  padding: 2px 9px;
  border-radius: 999px;
}

.delta.up {
  background: #fef2f2;
  color: #dc2626;
}

.delta.down {
  background: #ecfdf5;
  color: #059669;
}

.delta.flat {
  background: #f1f5f9;
  color: #64748b;
}

.delta-none {
  color: #cbd5e1;
}
</style>
