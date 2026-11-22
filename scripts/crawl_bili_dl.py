"""Bilibili Deep Learning Course Extractor for BV1YCh462Emp and its ugc_season."""

import json
import os
import sys
import time
import urllib.error
import urllib.request

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.bilibili.com/",
}

PRIMARY_BVID = "BV1YCh462Emp"
OFFICIAL_SITE = "https://introtodeeplearning.com"

# Categorized Deep Learning courses curated from the 211-video ugc_season
CATEGORY_RULES = [
    (
        "core",
        "核心主干课 (Core Deep Learning)",
        {
            "BV1YCh462Emp": ("MIT", "原声/中英字幕", "MIT 6.S191 (2026) 深度学习导论 — 主链接"),
            "BV1pPap6DE4m": ("MIT", "中配版", "MIT 6.S191 (2026) 深度学习导论中配版"),
            "BV1AsBYBfE3R": ("MIT", "原声/中英字幕", "MIT 6.S191 (2025) 深度学习导论往期经典版"),
            "BV1WmVpzdEQv": ("DeepLearning.AI", "中英字幕", "吴恩达深度学习专项 1/5：神经网络与深度学习"),
            "BV1DLJ6zAEmu": ("DeepLearning.AI", "中英字幕", "吴恩达深度学习专项 2/5：改善深层神经网络"),
            "BV1RMjhzKEcS": ("DeepLearning.AI", "中英字幕", "吴恩达深度学习专项 3/5：结构化机器学习项目"),
            "BV1nqV2zDEhE": ("DeepLearning.AI", "中英字幕", "吴恩达深度学习专项 4/5：卷积神经网络"),
            "BV1ngjEzjERa": ("DeepLearning.AI", "中英字幕", "吴恩达深度学习专项 5/5：序列模型"),
            "BV1rJnBz1EUy": ("多伦多大学 / Coursera", "中英字幕", "图灵奖/诺奖得主 Geoffrey Hinton 神经网络经典课程"),
            "BV1NHui6TEsc": ("多伦多大学", "中英字幕", "UofT Applied Deep Learning (Winter 2026) 应用深度学习"),
            "BV137EF6iE2M": ("前沿专题", "中英字幕", "从第一性原理出发理解深度网络 (2021)"),
        },
    ),
    (
        "math",
        "数学与理论基础 (Math & Theory for DL)",
        {
            "BV1DBhR69ERy": ("芝加哥大学", "中英字幕", "深度学习数学精讲 Minicourse Mathematics of Deep Learning"),
            "BV1e4ZWBNEwD": ("MIT", "中英字幕", "MIT 18.065 线性代数与机器学习（Gilbert Strang）"),
            "BV1876KBiEBa": ("MIT", "中英字幕", "MIT 18.S096 矩阵微积分在机器学习及其扩展中的应用"),
            "BV116VrzVEgk": ("DeepLearning.AI", "中英字幕", "机器学习与数据科学数学专项 1/3：线性代数"),
            "BV1koVmzdEhB": ("DeepLearning.AI", "中英字幕", "机器学习与数据科学数学专项 2/3：微积分"),
            "BV1T1VizvEmp": ("DeepLearning.AI", "中英字幕", "机器学习与数据科学数学专项 3/3：概率论与统计"),
            "BV1sgtw6HENq": ("MIT", "中英字幕", "MIT 9.520 统计学习理论及其应用"),
            "BV18BQRBiE8i": ("芝加哥大学", "中英字幕", "STAT27700 机器学习数学基础 (Fall 2019)"),
            "BV1rhGe6AEne": ("CMU", "中英字幕", "CMU 10-606 机器学习的数学基础"),
        },
    ),
    (
        "systems",
        "深度学习系统、框架与底层算力 (DL Systems, Frameworks & GPU)",
        {
            "BV1nrsXzaEBb": ("CMU", "中英字幕", "CMU 10-714 深度学习系统：算法与实现 (Needle框架从零搭建)"),
            "BV1BJjuzEEtQ": ("DeepLearning.AI", "中英字幕", "TensorFlow 深度学习系统课程 1/4"),
            "BV1UZ7UzUE27": ("DeepLearning.AI", "中英字幕", "TensorFlow 深度学习系统课程 2/4"),
            "BV1MA7Kz4EWY": ("DeepLearning.AI", "中英字幕", "TensorFlow 深度学习系统课程 3/4"),
            "BV1jD7rz3EpL": ("DeepLearning.AI", "中英字幕", "TensorFlow 深度学习系统课程 4/4"),
            "BV1haTSzFEUz": ("DeepLearning.AI", "中英字幕", "TensorFlow 高阶开发技术与模型优化 1/4"),
            "BV1VXTrzCE9F": ("DeepLearning.AI", "中英字幕", "TensorFlow 高阶开发技术与模型优化 2/4"),
            "BV1CyTizCEH8": ("DeepLearning.AI", "中英字幕", "TensorFlow 高阶开发技术与模型优化 3/4"),
            "BV16AT3zvEUz": ("DeepLearning.AI", "中英字幕", "TensorFlow 高阶开发技术与模型优化 4/4"),
            "BV14yKn6sEBT": ("PyTorch Foundation", "中英字幕", "PyTorch Conference Europe 2026 前沿技术大会"),
            "BV1hXcRzbEEJ": ("开源工程", "中英字幕", "PyTensor 计算图深度解析与自动微分"),
            "BV1icVJ6nEQi": ("GPU 算子优化", "中英字幕", "高性能 AI 计算核心三部曲：CUDA、Triton 到 FlashAttention"),
            "BV1bTA6zDETU": ("GPU Mode", "中英字幕", "GPU Mode / CUDA Mode 深度学习算子优化全系列"),
            "BV1QRXNBvEns": ("并行计算", "中英字幕", "CUDA GPU 并行编程实战（软硬件协同）"),
            "BV1AmFmzdEtq": ("系统架构", "中英字幕", "机器学习的硬件与系统架构"),
        },
    ),
    (
        "cv_gen_nlp",
        "深度生成模型、计算机视觉与 NLP (GenAI, CV & NLP)",
        {
            "BV1fyv8BqE7g": ("斯坦福大学", "原声/中英字幕", "Stanford CS231n (2025) 计算机视觉的深度学习"),
            "BV1RLp76vEZu": ("斯坦福大学", "中配版", "Stanford CS231n (2025) 计算机视觉的深度学习中配版"),
            "BV1dFCCBWEMu": ("斯坦福大学", "中英字幕", "Stanford CS236 (2023) 深度生成模型（VAE/GAN/Diffusion）"),
            "BV1cinvzMEEj": ("MIT", "中英字幕", "MIT 6.S184 流匹配与扩散模型（Flow Matching & Diffusion）"),
            "BV1NTmDBqEYD": ("MIT", "中英字幕", "MIT 6.S184 流匹配与扩散模型（镜像版本）"),
            "BV132hP6jEW6": ("多伦多大学", "中英字幕", "多伦多大学：深度生成式 AI（Deep GenAI Course）"),
            "BV14jFZzoE3T": ("MIT / 何恺明", "中英字幕", "何恺明讲座：端到端生成模型前沿"),
            "BV1Eg37zfEBU": ("斯坦福大学", "中英字幕", "Stanford CS224n 自然语言处理（全18集）"),
            "BV1z3NczaEwf": ("MIT", "中英字幕", "MIT 高级自然语言处理 Advanced NLP"),
            "BV1eS9pBdESP": ("CMU", "中英字幕", "CMU Advanced NLP (Fall 2025) 高级自然语言处理"),
            "BV1XrEUzWEP1": ("DeepLearning.AI", "中英字幕", "自然语言处理专项 1/4：分类与向量空间"),
            "BV1mT7JzcEQ3": ("DeepLearning.AI", "中英字幕", "自然语言处理专项 2/4：概率模型"),
            "BV1Uc7Sz2Ewh": ("DeepLearning.AI", "中英字幕", "自然语言处理专项 3/4：序列模型"),
            "BV11w7mzMESk": ("DeepLearning.AI", "中英字幕", "自然语言处理专项 4/4：注意力机制模型"),
        },
    ),
    (
        "llm_rl",
        "Transformer、大语言模型底层与深度强化学习 (Transformers, LLMs & Deep RL)",
        {
            "BV19Py7BUEf5": ("斯坦福大学", "中英字幕", "Stanford CS25 (2023) Transformer 专题研讨会"),
            "BV154qTBBEbx": ("斯坦福大学", "中英字幕", "Stanford CS336 (Spring 2025) 从零开始构建大语言模型"),
            "BV1zmnx6ZEcn": ("Andrej Karpathy", "中英字幕", "Zero to Hero：micrograd 反向传播 + 从零手写 GPT"),
            "BV1H4pFz5EAN": ("Vizuara", "中英字幕", "从零开始构建大语言模型系统长课"),
            "BV1ykC9BvEPh": ("Python 实战", "中英字幕", "从零开始用 Python 搭建大语言模型"),
            "BV1CKV86oEkW": ("架构解析", "中英字幕", "主流大语言模型架构深度对比"),
            "BV1LidKBEEFT": ("阿尔伯塔大学", "中英字幕", "大模型推理的数学原理 (2025)"),
            "BV16TXpBhEd6": ("CMU", "中英字幕", "CMU 大语言模型推理算法 (2025)"),
            "BV1e66pBRE6C": ("斯坦福大学", "中英字幕", "Stanford CS234 (2024) 强化学习"),
            "BV1XykZBdEAZ": ("普林斯顿大学", "中英字幕", "Princeton ECE524 (2024) 强化学习基础"),
            "BV1XGe76oEnX": ("机器人学习", "中英字幕", "机器人深度强化学习：连续控制、步态生成与仿真"),
            "BV1G9Nw6kE5r": ("蒙特利尔大学", "中英字幕", "机器人基础模型与深度强化学习扩展（Scaling DeepRL）"),
            "BV1WBYL6MEQT": ("具身智能", "中英字幕", "物理 AI 基础：VLM、VLA 与 WAM 的数学原理"),
        },
    ),
]

