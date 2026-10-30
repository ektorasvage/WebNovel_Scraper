WEB NOVEL DATA PIPELINE AND SCRAPER

DESCRIPTION
This project is a robust data-extraction pipeline built with Python and Playwright. It is designed to scrape web novel chapters into cleanly formatted text files, acting as the primary data source for populating a local 
SQLite database in a custom Flutter reader app.
While currently configured for NovelFull, the script is highly modular and can be adapted to almost any standard reader site. It operates by launching a headless/visible Chromium browser, extracting the raw text fromthe DOM,
and parsing it cleanly into a .txt file.

KEY FEATURES

    Data Sanitization: Utilizes regex to detect and strip leftover hex-string artifacts embedded in the site's HTML.

    Anti-Bot Evasion: Calculates dynamic, randomized delays based on chapter word count to mimic human reading behavior, preventing Cloudflare IP bans and CAPTCHA triggers.

    Fault-Tolerance: Features an auto-resume master loop. If a timeout occurs or a bot-detection challenge is triggered, the script automatically pauses for 5 minutes and safely restarts exactly where it left off.

INSTRUCTIONS
By default, the script is ready to use for NovelFull.

    Navigate to your target novel's first chapter (e.g., https://novelfull.net/shadow-slave/chapter-1-nightmare-begins.html).

    Paste this URL into the target_url variable.

    Update the desired output file name inside the scrape_until_crash call within the master loop:

    scrape_until_crash(target_url, current_chapter, "shadow_slave.txt")

Once complete, you can read directly from the text file, import it into an SQLite database, or use the provided TXT2Epub script to generate an EPUB for readers like Moon+ Reader.

ADAPTING TO OTHER WEBSITES
To scrape a site other than NovelFull, you only need to modify the CSS selectors to match the new site's DOM structure:

    Chapter Content: Right-click the first word of the chapter text and select "Inspect". Find the id of the container holding the text (e.g., id="chapter-content") and update the page.locator() in the script.

    Next Button: Inspect the "Next Chapter" button. Update the script to match either the exact text of the button (e.g., "Next") or its CSS class.

SCALABILITY ROADMAP
Because individual web scraping is inherently constrained by the need to mimic human reading speeds, scaling this process vertically (speeding up requests) on a single site will trigger IP bans.

Future optimizations for this pipeline will focus on horizontal scaling. This involves running the script concurrently across multiple different web novel domains. 
Because many of these domains share Cloudflare as a WAF (Web Application Firewall), upcoming stress tests will determine the threshold of concurrent requests Cloudflare allows from a single IP before globally flagging
the traffic.
