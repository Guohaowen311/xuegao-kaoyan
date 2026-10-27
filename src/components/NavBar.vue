<script setup>
import { useCollection } from '../composables/useCollection'

const { favIds, compareIds } = useCollection()

const links = [
  { to: '/', label: '首页' },
  { to: '/schools', label: '院校库' },
  { to: '/ratios', label: '报录比' },
  { to: '/majors', label: '专业目录' },
  { to: '/lines', label: '国家线' },
  { to: '/timeline', label: '考研流程' }
]
</script>

<template>
  <header class="navbar">
    <div class="container nav-inner">
      <RouterLink to="/" class="brand">
        <span class="brand-logo">🍦</span>
        <span class="brand-name">雪糕考研</span>
      </RouterLink>
      <nav class="nav-links">
        <RouterLink
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          class="nav-link"
          active-class="nav-link-active"
        >
          {{ link.label }}
        </RouterLink>
        <RouterLink
          to="/favorites"
          class="nav-link nav-icon-link"
          active-class="nav-link-active"
          :title="`我的收藏（${favIds.length}）`"
        >
          ⭐ 收藏<span v-if="favIds.length" class="nav-count">{{ favIds.length }}</span>
        </RouterLink>
        <RouterLink
          to="/compare"
          class="nav-link nav-icon-link"
          active-class="nav-link-active"
          :title="`院校对比（${compareIds.length}）`"
        >
          ⚖️ 对比<span v-if="compareIds.length" class="nav-count">{{ compareIds.length }}</span>
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  gap: 12px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  flex-shrink: 0;
}

.brand-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #60a5fa, var(--primary));
  font-size: 18px;
}

.brand-name {
  font-size: 19px;
  letter-spacing: 1px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 15px;
  color: var(--text-2);
  transition: all 0.2s ease;
  white-space: nowrap;
}

.nav-link:hover {
  color: var(--primary);
  background: var(--primary-light);
}

.nav-link-active {
  color: var(--primary);
  background: var(--primary-light);
  font-weight: 600;
}

.nav-icon-link {
  font-size: 14px;
}

.nav-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 999px;
  background: #dc2626;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
}

@media (max-width: 900px) {
  .nav-inner {
    height: auto;
    flex-direction: column;
    padding: 12px 16px;
    gap: 8px;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-link {
    font-size: 14px;
    padding: 6px 10px;
  }
}
</style>