ENRICH_BVIDS = [
    "BV1YCh462Emp",
    "BV1DBhR69ERy",
    "BV1NHui6TEsc",
    "BV1nrsXzaEBb",
    "BV1fyv8BqE7g",
    "BV1dFCCBWEMu",
    "BV1cinvzMEEj",
    "BV132hP6jEW6",
    "BV154qTBBEbx",
    "BV1zmnx6ZEcn",
    "BV19Py7BUEf5",
    "BV1rJnBz1EUy",
    "BV1e66pBRE6C",
    "BV1e4ZWBNEwD",
    "BV1WmVpzdEQv",
    "BV1AsBYBfE3R",
]


def fetch_json(url: str) -> dict:
    """Fetch and parse a JSON payload from Bilibili's public Web API."""
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def format_duration(seconds: int) -> str:
    """Format duration in seconds into compact human-readable hours/minutes/seconds."""
    seconds = max(0, int(seconds or 0))
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)
    if hours > 0:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m {secs:02d}s"


def extract_primary_course(bvid: str) -> tuple[dict, list]:
    """Fetch primary course metadata, tags, comments, and ugc_season episodes."""
    view_res = fetch_json(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}")
    data = view_res.get("data") or {}
    if not data:
        raise RuntimeError(f"Empty response for {bvid}: {view_res}")

    tags_res = fetch_json(f"https://api.bilibili.com/x/tag/archive/tags?bvid={bvid}")
    tags = [t.get("tag_name") for t in (tags_res.get("data") or []) if t.get("tag_name")]

    comments = []
    try:
        aid = data.get("aid")
        reply_res = fetch_json(f"https://api.bilibili.com/x/v2/reply?type=1&oid={aid}&sort=1&ps=20")
        rdata = reply_res.get("data") or {}
        top = (rdata.get("upper") or {}).get("top")
        if top:
            comments.append({"is_top": True, "user": top["member"]["uname"], "text": top["content"]["message"]})
        for r in rdata.get("replies") or []:
            comments.append({"is_top": False, "user": r["member"]["uname"], "text": r["content"]["message"]})
    except Exception:
        pass

    pages = [
        {
            "page": p.get("page"),
            "part": p.get("part"),
            "duration_sec": p.get("duration", 0),
            "duration_fmt": format_duration(p.get("duration", 0)),
            "cid": p.get("cid"),
            "url": f"https://www.bilibili.com/video/{bvid}/?p={p.get('page')}",
        }
        for p in (data.get("pages") or [])
    ]

    primary = {
        "bvid": data.get("bvid"),
        "aid": data.get("aid"),
        "cid": data.get("cid"),
        "title": data.get("title"),
        "owner": (data.get("owner") or {}).get("name"),
        "owner_mid": (data.get("owner") or {}).get("mid"),
        "pubdate": data.get("pubdate"),
        "pubdate_iso": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.get("pubdate", 0))),
        "desc": data.get("desc"),
        "official_site": OFFICIAL_SITE,
        "duration_sec": data.get("duration", 0),
        "duration_fmt": format_duration(data.get("duration", 0)),
        "stat": data.get("stat") or {},
        "tags": tags,
        "comments": comments,
        "pages": pages,
        "season_title": ((data.get("ugc_season") or {}).get("title") or "").strip(),
    }

    season_episodes = []
    for sec in (data.get("ugc_season") or {}).get("sections") or []:
        for ep in sec.get("episodes") or []:
            arc = ep.get("arc") or {}
            season_episodes.append(
                {
                    "bvid": ep.get("bvid"),
                    "aid": ep.get("aid"),
                    "title": ep.get("title"),
                    "duration_sec": arc.get("duration", 0),
                    "duration_fmt": format_duration(arc.get("duration", 0)),
                    "url": f"https://www.bilibili.com/video/{ep.get('bvid')}/",
                }
            )

    return primary, season_episodes


