# Example 05 — Direct CLI Usage (Without an Agent)

Use the script directly from the terminal if you don't have Hermes set up, or want to pipe the output to another tool.

## Basic usage

```bash
cd /path/to/trendingcontent-agent

# Research + all platforms, English, last 30 days (defaults)
python scripts/trendingcontent.py "artificial intelligence"

# Twitter thread in Spanish, last 7 days
python scripts/trendingcontent.py "inteligencia artificial" --days=7 --platform=twitter --lang=es

# LinkedIn, professional, 15 days
python scripts/trendingcontent.py "remote work" --days=15 --platform=linkedin --tone=professional

# Viral Instagram caption in Portuguese
python scripts/trendingcontent.py "moda sustentavel" --days=30 --platform=instagram --tone=viral --lang=pt
```

## Source control

```bash
# See all available sources
python scripts/trendingcontent.py --list-sources

# Only Reddit + YouTube + Brave (skip Twitter, TikTok, HackerNews, Bluesky)
python scripts/trendingcontent.py "sourdough bread" --sources=reddit,youtube,brave

# All sources except HackerNews and TikTok
python scripts/trendingcontent.py "fintech latam" --disable=hackernews,tiktok --lang=es

# Tech topic — keep all sources
python scripts/trendingcontent.py "rust programming language" --days=14
```

## Speed modes

```bash
# Quick mode (~90s) — fewer API calls, good for testing
python scripts/trendingcontent.py "bitcoin" --quick

# Deep mode (~5min) — maximum coverage
python scripts/trendingcontent.py "climate tech" --deep
```

## Research only

```bash
# Just the trending content, no content generation brief
python scripts/trendingcontent.py "web3" --research-only

# Save research to a file
python scripts/trendingcontent.py "machine learning" --research-only > research_output.txt
```

## Pipe the brief to your own LLM

The script outputs a structured content brief that you can pipe to any LLM:

```bash
# Pipe to ollama
python scripts/trendingcontent.py "AI agents" --days=7 --platform=twitter --lang=en \
  | ollama run llama3.2

# Pipe to LLM CLI (Simon Willison's llm tool)
python scripts/trendingcontent.py "AI agents" --days=7 --platform=twitter \
  | llm -m claude-sonnet-4-6

# Save brief to file, then send to any API
python scripts/trendingcontent.py "climate" --platform=linkedin > brief.txt
cat brief.txt | curl -X POST https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"gpt-4o\", \"messages\": [{\"role\": \"user\", \"content\": $(cat brief.txt | jq -Rs .)}]}"
```

## Environment variables

```bash
# Required
export SCRAPECREATORS_API_KEY="your_key"

# Optional — enriches results with web search
export BRAVE_API_KEY="your_key"

# Or use a .env file in the project root
cat .env
# SCRAPECREATORS_API_KEY=your_key
# BRAVE_API_KEY=your_key
```

## Quick sanity check

```bash
# Verify API keys are working and sources respond
python scripts/trendingcontent.py "test" --days=7 --quick --research-only
```

If the output shows results from at least Reddit or HackerNews, your setup is working.
