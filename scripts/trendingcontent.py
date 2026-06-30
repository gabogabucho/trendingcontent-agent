#!/usr/bin/env python3
"""
trendingcontent — Trending research + social media content generation.

Based on last30days by @mvanhorn (https://github.com/mvanhorn/last30days-skill)
Enhanced by @gabogabucho (https://github.com/gabogabucho/trendingcontent-agent)

MIT License — see LICENSE file for details.

Usage:
    python trendingcontent.py <topic> [options]

Options:
    --days=N            Time window in days (default: 30, min: 7, max: 90)
    --platform=PLAT     Content output: twitter|linkedin|instagram|all (default: all)
    --tone=TONE         Content tone: professional|casual|educational|viral (default: professional)
    --lang=LANG         Output language: en|es|pt (default: en)
    --sources=S1,S2     Only use these sources (comma-separated)
                        Available: reddit,twitter,youtube,tiktok,bluesky,hackernews,brave
    --disable=S1,S2     Disable specific sources (comma-separated)
    --list-sources      Show all available sources and exit
    --quick             Quick mode (fewer sources, faster)
    --deep              Deep mode (more sources, slower)
    --research-only     Only output research, skip content generation
    --tweetclaw-export  Optional TweetClaw JSON or JSONL export to include as local X evidence
    --help              Show this help message
"""

from __future__ import annotations

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LIB_DIR = SCRIPT_DIR / "lib"
LAST30_SCRIPT = SCRIPT_DIR / "last30days.py"

sys.path.insert(0, str(LIB_DIR))

# All supported sources and their last30days CLI flags
ALL_SOURCES = {
    "reddit":     "--reddit",
    "twitter":    "--twitter",
    "youtube":    "--youtube",
    "tiktok":     "--tiktok",
    "bluesky":    "--bluesky",
    "hackernews": "--hackernews",
    "brave":      "--brave",
}

# Sources enabled by default (all of them; last30days handles missing keys gracefully)
DEFAULT_SOURCES = list(ALL_SOURCES.keys())

# ─── Argument parsing ─────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="trendingcontent — trending research + social media content generation",
        add_help=False
    )
    parser.add_argument("topic", nargs="?", help="Topic to research")
    parser.add_argument("--days", type=int, default=30, metavar="N",
                        help="Time window in days (7-90, default: 30)")
    parser.add_argument("--platform", default="all",
                        choices=["twitter", "linkedin", "instagram", "all"],
                        help="Target social platform (default: all)")
    parser.add_argument("--tone", default="professional",
                        choices=["professional", "casual", "educational", "viral"],
                        help="Content tone (default: professional)")
    parser.add_argument("--lang", default="en",
                        choices=["en", "es", "pt"],
                        help="Output language (default: en)")
    parser.add_argument("--sources", default=None, metavar="S1,S2",
                        help="Only use these sources (comma-separated). "
                             "Available: " + ", ".join(ALL_SOURCES.keys()))
    parser.add_argument("--disable", default=None, metavar="S1,S2",
                        help="Disable specific sources (comma-separated)")
    parser.add_argument("--list-sources", action="store_true",
                        help="Show all available sources and exit")
    parser.add_argument("--quick", action="store_true",
                        help="Quick mode — fewer sources, faster results")
    parser.add_argument("--deep", action="store_true",
                        help="Deep mode — more sources, slower but thorough")
    parser.add_argument("--research-only", action="store_true",
                        help="Output only research data, skip content generation")
    parser.add_argument("--tweetclaw-export", default=None, metavar="PATH",
                        help="Include local TweetClaw JSON or JSONL exports as reviewed X/Twitter source evidence")
    parser.add_argument("--tweetclaw-limit", type=int, default=12, metavar="N",
                        help="Maximum TweetClaw rows to include in the research summary (default: 12)")
    parser.add_argument("--help", "-h", action="store_true",
                        help="Show help message")
    return parser.parse_args()


