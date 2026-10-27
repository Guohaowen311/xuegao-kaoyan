/**
 * 远程数据接入层（真实 API）
 *
 * 数据源：kaoyan-site 开源考研数据项目（GitHub: danking211367/kaoyan-site）
 * 该项目每周更新国家线、调剂信息、考研日历等公开数据。
 *
 * 请求策略（多重降级）：
 *   1. raw.githubusercontent.com 直连（快，无鉴权）
 *   2. api.github.com 官方 API（base64 内容，CORS 友好）
 *   3. 本地打包快照（src/data/remote/*.json，保证离线可用）
 *
 * 缓存策略：localStorage 缓存 24 小时，避免触发 GitHub API 速率限制
 */

import fallbackScores from '../data/remote/scores.json'
import fallbackTimeline from '../data/remote/timeline.json'
import fallbackAdjust from '../data/remote/adjust.json'
import fallbackLastUpdate from '../data/remote/last-update.json'

const REPO = 'danking211367/kaoyan-site'
const BRANCH = 'main'
const RAW_BASE = `https://raw.githubusercontent.com/${REPO}/${BRANCH}/data`
const API_BASE = `https://api.github.com/repos/${REPO}/contents/data`
const CACHE_KEY = 'xuegao-kaoyan-remote-cache'
const CACHE_TTL = 24 * 60 * 60 * 1000 // 24 小时

const fallbacks = {
  scores: fallbackScores,
  timeline: fallbackTimeline,
  adjust: fallbackAdjust,
  'last-update': fallbackLastUpdate
}

function readCache(file) {
  try {
    const cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}')
    const hit = cache[file]
    if (hit && Date.now() - hit.timestamp < CACHE_TTL) return hit.data
  } catch {
    /* 忽略缓存读取错误 */
  }
  return null
}

function writeCache(file, data) {
  try {
    const cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}')
    cache[file] = { data, timestamp: Date.now() }
    localStorage.setItem(CACHE_KEY, JSON.stringify(cache))
  } catch {
    /* 忽略缓存写入错误 */
  }
}

async function fetchWithTimeout(url, ms = 8000) {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), ms)
  try {
    const res = await fetch(url, { signal: controller.signal })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return res
  } finally {
    clearTimeout(timer)
  }
}

/** 依次尝试 raw → GitHub API，失败则抛错由调用方降级 */
async function fetchRemote(file) {
  // 1. raw 直连
  try {
    const res = await fetchWithTimeout(`${RAW_BASE}/${file}.json`)
    return await res.json()
  } catch {
    /* 继续降级 */
  }
  // 2. GitHub API（base64）
  const res = await fetchWithTimeout(`${API_BASE}/${file}.json`)
  const payload = await res.json()
  const bytes = Uint8Array.from(atob(payload.content), (c) => c.charCodeAt(0))
  return JSON.parse(new TextDecoder('utf-8').decode(bytes))
}

/**
 * 获取远程数据（带缓存与本地降级）
 * @param {'scores'|'timeline'|'adjust'|'last-update'} file
 * @returns {Promise<{data: object, source: 'remote'|'cache'|'fallback'}>}
 */
export async function getRemoteData(file) {
  const cached = readCache(file)
  if (cached) return { data: cached, source: 'cache' }
  try {
    const data = await fetchRemote(file)
    writeCache(file, data)
    return { data, source: 'remote' }
  } catch {
    return { data: fallbacks[file], source: 'fallback' }
  }
}

/**
 * 预留：接入商业考研数据 API（如聚合数据 / 阿里云市场等）
 * 在 .env 中配置 VITE_KAOYAN_API_URL 与 VITE_KAOYAN_API_KEY 后，
 * 可在此函数中对接真实报录比、院校库、复试线接口。
 */
export async function fetchFromConfiguredApi(path, params = {}) {
  const base = import.meta.env.VITE_KAOYAN_API_URL
  const key = import.meta.env.VITE_KAOYAN_API_KEY
  if (!base) return null
  const url = new URL(path, base)
  Object.entries({ ...params, key }).forEach(([k, v]) => url.searchParams.set(k, v))
  const res = await fetchWithTimeout(url.toString())
  return res.json()
}
