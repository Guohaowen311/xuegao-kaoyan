# 🍦 雪糕考研 - 考研院校与信息平台

基于 Vue 3 + Vite 的考研信息一站式查询网站，中文界面。

## 功能页面

| 页面 | 路由 | 说明 |
| --- | --- | --- |
| 首页 | `/` | 备考倒计时、院校搜索、热门院校、关键节点速览、工具入口 |
| 院校库 | `/schools` | 137 所高校（全部 985、主要 211、双一流新增院校），地区 / 类型 / 层次筛选 + 搜索 |
| 院校详情 | `/schools/:id` | 简介、学科评估（9 档 + 学科明细）、近 5 年复试线（2021-2025，覆盖全部参评学科，可筛选）、报录比速览、收藏与对比、同地区推荐 |
| 报录比查询 | `/ratios` | 覆盖全部 137 所院校（2023-2025，优势学科 + 热门专业），竞争程度分级（示例数据） |
| 专业目录 | `/majors` | 14 个学科门类，展开查看一级学科，点击可查看该学科所有参评学校的评估排名（A+ 至 C-） |
| 国家线 | `/lines` | 2023-2026 年国家线，**2026 年数据远程同步**（学硕 + 专硕，每周更新） |
| 考研流程 | `/timeline` | 2027 考研全流程时间轴（自动标注进度）+ 调剂贴士（远程同步） |
| 我的收藏 | `/favorites` | 收藏夹，localStorage 持久化 |
| 院校对比 | `/compare` | 最多 4 所院校横向对比（层次 / 学科评估 / 复试线 / 报录比） |

## 真实数据接入（API）

### 已接入：开源考研数据项目

数据源：[kaoyan-site](https://github.com/danking211367/kaoyan-site)（考研干货公益网站，每周更新国家线、调剂信息、考研日历）

- 请求策略见 [src/api/index.js](src/api/index.js)：raw.githubusercontent → GitHub API → 本地快照（`src/data/remote/`）三级降级
- localStorage 缓存 24 小时，避免触发 GitHub 速率限制
- 国家线页 2026 年数据、考研流程页调剂贴士均走该通道，页面上可看到数据来源与更新时间

### 可扩展：商业 API

报录比、院校库等数据目前为**示例数据**。如需真实数据，可购买聚合数据（juhe.cn）
或阿里云 API 市场等平台的考研数据服务，配置 `.env`：

```bash
VITE_KAOYAN_API_URL=https://v.juhe.cn/kaoyan/...
VITE_KAOYAN_API_KEY=你的key
```

然后在 [src/api/index.js](src/api/index.js) 的 `fetchFromConfiguredApi` 中对接具体接口。

## 技术栈

- Vue 3（组合式 API）+ Vue Router 4
- Vite 6
- 纯手写 CSS 设计系统（CSS 变量 + 响应式），无 UI 框架依赖
- 状态管理：composable 单例（收藏 / 对比，localStorage 持久化）

## 本地运行

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # 构建到 dist/
```

## 数据说明

- 2026 年国家线：远程同步自 kaoyan-site 开源项目
- 2023-2025 年国家线：整理自中国研究生招生信息网（yz.chsi.com.cn）
- 学科评估：教育部学位中心第四轮学科评估（2017）完整公开数据，共 5112 条记录、463 所高校、95 个一级学科，A+ 至 C- 九档；由 [scripts/build_eval_data.py](scripts/build_eval_data.py) 与 [scripts/build_eval_mapping.py](scripts/build_eval_mapping.py) 生成 [src/data/eval4th.js](src/data/eval4th.js)、[src/data/evalMapping.js](src/data/evalMapping.js)（131/137 所院校已映射，未收录的院校页面会明确提示）
- 院校复试线：研招网各校复试线由招生单位以公告形式发布、无结构化公开数据集，[src/data/retest.js](src/data/retest.js) 覆盖全部 137 所院校 × 全部参评学科（3080 个专业）× 5 年（2021-2025）示例数据，分数按「门类国家线 + 院校层次 + 学科等级 + 热门度」锚定生成（由 [scripts/build_retest_data.py](scripts/build_retest_data.py) 生成，懒加载），院校详情页附研招网分数线专题与搜索入口，接入真实数据源时直接替换该文件即可
- 报录比：[src/data/ratios.js](src/data/ratios.js) 覆盖全部 137 所院校 × 优势学科/热门专业 × 3 年（2023-2025）示例数据（由 [scripts/build_ratios_data.py](scripts/build_ratios_data.py) 生成），页面均有醒目提示
- 报考信息请务必以研招网及各高校研招网官方发布为准
