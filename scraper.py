from playwright.sync_api import sync_playwright
import time
import random
import re

def scrape_until_crash(start_url, start_chapter, output_filename):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Track our current position so we can return it if something breaks
        current_url = start_url
        chapter_number = start_chapter
        
        with open(output_filename, 'a', encoding='utf-8') as f:
            
            page.goto(current_url, wait_until="domcontentloaded")
            
            while True:
                print(f"Scraping Chapter {chapter_number}...")
                
                try:
                    # Wait up to 60 seconds for the text
                    page.wait_for_selector('#chapter-content', timeout=60000)
                except Exception as e:
                    print(f"\n[!] Timeout or block detected on Chapter {chapter_number}.")
                    browser.close()
                    # Return the exact URL and chapter we failed on so the master loop can restart it
                    return page.url, chapter_number 

                # Extract and clean text
                paragraphs = page.locator('#chapter-content p').all_inner_texts()
                if paragraphs:
                    chapter_text = "\n\n".join(paragraphs)
                    chapter_text = re.sub(r'\b[0-9a-fA-F]{24}\b', '', chapter_text).strip()
                    
                    f.write(f"\n\n--- Chapter {chapter_number} ---\n\n")
                    f.write(chapter_text)
                    print(f"Saved Chapter {chapter_number}.")
                
                # Find and click Next
                next_button = page.locator('a:text-is("Next Chapter"), .next-chapter').first
                
                if next_button.is_visible():
                    with page.expect_navigation():
                        next_button.click()
                    
                    chapter_number += 1
                    
                    # Dynamic delay
                    word_count = len(chapter_text.split())
                    dynamic_delay = (word_count / 500) + random.uniform(1.5, 3.5)
                    time.sleep(min(dynamic_delay, 8.0))
                else:
                    print("No 'Next' button found. The novel is complete!")
                    browser.close()
                    # Return None to signal the master loop that the whole book is finished
                    return None, None 

if __name__ == "__main__":
    target_url = "ENTER TARGET URL"
    current_chapter = 1
    
    # The Master Retry Loop
    while target_url is not None:
        target_url, current_chapter = scrape_until_crash(target_url, current_chapter, "ENTER NAME")
        
        if target_url is not None:
            # If target_url isn't None, it means the script crashed.
            wait_time = 300 # 300 seconds = 5 minutes
            print(f"Waiting {wait_time} seconds before automatically restarting...")
            time.sleep(wait_time)
            print("Restarting scraper now!\n")
            #test
            