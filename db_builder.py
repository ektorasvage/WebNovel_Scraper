import sqlite3
import re
import os
import glob

# Notice we removed the os.remove() lines. We want to keep the existing database!
conn = sqlite3.connect('webnovel.db')
cursor = conn.cursor()

# 1. Use IF NOT EXISTS so we don't overwrite the tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS novels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE NOT NULL
    )
''')

# 2. Add a UNIQUE constraint on novel_id + chapter_number
# This prevents duplicate chapters if you run the script multiple times
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        novel_id INTEGER NOT NULL,
        chapter_number INTEGER NOT NULL,
        title TEXT,
        content TEXT NOT NULL,
        FOREIGN KEY (novel_id) REFERENCES novels (id),
        UNIQUE(novel_id, chapter_number)
    )
''')

novel_files = glob.glob('raw_novels/*.txt')

for filepath in novel_files:
    novel_title = os.path.basename(filepath).replace('.txt', '').strip()
    
    # 3. INSERT OR IGNORE safely adds new novels and skips ones already in the DB
    cursor.execute('INSERT OR IGNORE INTO novels (title) VALUES (?)', (novel_title,))
    
    # Get the ID of the novel (whether it was just added or already existed)
    cursor.execute('SELECT id FROM novels WHERE title = ?', (novel_title,))
    novel_id = cursor.fetchone()[0]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        full_text = f.read()
        
    parts = re.split(r'(?m)^(---\s*Chapter\s+\d+\s*---)', full_text, flags=re.IGNORECASE)
    
    chapters_dict = {}
    for i in range(1, len(parts), 2):
        chap_title = parts[i].strip('- \t\n\r')
        content = parts[i+1].strip() if (i + 1) < len(parts) else ""
        chapters_dict[chap_title] = content
        
    # 4. INSERT OR REPLACE updates existing chapters (if you fixed typos) and adds new ones
    chapter_num = 1
    for chap_title, content in chapters_dict.items():
        cursor.execute('''
            INSERT OR REPLACE INTO chapters (novel_id, chapter_number, title, content)
            VALUES (?, ?, ?, ?)
        ''', (novel_id, chapter_num, chap_title, content))
        chapter_num += 1
        
    print(f"Synced '{novel_title}' (Total chapters: {chapter_num - 1})")

# 5. Compress the database to save space after any updates

conn.commit()
cursor.execute('VACUUM')
conn.close()
print("Incremental database sync complete!")