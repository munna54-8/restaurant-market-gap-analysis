# Kochi Restaurant Market: Cuisine Demand-Gap Analysis

## Problem
If you were deciding which type of restaurant to open in Kochi, which cuisine gives you the best shot — not by gut feel or "everyone opens a Kerala restaurant," but by an actual demand-versus-supply number?

## Data source & collection method
90 restaurant listings scraped from Zomato's structured (JSON-LD) data across 10 real Kochi localities (MG Road, Edappally, Kakkanad, Panampilly Nagar, Kaloor, Palarivattom, Fort Kochi, Kadavanthra, Marine Drive, Ernakulam City) — not a pre-existing dataset. Collected via a Python scraper respecting robots.txt and rate-limited requests.

## A data-quality finding worth stating upfront
63% of the initially scraped listings (57 of 90) were duplicates — the same restaurants appearing under multiple "nearby" localities. This revealed that Zomato's per-area listing widget draws from a shared citywide pool rather than fully distinct per-locality rankings, rather than being a scraping error. After deduplication, this analysis covers Kochi's 33 most prominent, most-reviewed restaurants — a meaningful but not exhaustive slice of the market, and the findings below are scoped accordingly.

## Approach
- Python (requests, BeautifulSoup) to scrape and parse structured listing data
- Pandas for cleaning, deduplication, and cuisine-tag parsing
- SQLite for storage and aggregation
- A custom demand-intensity index: `rating × log(review_count + 1)`, which prevents one high-review outlier from dominating an average while still rewarding restaurants that are both popular and well-rated
- A percentile-based gap score per cuisine: `demand_percentile − supply_percentile`, so cuisines are ranked by demand relative to how many restaurants already compete in that category, not raw counts

## Key findings
- **Burger (+73.1) and Coffee (+61.5) cuisines show the strongest demand-to-supply gap** — the clearest whitespace among Kochi's top-tier restaurants
- **Kerala (-73.1) and South Indian (-57.7) are the most oversaturated** — despite being the two most common cuisines in the dataset, they rank lowest on demand relative to supply
- **Review count and rating are essentially uncorrelated** (Pearson r = -0.039) — a restaurant with thousands of reviews is no more likely to be highly rated than one with a few hundred
- **63% of scraped listings were duplicates across localities** — a finding about platform behavior as much as a data-cleaning step

## Business recommendation
A new Burger or Coffee-focused concept has real, measurable whitespace among Kochi's most prominent restaurants. A new Kerala or South Indian restaurant — the default choice for most new entrants — would be competing in the most crowded, most commoditized segment of the market.

## Limitations
Sample reflects Zomato's "most prominent" listings per locality, not a full census of every restaurant in Kochi. Findings describe patterns among high-visibility restaurants, not the entire market.

## Tools
Python, Pandas, SQLite, Chart.js

## Dashboard
https://munna54-8.github.io/restaurant-market-gap-analysis/dashboard/kochi_restaurant_dashboard.html
