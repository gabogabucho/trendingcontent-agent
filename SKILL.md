---
name: trendingcontent
description: Research trending topics across Reddit, X/Twitter, YouTube, TikTok, HackerNews, Bluesky and Brave Search over a configurable time window, then generate ready-to-post social media content — Twitter/X threads, LinkedIn posts, Instagram captions — in English, Spanish, or Portuguese.
version: 1.0.0
author: gabogabucho
license: MIT
platforms: [linux, macos]
prerequisites:
  env_vars: [SCRAPECREATORS_API_KEY]
  commands: [python3, yt-dlp]
metadata:
  hermes:
    tags: [social-media, trending, research, twitter, linkedin, instagram, content-generation, reddit, youtube]
    related_skills: [xitter, duckduckgo-search]
    homepage: https://github.com/gabogabucho/trendingcontent-agent
---

# trendingcontent

Research what's trending on a topic and generate polished social media content based on those findings.

Built on top of [last30days](https://github.com/mvanhorn/last30days-skill) by @mvanhorn.
Social media generation layer and Hermes skill packaging by [@gabogabucho](https://twitter.com/gabogabucho).

## When to use

Use this skill when the user asks to:
- "What's trending about [topic] this week / last 15 days?"
- "Generate a Twitter/X thread about [topic] based on recent trends"
- "Write a LinkedIn post about what's happening with [topic]"
- "Create an Instagram caption about [topic] trends"
- "Research [topic] and generate social media posts"
- "What are people saying about [topic] on Reddit/Twitter/YouTube?"
- "Make me content about [topic] for my social media"

Do NOT use this skill for general web searches without a content generation goal — prefer `duckduckgo-search` or `web_search` for that.

## Setup (one-time)

```bash
pip install yt-dlp requests
```

Verify API keys are set:
```bash
grep SCRAPECREATORS ~/.hermes/.env
grep BRAVE ~/.hermes/.env   # optional but recommended
```

## How to invoke

```bash
python ~/.hermes/skills/social-media/trendingcontent/scripts/trendingcontent.py \
  "<topic>" \
  --days=<N> \
  --platform=<twitter|linkedin|instagram|all> \
  --tone=<professional|casual|educational|viral> \
  --lang=<en|es|pt>
```

### Mapping user intent to parameters

| User says | Parameter |
|-----------|-----------|
| "last week", "this week", "7 days" | `--days=7` |
| "last 2 weeks", "15 days" | `--days=15` |
| "this month", "last 30 days" | `--days=30` (default) |
| "Twitter thread", "hilo" | `--platform=twitter` |
| "LinkedIn post" | `--platform=linkedin` |
| "Instagram caption", "Instagram copy" | `--platform=instagram` |
| "all platforms", no platform specified | `--platform=all` |
| "viral", "que se viralice" | `--tone=viral` |
| "casual", "friendly", "informal" | `--tone=casual` |
| "educational", "explainer" | `--tone=educational` |
| no tone specified | `--tone=professional` |
| user writes in Spanish or asks in Spanish | `--lang=es` |
| user writes in Portuguese | `--lang=pt` |
| no language specified | `--lang=en` |

### Source management

For niche topics, disable sources that won't have relevant content:

```bash
# Topic outside tech — disable HackerNews (very tech-specific)
--disable=hackernews

# Lifestyle / food / fashion
--sources=reddit,youtube,brave

# Finance / investing
--disable=hackernews,tiktok

# Pure tech topic — all sources are relevant, keep defaults
```

List all available sources:
```bash
python ~/.hermes/skills/social-media/trendingcontent/scripts/trendingcontent.py --list-sources
```

### Speed modes

```bash
--quick    # faster, fewer sources (~90s) — use when the user wants quick results
--deep     # thorough, more sources (~5 min) — use when quality matters more than speed
```

## Examples

```bash
# AI trends last 7 days, all platforms, English
python ~/.hermes/skills/social-media/trendingcontent/scripts/trendingcontent.py \
  "artificial intelligence" --days=7 --platform=all --lang=en

# LinkedIn post about fintech in Spanish, disable irrelevant sources
python ~/.hermes/skills/social-media/trendingcontent/scripts/trendingcontent.py \
  "fintech" --days=15 --platform=linkedin --lang=es --disable=hackernews,tiktok

# Viral Twitter thread about climate tech
python ~/.hermes/skills/social-media/trendingcontent/scripts/trendingcontent.py \
  "climate tech" --days=30 --platform=twitter --tone=viral

# Quick test run
python ~/.hermes/skills/social-media/trendingcontent/scripts/trendingcontent.py \
  "bitcoin" --days=7 --platform=twitter --quick
```

## Interpreting the output

The script outputs two sections:

### Section 1 — Research summary
A ranked list of trending posts, videos, and articles with titles, engagement scores, and source URLs.
- Present 3–5 highlights to the user as context: what's trending, which platforms, key themes.
- Cite sources using @handles (for X) and r/subreddit (for Reddit) when available.

### Section 2 — Content generation brief
A structured prompt block with platform specs, tone guidance, and the research as factual grounding.
- Use this block to generate the actual social media copy.
- Write the content yourself based on the brief — do NOT just paste the brief to the user.
- Stick strictly to facts from the research summary. Do not invent trends or stats.

## Full workflow

```
1. Run the script with appropriate parameters
2. Read the research summary — share key highlights with the user
3. Use the content generation brief to write the final copy
4. Present the copy to the user, clearly labeled by platform
5. Offer to adjust tone, length, or language if needed
```

## Pitfalls

- **Long runtime**: The script calls multiple external APIs concurrently. Warn the user it may take 1–3 minutes. Use `--quick` to speed up.
- **Missing SCRAPECREATORS_API_KEY**: The script will fail. Check `~/.hermes/.env` and ask the user to provide the key.
- **HackerNews for non-tech topics**: HackerNews almost never has content about lifestyle, culture, food, fashion, or local topics. Disable it with `--disable=hackernews` to avoid polluting results.
- **Do not invent content**: The generated copy must be grounded in the research output. Never make up trending stories, stats, or quotes.
- **Language detection**: If the user writes in Spanish or Portuguese, default `--lang` to match — do not force English output.
- **Research-only mode**: If the user only wants to know what's trending (no content needed), use `--research-only` and summarize the findings.
