# Example 04 — Research Only (No Content Generation)

## Use case

You want to know what's trending about a topic before deciding what content to create — or you just want a briefing without generating any posts yet.

## Prompt to the agent

```
What's been trending about climate tech in the last 7 days? Just give me the research, I'll decide what to write later.
```

## What Hermes does internally

```bash
python ~/.hermes/skills/social-media/trendingcontent/scripts/trendingcontent.py \
  "climate tech" \
  --days=7 \
  --research-only \
  --quick
```

## Example output

The agent presents the research summary directly:

---

> **Trending: climate tech — last 7 days**
>
> **Reddit** (r/ClimateActionPlan, r/energy, r/technology):
> - "Direct air capture just hit $300/ton — here's why that matters" — 6.4k upvotes
> - "Battery storage costs dropped 40% in 18 months — chart" — 4.1k upvotes
> - "Why rooftop solar is outpacing utility-scale in emerging markets" — 2.8k upvotes
>
> **X/Twitter:**
> - @EnergyMonitor thread on perovskite solar efficiency hitting 29.3% in lab conditions — 12k likes
> - Bill Gates quoted on nuclear: "Small modular reactors are now cheaper than I expected" — 34k likes
> - Viral thread: "The energy transition is happening faster than the IEA predicted — every year" — 8.7k retweets
>
> **YouTube:**
> - "Why nuclear is back on the table — explained" — 1.2M views (7 days)
> - "Direct Air Capture: can we actually remove CO2 at scale?" — 340k views
>
> **HackerNews:**
> - "Ask HN: Why are grid-scale battery projects taking so long to permit?" — 420 points
>
> **Brave Search:**
> - Reuters: EU approves €3.4B in state aid for green hydrogen projects
> - Bloomberg: US clean energy investment hit $303B in 2025

---

## Follow-up after research

Once you see the research, ask the agent to generate content:

```
Great, now write a LinkedIn post focused on the battery cost drop story. Professional tone.
```

```
Turn the nuclear angle into a casual Twitter thread. 6 tweets max.
```

```
Generate an Instagram caption about the direct air capture milestone. English.
```
