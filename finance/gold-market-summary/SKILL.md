---
name: gold-market-summary
description: Analyze and summarize global gold price movements over the past 14 days using live market data.
version: 1.0.0
author: Quang Tu Do
license: MIT

metadata:
  hermes:
    category: finance
    tags:
      - gold
      - xauusd
      - commodities
      - macroeconomics
      - investing
      - market-analysis
      - precious-metals
      - finance
    requires_toolsets: [web]           # Hide if the web toolset is NOT active
    requires_tools: [web_search]       # Hide if web_search tool is NOT available
    fallback_for_toolsets: [browser]   # Hide if the browser toolset IS active
    fallback_for_tools: [browser_navigate]  # Hide if browser_navigate IS available
---

# Gold Market Summary

## Purpose

Produce an objective, data-driven summary of **global gold price movements during the previous 14 calendar days** using **live data retrieved at execution time**.

This skill is intended for investment research, market monitoring, and macroeconomic analysis.

---

## When to Use

Use this skill whenever the user asks questions such as:

- Summarize gold prices over the last two weeks.
- What happened to gold recently?
- Explain the latest movements in XAU/USD.
- Why did gold rise (or fall) recently?
- Provide a market update on gold.
- Analyze current gold market sentiment.
- Give me a gold market briefing.

---

## Core Principles

### Always use live information

Never answer using model pretraining alone.

Retrieve current market information before beginning the analysis.

If live data cannot be retrieved, explicitly state this limitation instead of generating estimates.

---

### Time Window

Analyze only:

**Current Date − 14 calendar days → Current Date**

Do not include older events unless they are necessary to explain recent price action.

---

### Preferred Information

Prioritize authoritative financial sources, including:

- LBMA
- CME Group
- Kitco
- TradingView
- Bloomberg
- Reuters
- CNBC
- Financial Times
- Investing.com
- MarketWatch
- World Gold Council
- Federal Reserve releases
- U.S. Bureau of Labor Statistics
- U.S. Treasury
- FRED

---

## Procedure

### 1. Retrieve Current Market Data

Collect:

- Current spot gold price (XAU/USD)
- Price 14 days ago
- Highest price during period
- Lowest price during period
- Percentage change
- Daily trend

---

### 2. Build a Timeline

Create a chronological timeline containing major price movements.

For each significant movement include:

- Date
- Approximate price movement
- Magnitude
- Primary catalyst

---

### 3. Identify Key Drivers

Explain how each factor influenced gold:

- Federal Reserve communications
- Interest-rate expectations
- Treasury yields
- US Dollar Index (DXY)
- CPI
- PPI
- Employment reports
- GDP
- Central bank purchases
- ETF inflows/outflows
- Geopolitical events
- Risk sentiment
- Major economic releases

For every driver specify whether it was:

- Bullish
- Bearish
- Neutral

---

### 4. Technical Analysis

Provide a concise technical overview including:

- Momentum
- Trend
- Support levels
- Resistance levels
- Breakouts
- Pullbacks
- Important chart patterns

Avoid excessive technical jargon.

---

### 5. Market Sentiment

Summarize the current consensus among:

- Analysts
- Institutional investors
- Precious metals traders

Clearly distinguish:

- Facts
- Market expectations
- Analyst opinions

---

### 6. Final Summary

Finish with a concise executive summary containing 3–5 bullets highlighting the most important developments.

---

## Output Format

# Gold Market Summary (Last 14 Days)

## Price Overview

- Current Spot Price
- 14-Day Change
- Highest Price
- Lowest Price
- Overall Trend

---

## Timeline

| Date | Price Movement | Main Driver |
|------|----------------|-------------|

---

## Key Drivers

Discuss each important macroeconomic or geopolitical factor.

---

## Technical Perspective

- Momentum
- Trend
- Support
- Resistance

---

## Market Sentiment

Summarize current market positioning and analyst consensus.

---

## Executive Summary

- Bullet 1
- Bullet 2
- Bullet 3
- Bullet 4
- Bullet 5

---

## Style Guidelines

Always write in:

- Professional tone
- Objective language
- Concise paragraphs
- Evidence-based analysis

Avoid:

- Speculation presented as fact
- Unsupported predictions
- Hallucinated prices
- Using pretrained knowledge when current data are available

Whenever numerical values are available:

- Include approximate prices.
- Include percentage changes.
- Mention the reporting currency (USD).
- Clearly indicate when values are approximate.

---

## Verification Checklist

Before finishing, verify:

- ✓ Live market information was retrieved.
- ✓ The analysis covers only the previous 14 days.
- ✓ Numerical values are internally consistent.
- ✓ Major price movements are explained.
- ✓ Facts are distinguished from opinions.
- ✓ Output follows the required structure.
- ✓ Data sources are cited whenever possible.