/**
 * 历年考研国家线（学术学位）
 * 数据来源：中国研究生招生信息网（yz.chsi.com.cn）及公开报道整理
 * 注：B区总分按「A区 - 10分」估算，单科线 2024/2023 年数据未收录
 * 仅供参考，请以研招网官方发布为准
 */

export const aZoneProvinces = [
  '北京', '天津', '河北', '山西', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江',
  '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '重庆', '四川', '陕西'
]

export const bZoneProvinces = [
  '内蒙古', '广西', '海南', '贵州', '云南', '西藏', '甘肃', '青海', '宁夏', '新疆'
]

// 学科门类基础信息
export const categories = [
  { code: '01', name: '哲学' },
  { code: '02', name: '经济学' },
  { code: '03', name: '法学' },
  { code: '04', name: '教育学' },
  { code: '05', name: '文学' },
  { code: '06', name: '历史学' },
  { code: '07', name: '理学' },
  { code: '08', name: '工学' },
  { code: '09', name: '农学' },
  { code: '10', name: '医学' },
  { code: '11', name: '军事学' },
  { code: '12', name: '管理学' },
  { code: '13', name: '艺术学' },
  { code: '14', name: '交叉学科' }
]

// 2025 年（含单科线，官方发布）
export const lines2025 = [
  { code: '01', name: '哲学', a: 321, b: 311, single100: 39, single150: 59 },
  { code: '02', name: '经济学', a: 323, b: 313, single100: 40, single150: 60 },
  { code: '03', name: '法学', a: 323, b: 313, single100: 40, single150: 60 },
  { code: '04', name: '教育学', a: 341, b: 331, single100: 45, single150: 135, note: '教育[0451]、国际中文教育[0453]等；体育学[0403]总分 304' },
  { code: '05', name: '文学', a: 351, b: 341, single100: 47, single150: 71 },
  { code: '06', name: '历史学', a: 336, b: 326, single100: 43, single150: 129 },
  { code: '07', name: '理学', a: 274, b: 264, single100: 34, single150: 51 },
  { code: '08', name: '工学', a: 260, b: 250, single100: 34, single150: 51, note: '工学照顾专业总分 251' },
  { code: '09', name: '农学', a: 245, b: 235, single100: 33, single150: 50 },
  { code: '10', name: '医学', a: 293, b: 283, single100: 36, single150: 108 },
  { code: '11', name: '军事学', a: 260, b: 250, single100: 34, single150: 51 },
  { code: '12', name: '管理学', a: 333, b: 323, single100: 41, single150: 62, note: '工商管理[1251]151分、公共管理[1252]164分、会计[1253]194分等专业学位单列' },
  { code: '13', name: '艺术学', a: 351, b: 341, single100: 37, single150: 56 },
  { code: '14', name: '交叉学科', a: 266, b: 256, single100: 34, single150: 51 }
]

// 2024 年（总分）
export const lines2024 = [
  { code: '01', name: '哲学', a: 333, b: 323 },
  { code: '02', name: '经济学', a: 338, b: 328 },
  { code: '03', name: '法学', a: 331, b: 321 },
  { code: '04', name: '教育学', a: 350, b: 340 },
  { code: '05', name: '文学', a: 365, b: 355 },
  { code: '06', name: '历史学', a: 345, b: 335 },
  { code: '07', name: '理学', a: 288, b: 278 },
  { code: '08', name: '工学', a: 273, b: 263 },
  { code: '09', name: '农学', a: 251, b: 241 },
  { code: '10', name: '医学', a: 304, b: 294 },
  { code: '11', name: '军事学', a: 260, b: 250 },
  { code: '12', name: '管理学', a: 347, b: 337 },
  { code: '13', name: '艺术学', a: 362, b: 352 },
  { code: '14', name: '交叉学科', a: 275, b: 265 }
]

// 2023 年（总分）
export const lines2023 = [
  { code: '01', name: '哲学', a: 323, b: 313 },
  { code: '02', name: '经济学', a: 346, b: 336 },
  { code: '03', name: '法学', a: 326, b: 316 },
  { code: '04', name: '教育学', a: 350, b: 340 },
  { code: '05', name: '文学', a: 363, b: 353 },
  { code: '06', name: '历史学', a: 336, b: 326 },
  { code: '07', name: '理学', a: 279, b: 269 },
  { code: '08', name: '工学', a: 273, b: 263 },
  { code: '09', name: '农学', a: 251, b: 241 },
  { code: '10', name: '医学', a: 296, b: 286 },
  { code: '11', name: '军事学', a: 260, b: 250 },
  { code: '12', name: '管理学', a: 340, b: 330 },
  { code: '13', name: '艺术学', a: 362, b: 352 },
  { code: '14', name: '交叉学科', a: 265, b: 255 }
]

export const yearLines = {
  2025: lines2025,
  2024: lines2024,
  2023: lines2023
}

/** 计算某年较上一年的总分变化（返回 null 表示无上一年数据） */
export function deltaOf(year, line) {
  const prev = yearLines[year - 1]
  if (!prev) return null
  const prevLine = prev.find((l) => l.code === line.code)
  if (!prevLine) return null
  return line.a - prevLine.a
}
