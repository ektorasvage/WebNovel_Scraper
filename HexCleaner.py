import re

# Use the exact name of your scraped file
input_filename = "full_novel.txt"
# We save to a new file so your original remains safe just in case
ShadowSlave = "full_novel_cleaned.txt"

print("Reading the original file...")
with open(input_filename, 'r', encoding='utf-8') as f:
    text_content = f.read()

print("Hunting down and deleting hex IDs...")
# Find all 24-character hex strings and replace them with nothing
cleaned_content = re.sub(r'\b[0-9a-fA-F]{24}\b', '', text_content)

print("Saving the cleaned version...")
with open(ShadowSlave, 'w', encoding='utf-8') as f:
    f.write(cleaned_content)

print(f"Done! Your clean text is saved as '{ShadowSlave}'.")