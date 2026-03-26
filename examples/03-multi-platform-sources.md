# Example 03 — Multi-Platform with Source Control

## Use case

Content creator covering DeFi / crypto. Wants content for all three platforms. Twitter and Reddit are the best sources for this topic — skip TikTok noise and HackerNews.

## Prompt to the agent

```
I want content for all my social platforms about what's happening in DeFi this month.
Twitter thread, LinkedIn post, and Instagram caption. Casual tone. English.
Only use Reddit, Twitter, and Brave Search as sources.
```

## What Hermes does internally

```bash
python ~/.hermes/skills/social-media/trendingcontent/scripts/trendingcontent.py \
  "DeFi decentralized finance" \
  --days=30 \
  --platform=all \
  --tone=casual \
  --lang=en \
  --sources=reddit,twitter,brave
```

## Example output

---

### [TWITTER]

```
1/ DeFi had a wild month. Here's everything that happened in one thread 🧵

2/ TVL (Total Value Locked) hit $95B — up 18% from last month.
That's not a fluke. Liquidity is back and protocols are competing hard for it.

3/ The biggest mover? Hyperliquid.
A perps DEX that launched its own L1 and processed more volume than Coinbase on some days.
No VC funding. No pre-mine. Community-first from day one.

4/ Meanwhile, Aave v4 launched with a unified liquidity layer across chains.
One position. Multiple networks. This is what cross-chain UX should look like.

5/ The narrative shift this month: people stopped asking "is DeFi dead?" and started asking "which protocol wins the liquidity war?"

Big difference.

6/ Most surprising stat: 41% of new DeFi wallets this month came from Southeast Asia.
The next wave of users isn't coming from Silicon Valley.

7/ If you're not paying attention to DeFi right now, you might be a cycle late.
What protocol are you watching? Drop it below 👇
```

---

### [LINKEDIN]

```
DeFi just had one of its strongest months in two years. Here's what the data says.

Total Value Locked crossed $95B — an 18% increase month-over-month. That's not a bounce. That's a trend.

Three things stood out:

Hyperliquid proved that community-first, VC-free token launches can compete with well-funded protocols. Their perps volume matched Coinbase on multiple days this month.

Aave v4's unified liquidity layer is the clearest sign yet that cross-chain UX is finally becoming a real priority, not just a talking point.

And perhaps most interesting: 41% of new DeFi wallets this month originated in Southeast Asia. The next chapter of decentralized finance is being written outside the US.

For anyone building in web3 or advising clients on digital assets: the infrastructure is maturing faster than the narrative gives it credit for.

What's your read on the current DeFi cycle?

#DeFi #Web3 #DecentralizedFinance #Crypto #Blockchain
```

---

### [INSTAGRAM]

```
DeFi just had its biggest month in years — and most people missed it 👀

Here's a quick breakdown of what happened:

📈 TVL hit $95B (up 18% MoM). Liquidity is back.

🏆 Hyperliquid — a community-built perps DEX — matched Coinbase in daily volume. No VCs. No pre-mine. Just product.

🔗 Aave v4 launched cross-chain liquidity. One position, multiple networks. Finally.

🌏 41% of new DeFi wallets this month came from Southeast Asia. The next wave of users isn't from Silicon Valley.

The DeFi "is it dead?" conversation ended this month. Now it's about which protocols win.

Are you watching any of these? Drop your picks below 👇

#DeFi #Crypto #Web3 #DecentralizedFinance #Blockchain #CryptoTwitter #Ethereum #yield #liquidity #altcoins #cryptonews #web3community #defiprotocol #cryptoinvestor #hyperliquid #aave
```

---

## Adjust the result

```
The Twitter thread is too long, cut it to 5 tweets max.
```

```
Make the Instagram caption more hype, this audience loves bold claims.
```

```
Translate all three to Spanish.
```
