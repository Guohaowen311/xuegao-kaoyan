<script setup>
import { tagLabels } from '../data/schools'
import { useCollection } from '../composables/useCollection'

const props = defineProps({
  school: { type: Object, required: true }
})

const { toggleFav, isFav, toggleCompare, isCompared } = useCollection()

function onToggleFav() {
  toggleFav(props.school.id)
}

function onToggleCompare() {
  const r = toggleCompare(props.school.id)
  if (!r.ok) alert(r.reason)
}
</script>

<template>
  <div class="school-card card card-hover">
    <div class="card-actions">
      <button
        class="act-btn"
        :class="{ 'act-on': isFav(school.id) }"
        :title="isFav(school.id) ? '取消收藏' : '加入收藏'"
        @click.stop.prevent="onToggleFav"
      >
        {{ isFav(school.id) ? '⭐' : '☆' }}
      </button>
      <button
        class="act-btn"
        :class="{ 'act-on': isCompared(school.id) }"
        :title="isCompared(school.id) ? '移出对比' : '加入对比'"
        @click.stop.prevent="onToggleCompare"
      >
        ⚖
      </button>
    </div>
    <RouterLink :to="`/schools/${school.id}`" class="card-main">
      <div class="card-head">
        <h3 class="school-name">{{ school.name }}</h3>
        <div class="school-tags">
          <span
            v-for="tag in school.tags"
            :key="tag"
            class="badge"
            :class="`badge-${tag === '985' ? '985' : tag === '211' ? '211' : tag === '双一流' ? 'syl' : 'zhu'}`"
          >
            {{ tagLabels[tag] }}
          </span>
        </div>
      </div>
      <p class="school-meta">
        <span class="badge badge-region">{{ school.region }} · {{ school.city }}</span>
        <span class="badge badge-type">{{ school.type }}类</span>
        <span v-if="school.evalKnown && school.evalA.ap > 0" class="eval-text">
          A+ 学科 ×{{ school.evalA.ap }}
        </span>
      </p>
      <p class="school-intro">{{ school.intro }}</p>
      <div class="card-foot">
        <span class="more">查看详情</span>
        <span class="arrow">→</span>
      </div>
    </RouterLink>
  </div>
</template>

<style scoped>
.school-card {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 20px;
  gap: 10px;
}

.card-actions {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  gap: 6px;
  z-index: 2;
}

.act-btn {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #f8fafc;
  border: 1px solid var(--border);
  font-size: 15px;
  color: #94a3b8;
  transition: all 0.15s ease;
}

.act-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
  background: var(--primary-light);
}

.act-btn.act-on {
  background: var(--primary-light);
  border-color: var(--primary);
  color: var(--primary);
}

.card-main {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

.card-head {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-right: 66px;
}

.school-name {
  font-size: 18px;
  font-weight: 700;
}

.school-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.school-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  font-size: 13px;
}

.eval-text {
  color: var(--accent);
  font-weight: 600;
  font-size: 13px;
}

.school-intro {
  font-size: 13px;
  color: var(--text-2);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.card-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 10px;
  border-top: 1px solid var(--border);
  font-size: 13px;
  font-weight: 600;
  color: var(--primary);
}

.arrow {
  transition: transform 0.2s ease;
}

.school-card:hover .arrow {
  transform: translateX(4px);
}
</style>
