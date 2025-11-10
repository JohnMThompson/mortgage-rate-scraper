# mortgage-rate-scraper

A small Python utility that scrapes mortgage rates from a local credit union website and stores them in a MySQL database for historical tracking and analysis.

This repo contains a single scraper (`script.py`) which uses `requests` and `BeautifulSoup` to parse rate values and inserts them into a `daily_rates` table.

## Features

- Fetches mortgage rate values from the credit union website (example target: Wings Credit Union).
- Persists scraped values into MySQL for later analysis or visualization.
- Simple, dependency-light implementation intended for cron scheduling.

## Requirements

- Python 3.8+ (this repo includes a virtual environment with Python 3.10)
- A MySQL-compatible database
- Python packages listed in `requirements.txt` (requests, beautifulsoup4, mysql-connector, etc.)

## Installation

1. (Optional) Create and activate a virtual environment:

  python3 -m venv venv
  source venv/bin/activate

1. Install dependencies:

  pip install -r requirements.txt

1. Configure database credentials (see Configuration).

## Configuration

By default the project expects a `config.py` in the repo root with the following variables:

```python
host = "your-db-host"
user = "your-db-user"
pw = "your-db-password"
db = "your-database-name"
```

Important: Do not commit real credentials to version control. Prefer using environment variables or a separate, ignored configuration file. Example using environment variables (recommended):

```python
import os
host = os.environ.get('MORT_HOST')
user = os.environ.get('MORT_USER')
pw = os.environ.get('MORT_PW')
db = os.environ.get('MORT_DB')
```

If you keep `config.py`, ensure it is excluded from your git history (e.g. add it to `.gitignore`).

## Database schema (expected)

The scraper inserts rows into a table named `daily_rates`. Example schema that matches the fields used in `script.py`:

```sql
CREATE TABLE daily_rates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  source VARCHAR(64),
  `timestamp` DATETIME,
  `30_year_fixed_rate` FLOAT,
  `30_year_fixed_points` FLOAT,
  `71_arm_rate` FLOAT,
  `71_arm_point` FLOAT
);
```

Note: The column names are quoted in the SQL used by `script.py`. Adjust names/types as needed for your use case.

## Usage

Run the scraper manually:

```bash
python3 script.py
```

Typical practice is to run this script on a schedule (cron). Example cron entry to run daily at 18:00 UTC:

```cron
0 18 * * * /path/to/venv/bin/python /path/to/mortgage-rate-scraper/script.py >> /var/log/mortgage-scraper.log 2>&1
```

Adjust paths and timezone as appropriate for your server.

## Notes & Security

- The current `script.py` is minimal and assumes the page structure does not change. If the target website changes markup, the parsing logic will need updates.
- Avoid committing `config.py` with credentials. Prefer environment variables or secret management.
- The repo stores sample code only; sanitize or rotate any credentials that have been accidentally committed.

## Extending this project

- Add better error handling and retries around network/database operations.
- Add unit tests for the parsing logic using saved HTML fixtures.
- Add a small dashboard to visualize historical rates (e.g. using Grafana or a simple Flask app).

## License

This project is licensed under the MIT License — see the `LICENSE` file in the repository root for the full terms.

Short summary: you may use, copy, modify, and distribute this software with attribution. See `LICENSE` for details.

## Acknowledgements

Originally created as a small personal project to learn web scraping and cron scheduling.
