/**
 * 备考倒计时：自动计算下一届考研初试日期（每年 12 月 19 日，已过则顺延一年）
 */
import { computed, onBeforeUnmount, ref } from 'vue'

function nextExamDate(from = new Date()) {
  let year = from.getFullYear()
  let target = new Date(year, 11, 19, 8, 30, 0) // 12 月 19 日 8:30 开考
  if (target < from) {
    year += 1
    target = new Date(year, 11, 19, 8, 30, 0)
  }
  return { target, year: year + 1 } // 考研年份 = 考试年份 + 1
}

export function useCountdown() {
  const { target, year } = nextExamDate()
  const now = ref(Date.now())

  const timer = setInterval(() => {
    now.value = Date.now()
  }, 1000)

  onBeforeUnmount(() => clearInterval(timer))

  const countdown = computed(() => {
    const diff = target.getTime() - now.value
    if (diff <= 0) return { days: 0, hours: 0, minutes: 0, seconds: 0, finished: true }
    return {
      days: Math.floor(diff / 86400000),
      hours: Math.floor((diff % 86400000) / 3600000),
      minutes: Math.floor((diff % 3600000) / 60000),
      seconds: Math.floor((diff % 60000) / 1000),
      finished: false
    }
  })

  return { countdown, examYear: year }
}