def enrich_course_details(bvid: str) -> dict:
    """Fetch extended details (pages count, desc, stat) for a single BV episode."""
    try:
        res = fetch_json(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}")
        d = res.get("data") or {}
        if not d:
            return {}
        return {
            "pages_count": len(d.get("pages") or []),
            "desc": (d.get("desc") or "").strip(),
            "pubdate_iso": time.strftime("%Y-%m-%d", time.localtime(d.get("pubdate", 0))),
            "stat": {
                "view": (d.get("stat") or {}).get("view", 0),
                "favorite": (d.get("stat") or {}).get("favorite", 0),
                "like": (d.get("stat") or {}).get("like", 0),
            },
        }
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
        return {}


def build_curated_courses(season_episodes: list) -> list:
    """Filter season episodes into categorized Deep Learning courses and enrich flagships."""
    ep_map = {ep["bvid"]: ep for ep in season_episodes if ep.get("bvid")}
    bv_lookup = {}
    for cat_id, cat_name, items in CATEGORY_RULES:
        for bv, (org, lang, note) in items.items():
            bv_lookup[bv] = (cat_id, cat_name, org, lang, note)

    curated = []
    seen = set()
    # Preserve ordered structure by category rules first, then check season metadata
    for cat_id, cat_name, items in CATEGORY_RULES:
        for bv, (org, lang, note) in items.items():
            if bv in seen:
                continue
            seen.add(bv)
            ep = ep_map.get(bv)
            if not ep:
                continue
            entry = {
                "bvid": bv,
                "title": ep["title"],
                "category_id": cat_id,
                "category_name": cat_name,
                "institution": org,
                "language": lang,
                "summary": note,
                "duration_sec": ep["duration_sec"],
                "duration_hours": round(ep["duration_sec"] / 3600, 2),
                "duration_fmt": ep["duration_fmt"],
                "url": ep["url"],
            }
            if bv in ENRICH_BVIDS:
                time.sleep(0.25)
                extra = enrich_course_details(bv)
                entry.update(extra)
            curated.append(entry)
    return curated


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "bili_dl_courses.json",
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    print(f"Fetching primary course {PRIMARY_BVID}...")
    primary, season_episodes = extract_primary_course(PRIMARY_BVID)
    print(f"Primary pages: {len(primary['pages'])}, Total season episodes: {len(season_episodes)}")

    print("Filtering and enriching Deep Learning courses...")
    curated = build_curated_courses(season_episodes)
    print(f"Curated Deep Learning courses: {len(curated)}")

    category_stats = {}
    for c in curated:
        cid = c["category_id"]
        if cid not in category_stats:
            category_stats[cid] = {"name": c["category_name"], "count": 0, "total_hours": 0.0}
        category_stats[cid]["count"] += 1
        category_stats[cid]["total_hours"] = round(
            category_stats[cid]["total_hours"] + c["duration_hours"], 2
        )

    payload = {
        "extracted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "extraction_method": "Bilibili Public Web API (x/web-interface/view, x/tag/archive/tags) + MIT 6.S191 Official Syllabus",
        "primary_course": primary,
        "season_total_episodes": len(season_episodes),
        "dl_curated_count": len(curated),
        "category_stats": category_stats,
        "dl_courses": curated,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Saved JSON to {out_path}")


if __name__ == "__main__":
    main()