def list_sources():
    print("Available research sources:")
    print()
    descriptions = {
        "reddit":     "Reddit posts — broad community discussion, requires ScrapeCreators",
        "twitter":    "X/Twitter tweets — real-time reactions, requires ScrapeCreators",
        "youtube":    "YouTube videos + transcripts — requires ScrapeCreators + yt-dlp",
        "tiktok":     "TikTok videos — trending short-form content, requires ScrapeCreators",
        "bluesky":    "Bluesky posts — decentralized social, requires ScrapeCreators",
        "hackernews": "Hacker News — tech-focused, very specific (public API, no key needed)",
        "brave":      "Brave Search — general web results (optional, requires BRAVE_API_KEY)",
    }
    for name, desc in descriptions.items():
        default_mark = " [default]" if name in DEFAULT_SOURCES else ""
        print(f"  {name:<12} {desc}{default_mark}")
    print()
    print("Examples:")
    print("  --sources=reddit,youtube,brave      # only these three")
    print("  --disable=hackernews,tiktok         # all except these two")


def resolve_sources(sources_arg: str | None, disable_arg: str | None) -> list:
    """Return the list of sources to use based on --sources and --disable flags."""
    if sources_arg:
        requested = [s.strip().lower() for s in sources_arg.split(",") if s.strip()]
        unknown = [s for s in requested if s not in ALL_SOURCES]
        if unknown:
            print(f"[WARNING] Unknown sources ignored: {', '.join(unknown)}", file=sys.stderr)
        active = [s for s in requested if s in ALL_SOURCES]
    else:
        active = list(DEFAULT_SOURCES)

    if disable_arg:
        disabled = [s.strip().lower() for s in disable_arg.split(",") if s.strip()]
        unknown = [s for s in disabled if s not in ALL_SOURCES]
        if unknown:
            print(f"[WARNING] Unknown --disable sources ignored: {', '.join(unknown)}", file=sys.stderr)
        active = [s for s in active if s not in disabled]

    if not active:
        print("[WARNING] No sources selected — falling back to defaults.", file=sys.stderr)
        active = list(DEFAULT_SOURCES)

    return active


def validate_days(days: int) -> int:
    if days < 7:
        print(f"[WARNING] --days={days} is below minimum (7). Using 7.", file=sys.stderr)
        return 7
    if days > 90:
        print(f"[WARNING] --days={days} exceeds maximum (90). Using 90.", file=sys.stderr)
        return 90
    return days


# ─── Research phase ───────────────────────────────────────────────────────────

def run_research(
    topic: str,
    days: int,
    sources: list | None = None,
    quick: bool = False,
    deep: bool = False,
) -> dict:
    """
    Invoke the last30days research engine and return structured results.
    """
    args = [sys.executable, str(LAST30_SCRIPT), topic, f"--days={days}"]
    if quick:
        args.append("--quick")
    elif deep:
        args.append("--deep")

    # Pass source flags if last30days supports them (graceful — unknown flags are ignored)
    if sources is not None:
        all_source_names = list(ALL_SOURCES.keys())
        disabled = [s for s in all_source_names if s not in sources]
        for src in disabled:
            flag = ALL_SOURCES[src].replace("--", "--no-")
            args.append(flag)

    active_sources = ", ".join(sources) if sources else "all"
    print(
        f"\n[trendingcontent] Researching: '{topic}' | last {days} days | sources: {active_sources}\n",
        file=sys.stderr,
    )

    try:
        result = subprocess.run(args, capture_output=True, text=True, cwd=str(SCRIPT_DIR))
        if result.returncode != 0:
            print(f"[ERROR] Research engine failed:\n{result.stderr}", file=sys.stderr)
            return {"error": result.stderr, "raw": ""}
        return {"raw": result.stdout, "error": None}
    except Exception as e:
        return {"error": str(e), "raw": ""}


def load_tweetclaw_export(export_path: str) -> list[dict]:
    """Load TweetClaw JSON or JSONL exports without requiring a strict schema."""
    path = Path(export_path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"TweetClaw export not found: {path}")

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []

    if path.suffix.lower() == ".jsonl":
        rows = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL on line {line_number}: {exc}") from exc
        return [row for row in rows if isinstance(row, dict)]

    payload = json.loads(text)
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("tweets", "items", "results", "data", "records"):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
        return [payload]
    return []


