import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('../views/HomeView.vue'), meta: { title: '首页' } },
  { path: '/schools', name: 'schools', component: () => import('../views/SchoolsView.vue'), meta: { title: '院校库' } },
  { path: '/schools/:id', name: 'school-detail', component: () => import('../views/SchoolDetailView.vue'), meta: { title: '院校详情' } },
  { path: '/ratios', name: 'ratios', component: () => import('../views/RatiosView.vue'), meta: { title: '报录比查询' } },
  { path: '/majors', name: 'majors', component: () => import('../views/MajorsView.vue'), meta: { title: '专业目录' } },
  { path: '/lines', name: 'lines', component: () => import('../views/ScoreLinesView.vue'), meta: { title: '国家线' } },
  { path: '/timeline', name: 'timeline', component: () => import('../views/TimelineView.vue'), meta: { title: '考研流程' } },
  { path: '/favorites', name: 'favorites', component: () => import('../views/FavoritesView.vue'), meta: { title: '我的收藏' } },
  { path: '/compare', name: 'compare', component: () => import('../views/CompareView.vue'), meta: { title: '院校对比' } },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  // BASE_URL 在 GitHub Pages 子路径部署时自动带上 /仓库名/ 前缀
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.afterEach((to) => {
  document.title = `${to.meta.title} - 雪糕考研`
})

export default router
