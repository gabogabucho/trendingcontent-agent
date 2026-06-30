# trendingcontent-agent

> Research trending topics and generate ready-to-post social media content — as a Hermes/OpenClaw skill.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**trendingcontent** is a two-phase AI agent skill:

1. **Research phase** — scrapes Reddit, X/Twitter, YouTube, TikTok, HackerNews, Bluesky and Brave Search to surface the most engaging content about your topic over a configurable time window (7, 15, 30, or up to 90 days).
2. **Content generation phase** — uses the research findings to generate platform-specific social media copy: Twitter/X threads, LinkedIn posts, and Instagram captions.

Built on top of [last30days](https://github.com/mvanhorn/last30days-skill) by [@mvanhorn](https://github.com/mvanhorn), extended with:
- Variable time windows (not just 30 days)
- Multi-platform content generation (Twitter, LinkedIn, Instagram)
- Tone control (professional, casual, educational, viral)
- Multilingual output (English, Spanish, Portuguese)
- Hermes/OpenClaw skill standard compatibility

---

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/gabogabucho/trendingcontent-agent.git
cd trendingcontent-agent
pip install -r requirements.txt
```

### 2. Configure API keys

```bash
export SCRAPECREATORS_API_KEY="your_key"   # required
export BRAVE_API_KEY="your_key"            # optional but recommended
```

Or add them to your `.env` file.

Get a ScrapeCreators API key at [scrapecreators.com](https://scrapecreators.com).
Get a Brave Search API key at [brave.com/search/api](https://brave.com/search/api/).

### 3. Run

```bash
python scripts/trendingcontent.py "artificial intelligence" --days=7 --platform=all
```

---

## Usage

```
python scripts/trendingcontent.py <topic> [options]

Options:
  --days=N           Time window: 7-90 days (default: 30)
  --platform         twitter | linkedin | instagram | all (default: all)
  --tone             professional | casual | educational | viral (default: professional)
  --lang             en | es | pt (default: en)
  --sources=S1,S2    Only use these sources (reddit,twitter,youtube,tiktok,bluesky,hackernews,brave)
  --disable=S1,S2    Disable specific sources
  --list-sources     Show all available sources
  --quick            Fewer sources, faster
  --deep             More sources, thorough
  --research-only    Output research only, skip content generation
  --tweetclaw-export Local TweetClaw JSON or JSONL export to add as X/Twitter source evidence
```

### Examples

```bash
# AI trends last 7 days → all platforms
python scripts/trendingcontent.py "artificial intelligence" --days=7

# Web3 → LinkedIn post in Spanish, professional tone
python scripts/trendingcontent.py "web3" --days=15 --platform=linkedin --lang=es

# Climate tech → viral Twitter thread
python scripts/trendingcontent.py "climate tech" --days=30 --platform=twitter --tone=viral

# Niche topic — only Reddit and YouTube (no HackerNews)
python scripts/trendingcontent.py "sourdough bread" --sources=reddit,youtube,brave

# Disable sources that don't fit your topic
python scripts/trendingcontent.py "fintech" --disable=hackernews,tiktok

# See all available sources
python scripts/trendingcontent.py --list-sources

# Research only, no content
python scripts/trendingcontent.py "LLMs" --days=14 --research-only

# Add reviewed X/Twitter evidence from a local TweetClaw export
python scripts/trendingcontent.py "AI developer tools" \
  --platform=twitter \
  --tweetclaw-export ./tweetclaw-export.jsonl
```

TweetClaw exports are treated as local source context only. They can strengthen
the research summary with public X/Twitter posts, URLs, handles, dates, and
engagement signals, while trendingcontent still owns the brief and final copy.

---

## As a Hermes/OpenClaw skill

This repository follows the [Hermes skill standard](https://github.com/NousResearch/hermes-agent).
To install as a skill:

```bash
# Copy to your Hermes skills directory
cp -r . /path/to/hermes-agent/skills/social-media/trendingcontent/

# Add API keys to your Hermes .env
echo "SCRAPECREATORS_API_KEY=your_key" >> ~/.hermes/.env
echo "BRAVE_API_KEY=your_key" >> ~/.hermes/.env
```

The agent will automatically discover the skill via `SKILL.md`.

---

## Sources

| Source | Notes |
|--------|-------|
| Reddit | Top posts by engagement |
| X / Twitter | Trending tweets |
| YouTube | Video titles + transcripts |
| TikTok | Trending videos |
| Bluesky | Recent posts |
| HackerNews | Top stories (no key needed) |
| Brave Search | Web results (optional) |

---

## Output structure

```
═══════════════════════════════════════════════
TRENDINGCONTENT — CONTENT GENERATION BRIEF
═══════════════════════════════════════════════
Topic:     artificial intelligence
Period:    Last 7 days
Language:  English
Tone:      Professional
Platforms: Twitter, LinkedIn, Instagram

───────────────────────────────────────────────
RESEARCH SUMMARY
───────────────────────────────────────────────
[ranked trending content with titles, scores, URLs]

───────────────────────────────────────────────
CONTENT INSTRUCTIONS
───────────────────────────────────────────────
[platform-specific format specs + tone guidance]
```

---

## Requirements

- Python 3.9+
- `yt-dlp` — YouTube transcript extraction
- `requests` — HTTP calls
- ScrapeCreators API key (required)
- Brave Search API key (optional)

---

## Credits

- Original research engine: [last30days-skill](https://github.com/mvanhorn/last30days-skill) by [@mvanhorn](https://github.com/mvanhorn) — MIT License
- Social media generation layer & Hermes skill packaging: [@gabogabucho](https://twitter.com/gabogabucho)

---

## License

MIT License — see [LICENSE](LICENSE) for details.
