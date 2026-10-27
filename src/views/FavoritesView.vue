<script setup>
import { computed } from 'vue'
import { getSchool } from '../data/schools'
import { useCollection } from '../composables/useCollection'
import SchoolCard from '../components/SchoolCard.vue'

const { favIds } = useCollection()

const favSchools = computed(() =>
  favIds.value.map((id) => getSchool(id)).filter(Boolean)
)
</script>

<template>
  <div class="container section">
    <div class="page-head">
      <h1 class="page-title">⭐ 我的收藏</h1>
      <p class="page-sub">已收藏 {{ favSchools.length }} 所院校，数据保存在本地浏览器</p>
    </div>

    <div v-if="favSchools.length" class="school-grid">
      <SchoolCard v-for="school in favSchools" :key="school.id" :school="school" />
    </div>
    <div v-else class="empty card">
      <p class="empty-icon">💫</p>
      <p>还没有收藏任何院校</p>
      <p class="empty-sub">在院校库中点击卡片右上角的 ☆ 即可收藏心仪院校</p>
      <RouterLink to="/schools" class="btn btn-primary" style="margin-top: 16px">去逛逛院校库</RouterLink>
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

.school-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
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

@media (max-width: 1024px) {
  .school-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .school-grid {
    grid-template-columns: 1fr;
  }
}
</style>
