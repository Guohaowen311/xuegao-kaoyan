/**
 * 收藏夹 + 院校对比状态（模块级单例，localStorage 持久化）
 */
import { ref, watch } from 'vue'

const FAV_KEY = 'xuegao-favorites'
const CMP_KEY = 'xuegao-compare'
const MAX_COMPARE = 4

function load(key) {
  try {
    return JSON.parse(localStorage.getItem(key) || '[]')
  } catch {
    return []
  }
}

const favIds = ref(load(FAV_KEY))
const compareIds = ref(load(CMP_KEY))

watch(
  favIds,
  (v) => localStorage.setItem(FAV_KEY, JSON.stringify(v)),
  { deep: true }
)

watch(
  compareIds,
  (v) => localStorage.setItem(CMP_KEY, JSON.stringify(v)),
  { deep: true }
)

function toggleFav(id) {
  const i = favIds.value.indexOf(id)
  if (i >= 0) favIds.value.splice(i, 1)
  else favIds.value.push(id)
}

function isFav(id) {
  return favIds.value.includes(id)
}

function toggleCompare(id) {
  const i = compareIds.value.indexOf(id)
  if (i >= 0) {
    compareIds.value.splice(i, 1)
  } else {
    if (compareIds.value.length >= MAX_COMPARE) {
      return { ok: false, reason: `最多同时对比 ${MAX_COMPARE} 所院校` }
    }
    compareIds.value.push(id)
  }
  return { ok: true }
}

function isCompared(id) {
  return compareIds.value.includes(id)
}

function clearCompare() {
  compareIds.value = []
}

export function useCollection() {
  return {
    favIds,
    compareIds,
    toggleFav,
    isFav,
    toggleCompare,
    isCompared,
    clearCompare,
    MAX_COMPARE
  }
}
