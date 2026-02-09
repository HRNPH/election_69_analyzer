# Thai Election 69 Correlative Analyzer

An analytical tool designed to scrape and evaluate Thai election data, inspired by the correlation observations shared by [Khajochi's Blog](https://www.facebook.com/KhajochiBlog/posts/pfbid02qyYXY3NH7zns1gr3Emhdcij48y8UFQg3htvXYHRgfaDosjhQzytHapCAAj3bLhgl).

This project investigates the relationship between Constituency MP candidate numbers and Party List rankings across various election districts.

## 📊 Project Overview

The analyzer performs two primary functions:
1. **Data Acquisition**: Automates the collection of unofficial election results (Constituency and Party List) from the Thai PBS platform.
2. **Correlation Analysis**: Compares the winning MP's candidate number against the top 7 rankings of the Party List to identify statistical overlaps or trends.

## 🚀 Key Features

- **Efficient Scraping**: Utilizes direct JSON API endpoints for high-speed data retrieval.
- **Province Jumps**: Implements intelligent area-code skipping to avoid redundant requests for invalid districts.
- **Dynamic Aggregation**: Summarizes outcomes by party, providing a sorted overview of where candidate-party number matches occur most frequently.
- **Custom Filters**: Automatically excludes specific party codes (e.g., 06 and 09) from the analysis to focus on relevant variables.

## 🛠️ Installation

Ensure you have Python 3.12+ installed.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/election_69_analyzer.git
   cd election_69_analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install requests
   ```

## 📖 Usage

The analysis is performed in two sequential steps:

### 1. Data Collection (if raw data updating is needed)
Execute the scraper to download the latest unofficial results from Thai PBS. This process builds a local database in the `data/` directory.
```bash
python scripts/election_scraper.py
```
*Note: This process may take 5–10 minutes depending on network conditions.*

### 2. Statistical Comparison
Run the comparer to analyze the correlation between winning MP numbers and the top 7 Party List results.
```bash
python scripts/mp_pl_comparer.py
```

To also export JSON results and update the dashboard data, use the `--export` flag:
```bash
python scripts/mp_pl_comparer.py --export
```
This writes timestamped results to `docs/data/results.json` and appends a snapshot to `docs/data/history.json`.

## 🌐 Live Dashboard

A static HTML dashboard is available in `docs/index.html` and is automatically deployed to **GitHub Pages**. It visualizes:
- Summary statistics (total areas, match count, match rate)
- Bar chart of matches by party
- Filterable area-by-area detail table
- Scrape history over time

## ⚙️ Automated Pipeline (GitHub Actions)

A workflow (`.github/workflows/scrape-and-deploy.yml`) runs **every hour** to:
1. Scrape the latest election data from Thai PBS
2. Run the correlation analysis and export JSON results
3. Commit updated data back to the repository
4. Deploy the dashboard to GitHub Pages

The workflow can also be triggered manually via `workflow_dispatch`.

> **Setup**: Enable GitHub Pages in the repository settings (Settings → Pages → Source: GitHub Actions).

## 📝 Methodology
The analyzer extracts the "MP Number" from the `candidateCode` of the winning constituency candidate. It then checks if that number matches the last two digits of any `partyCode` ranked #1 through #7 in the Party List for that same area. 

By default, parties **06 (United Thai Nation Party)** and **09 (Pheu Thai Party)** are excluded from the comparison to reduce known statistical bias.

## 🙏 Acknowledgments
- **Inspiration**: Khajochorn (Khajochi) for the initial observation and analysis.
- **Data Source**: Results are fetched from the [Thai PBS Election 69](https://www.thaipbs.or.th/election69/result/en/geo?region=all&view=area) interactive portal. We are grateful for the availability of this public information for educational and analytical purposes.

## 🤖 Built with Gemini
This project was primarily developed with the assistance of **Gemini**. If you encounter any bugs, unexpected behavior, or inaccuracies in the analysis, please feel free to report them.

---
*Disclaimer: This project is for analytical and educational purposes only. Data is based on unofficial results as reported by Thai PBS.*