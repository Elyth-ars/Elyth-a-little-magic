# Elyth-"a little magic"

MIT 6.S191 (2026) 深度学习导论交互学习台与 B 站同合集（211 部视频 → 精选 62 门深度学习课程）课程全景总结。

- **在线访问地址（GitHub Pages）**：https://elyth-ars.github.io/Elyth-a-little-magic/
- **主视频来源**：[`BV1YCh462Emp?p=2`](https://www.bilibili.com/video/BV1YCh462Emp/?p=2) · MIT 官方主页：[introtodeeplearning.com](https://introtodeeplearning.com)

## 目录结构

- [`index.html`](./index.html)：零依赖单文件交互式学习网页（支持在线浏览，也可直接下载/本地 `file://` 离线打开）
  - MIT 6.S191 (2026) 全 9 讲精讲与 3 个 Software Labs 对照表（默认聚焦 P2，本地保存进度与笔记）
  - 三大深度学习原理交互实验室：Self-Attention 缩放点积沙盒、2D 损失地形优化器对比与激活函数导数探测、2D 卷积核感受野特征提取器
  - 10 题全课程核心概念自测
  - 62 门合集深度学习课程检索库、四阶段路线图与 `.md` 学习报告导出
- [`MIT_6S191_深度学习课程总结文档.md`](./MIT_6S191_深度学习课程总结文档.md)：完整版课程总结文档（全 9 讲拆解、核心公式速查表、62 门精选课程目录与 14–18 周学习路线）
- [`scripts/crawl_bili_dl.py`](./scripts/crawl_bili_dl.py)：B 站公开 API 课程信息采集脚本
- [`data/bili_dl_courses.json`](./data/bili_dl_courses.json)：采集并分类后的结构化课程数据