def pick_first(row: dict, keys: tuple[str, ...], default: str = "") -> str:
    for key in keys:
        value = row.get(key)
        if value is None:
            continue
        if isinstance(value, str):
            value = value.strip()
            if value:
                return value
        elif isinstance(value, (int, float)):
            return str(value)
    return default


def format_tweetclaw_export(export_path: str, limit: int) -> str:
    rows = load_tweetclaw_export(export_path)
    if not rows:
        return ""

    lines = [
        "TWEETCLAW LOCAL X/TWITTER EVIDENCE",
        f"Source file: {Path(export_path).expanduser()}",
        "Use these rows as source context only. Do not treat TweetClaw as the publishing authority.",
        "",
    ]
    max_rows = max(1, limit)

    for index, row in enumerate(rows[:max_rows], start=1):
        text = pick_first(row, ("text", "full_text", "content", "body", "description"))
        url = pick_first(row, ("status_url", "tweet_url", "url", "permalink"))
        author = pick_first(row, ("author_handle", "handle", "username", "screen_name", "author", "user"))
        created = pick_first(row, ("created_at", "createdAt", "date", "timestamp"))
        likes = pick_first(row, ("likes", "like_count", "favorite_count"))
        reposts = pick_first(row, ("reposts", "retweets", "retweet_count"))
        replies = pick_first(row, ("replies", "reply_count"))
        metrics = ", ".join(
            part for part in (
                f"likes={likes}" if likes else "",
                f"reposts={reposts}" if reposts else "",
                f"replies={replies}" if replies else "",
            ) if part
        )

        lines.append(f"{index}. {text[:500] if text else '(no text)'}")
        if author:
            lines.append(f"   author: {author}")
        if created:
            lines.append(f"   date: {created}")
        if url:
            lines.append(f"   url: {url}")
        if metrics:
            lines.append(f"   metrics: {metrics}")

    if len(rows) > max_rows:
        lines.append(f"... {len(rows) - max_rows} additional TweetClaw rows omitted by --tweetclaw-limit.")

    return "\n".join(lines)


def append_tweetclaw_research(research_text: str, export_path: str | None, limit: int) -> str:
    if not export_path:
        return research_text
    local_evidence = format_tweetclaw_export(export_path, limit)
    if not local_evidence:
        return research_text
    return f"{research_text.strip()}\n\n{local_evidence}\n"


# ─── Content generation ───────────────────────────────────────────────────────

