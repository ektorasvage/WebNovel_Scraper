from ebooklib import epub
import re

def convert_txt_to_epub(txt_filename, epub_filename, book_title):
    print(f"Reading {txt_filename}...")
    with open(txt_filename, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # Create the EPUB book
    book = epub.EpubBook()
    book.set_identifier("id123456")
    book.set_title(book_title)
    book.set_language("en")

    # Split the text by your chapter dividers (e.g., "--- Chapter 1 ---")
    # This regex captures the chapter title and the text that follows it
    chapters_raw = re.split(r'\n--- (Chapter \d+) ---\n', full_text)
    
    epub_chapters = []
    
    # The split creates a list like: [intro_text, "Chapter 1", chapter_1_text, "Chapter 2", chapter_2_text]
    # We skip the very first item (index 0) if it's just empty space before Chapter 1
    for i in range(1, len(chapters_raw), 2):
        chapter_title = chapters_raw[i]
        chapter_content = chapters_raw[i+1].strip()

        # Format the text with basic HTML paragraphs so it looks good on e-readers
        formatted_content = "".join([f"<p>{p}</p>" for p in chapter_content.split('\n\n')])
        
        # Create an EPUB chapter
        file_name = f"chapter_{i}.xhtml"
        c = epub.EpubHtml(title=chapter_title, file_name=file_name, lang='en')
        c.content = f"<h2>{chapter_title}</h2>{formatted_content}"
        
        # Add chapter to the book
        book.add_item(c)
        epub_chapters.append(c)
        print(f"Added {chapter_title}")

    # Build the Table of Contents and spine (reading order)
    book.toc = tuple(epub_chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # The spine tells the e-reader what order to display the pages
    book.spine = ['nav'] + epub_chapters

    # Save the file
    print("Generating EPUB...")
    epub.write_epub(epub_filename, book)
    print(f"Success! Saved as {epub_filename}")

if __name__ == "__main__":
    # Ensure you are using your cleaned text file
    convert_txt_to_epub("full_novel_cleaned.txt", "ShadowSlave.epub", "ShadowSlave")