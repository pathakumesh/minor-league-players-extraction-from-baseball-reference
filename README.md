# minor-league-players-extraction-from-baseball-reference
This is a Python Scrapy Project to scrape the minor league players from baseball-reference.com

1. Install the scrapy library: `pip install scrapy`
2. There needs to be input csv file with two headers (FIRST, LAST) in the path `Players-Stats/baseball_stat_extracter` with file name as `players_list.csv`.
3. Run the project with current directory in `Players-Stats/baseball_stat_extracter` as:
 `scrapy crawl baseball_extract_spider`
4. The files will be there in the path: `baseball_extract_spider` with file names as:
`MiLB-Player-Data-Master.csv` and `MiLB-Player-Data-Simplified.csv`.