PLATFORM_SPECS = {
    "twitter": {
        "en": (
            "Generate a Twitter/X thread (6-8 tweets). Format:\n"
            "- Tweet 1 (hook): attention-grabbing opening that makes people want to read more. Max 280 chars.\n"
            "- Tweets 2-6: one key insight per tweet, with data/stats if available. Start each with a number (2/, 3/, etc.).\n"
            "- Tweet 7 (insight): the most surprising or counterintuitive finding.\n"
            "- Tweet 8 (CTA): call to action — follow, retweet, reply, or share.\n"
            "Use line breaks for readability. No hashtag overload — max 2-3 per tweet.\n"
        ),
        "es": (
            "Genera un hilo de Twitter/X (6-8 tweets). Formato:\n"
            "- Tweet 1 (gancho): apertura que capture la atención y genere curiosidad. Máx 280 caracteres.\n"
            "- Tweets 2-6: un insight clave por tweet, con datos/estadísticas si hay. Empieza cada uno con número (2/, 3/, etc.).\n"
            "- Tweet 7 (dato sorprendente): el hallazgo más inesperado o contraintuitivo.\n"
            "- Tweet 8 (CTA): llamada a la acción — seguir, retweetear, responder o compartir.\n"
            "Usa saltos de línea. No abuses de hashtags — máx 2-3 por tweet.\n"
        ),
        "pt": (
            "Gere um thread do Twitter/X (6-8 tweets). Formato:\n"
            "- Tweet 1 (gancho): abertura que capture atenção. Máx 280 caracteres.\n"
            "- Tweets 2-6: um insight por tweet, com dados se disponível. Comece com número (2/, 3/, etc.).\n"
            "- Tweet 7 (insight): a descoberta mais surpreendente.\n"
            "- Tweet 8 (CTA): chamada para ação.\n"
            "Máx 2-3 hashtags por tweet.\n"
        ),
    },
    "linkedin": {
        "en": (
            "Generate a LinkedIn post (max 1300 characters). Structure:\n"
            "- Opening line: bold hook (no fluff, no 'I am excited to share')\n"
            "- 3-4 short paragraphs with key insights and data\n"
            "- One personal or professional takeaway\n"
            "- Closing question or CTA to drive comments\n"
            "- 3-5 relevant hashtags at the end\n"
            "Tone: authoritative but approachable. No bullet points — use short paragraphs.\n"
        ),
        "es": (
            "Genera un post de LinkedIn (máx 1300 caracteres). Estructura:\n"
            "- Primera línea: gancho directo (sin frases vacías)\n"
            "- 3-4 párrafos cortos con insights y datos clave\n"
            "- Una conclusión o aprendizaje personal/profesional\n"
            "- Pregunta o CTA al cierre para generar comentarios\n"
            "- 3-5 hashtags relevantes al final\n"
            "Tono: con autoridad pero cercano. Sin bullet points — párrafos cortos.\n"
        ),
        "pt": (
            "Gere um post do LinkedIn (máx 1300 caracteres). Estrutura:\n"
            "- Primeira linha: gancho direto\n"
            "- 3-4 parágrafos curtos com insights\n"
            "- Uma conclusão ou aprendizado\n"
            "- Pergunta ou CTA para gerar comentários\n"
            "- 3-5 hashtags relevantes\n"
            "Tom: autoritativo mas acessível. Sem bullet points.\n"
        ),
    },
    "instagram": {
        "en": (
            "Generate an Instagram caption. Structure:\n"
            "- Opening hook (first 2 lines visible before 'more' — make them irresistible)\n"
            "- 3-5 short paragraphs with insights (use emojis sparingly to separate sections)\n"
            "- One strong closing statement or question\n"
            "- Line break, then 15-20 relevant hashtags (mix of niche and broad)\n"
            "Max caption length: 2200 characters. Conversational, visual storytelling tone.\n"
        ),
        "es": (
            "Genera un caption de Instagram. Estructura:\n"
            "- Gancho de apertura (primeras 2 líneas visibles antes del 'más' — que sean irresistibles)\n"
            "- 3-5 párrafos cortos con insights (emojis con moderación para separar secciones)\n"
            "- Cierre fuerte o pregunta\n"
            "- Salto de línea y 15-20 hashtags relevantes (mezcla de nicho y generales)\n"
            "Máx 2200 caracteres. Tono conversacional, narrativo.\n"
        ),
        "pt": (
            "Gere uma legenda do Instagram. Estrutura:\n"
            "- Gancho de abertura (primeiras 2 linhas visíveis antes do 'mais')\n"
            "- 3-5 parágrafos curtos com insights\n"
            "- Fechamento forte ou pergunta\n"
            "- Quebra de linha e 15-20 hashtags relevantes\n"
            "Máx 2200 caracteres. Tom conversacional.\n"
        ),
    },
}

