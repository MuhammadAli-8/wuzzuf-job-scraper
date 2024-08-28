# Wuzzuf Job Scraper

This is a Python-based web scraping tool designed to extract job listings from [Wuzzuf.net](https://wuzzuf.net). The scraper uses Selenium to navigate the website, extract job details, and save them into a CSV file. It's a handy tool for anyone looking to collect job data for analysis or personal use.

## Features

- **Search by job title, location, or company**: Input any job-related query to start scraping.
- **Career level filtering**: Optionally filter jobs by career level (e.g., Student, Entry Level, Experienced, Manager).
- **Customizable number of records**: Choose how many job listings you want to scrape.
- **Detailed job information**: Extracts job title, company name, location, salary, requirements, description, skills, and more.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- Google Chrome
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) compatible with your Chrome version
- Selenium Python library (`pip install selenium`)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/wuzzuf-job-scraper.git
    cd wuzzuf-job-scraper
    ```

2. Make sure you have the correct version of ChromeDriver:

    - Download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
    - Place the `chromedriver` executable in your system's PATH or in the project directory.

## Usage

1. Run the script:

    ```bash
    python main.py
    ```

2. Enter your search query when prompted (e.g., job title, location, or company).

3. Select the desired career level (e.g., Student, Entry Level, Experienced, Manager) or choose "All" to include jobs of all career levels.

4. Specify the number of job listings to scrape.

5. The script will start scraping the job listings and save them into a CSV file named after your search query (e.g., `Engineer.csv`).

## Example

```bash
Enter Job Title, Location or Company: Engineer

Choose Career Level: 
    0 for "All"
    1 for "Student"
    2 for "Entry Level"
    3 for "Experienced"
    4 for "Manager"

Please enter the number corresponding to your desired career level: 0

There are 4051 Jobs Found, How many do you want to Scrape? 100

Job 1/100 Extracted Successfully.
Job 2/100 Extracted Successfully.
...
Engineer.csv Created Successfully.
```
## Notes

- Ensure that ChromeDriver is compatible with your Chrome browser version.
- Some job listings might have hidden or missing data (e.g., company name), in which case placeholders will be used in the CSV file.
- If the script encounters a stale element (due to dynamic page content), it will attempt to retry the extraction for that job.
