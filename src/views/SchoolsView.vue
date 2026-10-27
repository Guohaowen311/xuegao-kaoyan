<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { schools, regions, schoolTypes } from '../data/schools'
import SchoolCard from '../components/SchoolCard.vue'

const route = useRoute()
const router = useRouter()

const keyword = ref(route.query.q || '')
const region = ref('全部')
const type = ref('全部')
const selectedTags = ref([])
const sortBy = ref('default')

watch(
  () => route.query.q,
  (q) => {
    keyword.value = q || ''
  }
)

const levelOptions = ['985', '211', '双一流', '自划线']

function toggleTag(tag) {
  const i = selectedTags.value.indexOf(tag)
  if (i >= 0) selectedTags.value.splice(i, 1)
  else selectedTags.value.push(tag)
}

const filtered = computed(() => {
  let list = [...schools]
  const kw = keyword.value.trim().toLowerCase()
  if (kw) {
    list = list.filter(
      (s) =>
        s.name.toLowerCase().includes(kw) ||
        s.city.toLowerCase().includes(kw) ||
        s.type.toLowerCase().includes(kw) ||
        s.intro.toLowerCase().includes(kw)
    )
  }
  if (region.value !== '全部') list = list.filter((s) => s.region === region.value)
  if (type.value !== '全部') list = list.filter((s) => s.type === type.value)
  if (selectedTags.value.length) {
    list = list.filter((s) => selectedTags.value.every((t) => s.tags.includes(t)))
  }
  if (sortBy.value === 'evalA') {
    list.sort((a, b) => b.evalA.ap - a.evalA.ap)
  }
  return list
})

function updateQuery() {
  router.replace({ path: '/schools', query: keyword.value.trim() ? { q: keyword.value.trim() } : {} })
}

function resetAll() {
  keyword.value = ''
  region.value = '全部'
  type.value = '全部'
  selectedTags.value = []
  sortBy.value = 'default'
  router.replace('/schools')
}
</script>

<template>
  <div class="container section">
    <div class="page-head">
      <h1 class="page-title">院校库</h1>
      <p class="page-sub">共收录 {{ schools.length }} 所代表性高校，支持按地区、类型、层次筛选</p>
    </div>

    <!-- 搜索与筛选 -->
    <div class="filter-panel card">
      <div class="search-row">
        <input
          v-model="keyword"
          type="text"
          placeholder="输入院校名称 / 城市 / 专业关键词…"
          @keyup.enter="updateQuery"
        />
        <button class="btn btn-primary" @click="updateQuery">搜索</button>
        <button class="btn btn-light" @click="resetAll">重置筛选</button>
      </div>

      <div class="filter-row">
        <span class="filter-label">地区</span>
        <div class="chip-group">
          <button
            class="chip"
            :class="{ 'chip-on': region === '全部' }"
            @click="region = '全部'"
          >
            全部
          </button>
          <button
            v-for="r in regions"
            :key="r"
            class="chip"
            :class="{ 'chip-on': region === r }"
            @click="region = r"
          >
            {{ r }}
          </button>
        </div>
      </div>

      <div class="filter-row">
        <span class="filter-label">类型</span>
        <div class="chip-group">
          <button
            class="chip"
            :class="{ 'chip-on': type === '全部' }"
            @click="type = '全部'"
          >
            全部
          </button>
          <button
            v-for="t in schoolTypes.filter((t) => schools.some((s) => s.type === t))"
            :key="t"
            class="chip"
            :class="{ 'chip-on': type === t }"
            @click="type = t"
          >
            {{ t }}
          </button>
        </div>
      </div>

      <div class="filter-row">
        <span class="filter-label">层次</span>
        <div class="chip-group">
          <button
            v-for="lv in levelOptions"
            :key="lv"
            class="chip chip-tag"
            :class="{ 'chip-on': selectedTags.includes(lv) }"
            @click="toggleTag(lv)"
          >
            {{ lv }}
          </button>
          <span class="hint">多选，需同时满足</span>
        </div>
      </div>
    </div>

    <!-- 结果 -->
    <div class="result-bar">
      <span>找到 <strong class="result-count">{{ filtered.length }}</strong> 所院校</span>
      <select v-model="sortBy" class="sort-select">
        <option value="default">默认排序</option>
        <option value="evalA">按 A+ 学科数排序</option>
      </select>
    </div>

    <div v-if="filtered.length" class="school-grid">
      <SchoolCard v-for="school in filtered" :key="school.id" :school="school" />
    </div>
    <div v-else class="empty card">
      <p class="empty-icon">🔍</p>
      <p>没有找到符合条件的院校，试试调整筛选条件</p>
      <button class="btn btn-primary" style="margin-top: 12px" @click="resetAll">清除筛选</button>
    </div>

    <div class="note" style="margin-top: 32px">
      💡 院校复试线、学科评估等数据为示例数据，仅供参考。报考前请务必前往各高校研究生招生网核实最新招生简章与专业目录。
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

.filter-panel {
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.search-row {
  display: flex;
  gap: 10px;
}

.search-row input {
  flex: 1;
  padding: 11px 16px;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 15px;
  transition: border-color 0.2s;
}

.search-row input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.12);
}

.filter-row {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.filter-label {
  flex-shrink: 0;
  width: 44px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-2);
  padding-top: 5px;
}

.chip-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  padding: 5px 14px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--white);
  font-size: 13px;
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

.chip-tag.chip-on {
  background: #dc2626;
  border-color: #dc2626;
}

.hint {
  align-self: center;
  font-size: 12px;
  color: #9ca3af;
}

.result-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 24px 0 16px;
  font-size: 14px;
  color: var(--text-2);
}

.result-count {
  color: var(--primary);
  font-size: 18px;
}

.sort-select {
  padding: 7px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--white);
}

.school-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
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

@media (max-width: 1024px) {
  .school-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .school-grid {
    grid-template-columns: 1fr;
  }

  .search-row {
    flex-wrap: wrap;
  }

  .filter-row {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
