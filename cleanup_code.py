import os
import re

HEADER = """# Made by @codexnano from scratch.
# If you find any bugs, please let us know in the channel updates.
# You can 'git pull' to stay updated with the latest changes.

"""

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove triple-quoted docstrings
        content = re.sub(r'\"\"\"(.*?)\"\"\"', '', content, flags=re.DOTALL)
        content = re.sub(r'\'\'\'(.*?)\'\'\'', '', content, flags=re.DOTALL)
        
        processed_lines = []
        for line in content.splitlines():
            # Basic comment stripping that avoids strings
            clean_line = ""
            in_string = False
            string_char = None
            escaped = False
            
            for i, char in enumerate(line):
                if char == '\\' and not escaped:
                    escaped = True
                    clean_line += char
                    continue
                
                if char in ('"', "'") and not escaped:
                    if not in_string:
                        in_string = True
                        string_char = char
                    elif string_char == char:
                        in_string = False
                
                if char == '#' and not in_string:
                    break
                
                clean_line += char
                escaped = False
            
            if clean_line.strip():
                processed_lines.append(clean_line.rstrip())

        # Combine with header
        # Ensure we don't double add the header if run twice
        final_content = HEADER + "\n".join(processed_lines) + "\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    exclude_dirs = {'.git', 'venv', '__pycache__'}
    count = 0
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith('.py') and file != 'cleanup_code.py':
                path = os.path.join(root, file)
                if process_file(path):
                    count += 1
    print(f"Successfully processed {count} Python files.")

if __name__ == "__main__":
    main()