TONE_MODIFIERS = {
    "professional": {
        "en": "Use a professional, data-driven tone. Cite sources and statistics when possible.",
        "es": "Usa un tono profesional y basado en datos. Cita fuentes y estadísticas cuando sea posible.",
        "pt": "Use tom profissional e baseado em dados. Cite fontes e estatísticas quando possível.",
    },
    "casual": {
        "en": "Use a casual, friendly tone — like you are explaining this to a smart friend over coffee.",
        "es": "Usa un tono casual y amigable — como si le explicaras esto a un amigo inteligente tomando un café.",
        "pt": "Use tom casual e amigável — como se estivesse explicando para um amigo inteligente.",
    },
    "educational": {
        "en": "Use a clear, educational tone. Define key terms, explain context, use analogies.",
        "es": "Usa un tono educativo y claro. Define términos clave, explica el contexto, usa analogías.",
        "pt": "Use tom educativo e claro. Defina termos, explique contexto, use analogias.",
    },
    "viral": {
        "en": "Use a bold, contrarian, or surprising angle. Lead with the most unexpected finding. Make people want to share this.",
        "es": "Usa un ángulo audaz, contrario a la intuición o sorprendente. Comienza con el hallazgo más inesperado. Haz que la gente quiera compartirlo.",
        "pt": "Use ângulo ousado ou surpreendente. Comece com a descoberta mais inesperada. Faça as pessoas quererem compartilhar.",
    },
}


def get_platforms(platform: str) -> list:
    if platform == "all":
        return ["twitter", "linkedin", "instagram"]
    return [platform]


def generate_content_instructions(
    research_text: str,
    topic: str,
    days: int,
    platform: str,
    tone: str,
    lang: str,
    sources: list | None = None,
) -> str:
    """
    Build the content generation prompt block that the AI agent will use.
    """
    platforms = get_platforms(platform)
    lang_labels = {"en": "English", "es": "Spanish", "pt": "Portuguese"}
    lang_label = lang_labels.get(lang, "English")

    lines = []
    lines.append("=" * 70)
    lines.append(f"TRENDINGCONTENT — CONTENT GENERATION BRIEF")
    lines.append("=" * 70)
    lines.append(f"Topic:     {topic}")
    lines.append(f"Period:    Last {days} days")
    lines.append(f"Language:  {lang_label}")
    lines.append(f"Tone:      {tone.capitalize()}")
    lines.append(f"Platforms: {', '.join(p.capitalize() for p in platforms)}")
    if sources and set(sources) != set(DEFAULT_SOURCES):
        lines.append(f"Sources:   {', '.join(sources)}")
    lines.append("")
    lines.append("─" * 70)
    lines.append("RESEARCH SUMMARY")
    lines.append("─" * 70)
    lines.append(research_text.strip())
    lines.append("")
    lines.append("─" * 70)
    lines.append("CONTENT INSTRUCTIONS")
    lines.append("─" * 70)
    lines.append("")

    tone_mod = TONE_MODIFIERS.get(tone, TONE_MODIFIERS["professional"]).get(lang, "")
    if tone_mod:
        lines.append(f"Tone guidance: {tone_mod}")
        lines.append("")

    for plat in platforms:
        spec = PLATFORM_SPECS.get(plat, {}).get(lang, PLATFORM_SPECS[plat]["en"])
        lines.append(f"[{plat.upper()}]")
        lines.append(spec)

    lines.append("─" * 70)
    lines.append("Now generate the content for the platform(s) listed above.")
    lines.append("Base it strictly on the research summary provided.")
    lines.append("=" * 70)

    return "\n".join(lines)


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    args = parse_args()

    if args.list_sources:
        list_sources()
        sys.exit(0)

    if args.help or not args.topic:
        print(__doc__)
        sys.exit(0)

    days = validate_days(args.days)
    topic = args.topic
    sources = resolve_sources(args.sources, args.disable)

    # Phase 1: Research
    research = run_research(topic, days, sources=sources, quick=args.quick, deep=args.deep)

    if research.get("error") and not research.get("raw"):
        print(f"[ERROR] Research failed: {research['error']}", file=sys.stderr)
        sys.exit(1)

    research_text = append_tweetclaw_research(
        research_text=research["raw"],
        export_path=args.tweetclaw_export,
        limit=args.tweetclaw_limit,
    )

    if args.research_only:
        print(research_text)
        sys.exit(0)

    # Phase 2: Content generation brief
    brief = generate_content_instructions(
        research_text=research_text,
        topic=topic,
        days=days,
        platform=args.platform,
        tone=args.tone,
        lang=args.lang,
        sources=sources,
    )

    print(brief)


if __name__ == "__main__":
    main()
