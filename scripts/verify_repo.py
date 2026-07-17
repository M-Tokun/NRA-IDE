import os
import re
import sys
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding='utf-8')

# File types to check
CHECK_EXTENSIONS = ('.md', '.html', '.py')

# Exclude directories
EXCLUDE_DIRS = {'.git', '.vscode', '.devcontainer', 'node_modules', '__pycache__', 'local_reports'}

class HTMLTagChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags_stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        # Self-closing tags in HTML5
        if tag in {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'col', 'embed'}:
            return
        self.tags_stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'col', 'embed'}:
            return
        if not self.tags_stack:
            self.errors.append(f"Unexpected closing tag: </{tag}> at line {self.getpos()[0]}")
            return
        last_tag, pos = self.tags_stack.pop()
        if last_tag != tag:
            self.errors.append(f"Mismatched tag: expected </{last_tag}> (from line {pos[0]}), found </{tag}> at line {self.getpos()[0]}")
            # Put back to keep stack aligned if possible, or just continue
            self.tags_stack.append((last_tag, pos))

def check_file(file_path):
    file_errors = {
        'encoding': [],
        'bom': False,
        'katex_adjacent': [],
        'katex_text_underscore': [],
        'katex_setext': [],
        'html_tags': [],
    }
    
    # Read raw bytes first to check for BOM
    try:
        with open(file_path, 'rb') as f:
            raw = f.read()
    except Exception as e:
        file_errors['encoding'].append(f"Failed to read file: {e}")
        return file_errors

    if raw.startswith(b'\xef\xbb\xbf'):
        file_errors['bom'] = True

    # Decode as UTF-8
    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError as e:
        file_errors['encoding'].append(f"UTF-8 Decode Error: {e}")
        return file_errors

    ext = os.path.splitext(file_path)[1].lower()

    # Strip <script>/<style> blocks in HTML before the Japanese/$ adjacency
    # check, since `${...}` JS template literals are not KaTeX and trigger
    # false positives.
    scan_content = content
    if ext == '.html':
        def _blank_block(m):
            # Preserve line count/offsets by keeping newlines, blanking the rest.
            return '\n' * m.group(0).count('\n')
        scan_content = re.sub(
            r'<(script|style)\b[^>]*>.*?</\1>', _blank_block, content,
            flags=re.DOTALL | re.IGNORECASE
        )
    lines = scan_content.splitlines()

    # Check for KaTeX adjacent to Japanese characters (only for .md and .html)
    if ext in ('.md', '.html'):
        for idx, line in enumerate(lines, 1):
            # Check for: Japanese character followed directly by $ (excluding double $)
            for match in re.finditer(r'([^\x00-\x7F])\$([^$]|$)', line):
                file_errors['katex_adjacent'].append(
                    f"Line {idx}: Japanese char followed directly by '$' without space: '{line[max(0, match.start()-10):match.end()+10]}'"
                )
            # Check for: $ followed directly by Japanese character (excluding double $)
            for match in re.finditer(r'([^$]|^)\$([^\x00-\x7F])', line):
                file_errors['katex_adjacent'].append(
                    f"Line {idx}: '$' followed directly by Japanese char without space: '{line[max(0, match.start()-10):match.end()+10]}'"
                )

        # Check for \text{..._...} inside math blocks
        block_maths = re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL)
        for block in block_maths:
            for text_match in re.finditer(r'\\text\{([^}]*?_[^}]*?)\}', block):
                file_errors['katex_text_underscore'].append(
                    f"Found underscore inside \\text{{}} in block math: '\\text{{{text_match.group(1)}}}'"
                )
                
        # Also find inline math (excluding block math)
        clean_content = re.sub(r'\$\$.*?\$\$', '', content, flags=re.DOTALL)
        inline_maths = re.findall(r'\$([^$]+?)\$', clean_content)
        for inline in inline_maths:
            for text_match in re.finditer(r'\\text\{([^}]*?_[^}]*?)\}', inline):
                file_errors['katex_text_underscore'].append(
                    f"Found underscore inside \\text{{}} in inline math: '\\text{{{text_match.group(1)}}}'"
                )

        # Check for a bare '=' or '-' line inside a $$ block, immediately
        # after a non-blank line: CommonMark reads this as a Setext heading
        # underline, hijacking the paragraph before the math delimiters are
        # ever recognized, which breaks the rendering.
        in_block = False
        prev_line = None
        for idx, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped == '$$':
                in_block = not in_block
                prev_line = None
                continue
            if in_block:
                if re.match(r'^(=+|-+)$', stripped) and prev_line:
                    file_errors['katex_setext'].append(
                        f"Line {idx}: bare '{stripped}' after '{prev_line}' is parsed as a Setext heading underline"
                    )
                prev_line = stripped if stripped else None

    # Check for HTML tag balance in .html files
    if ext == '.html':
        checker = HTMLTagChecker()
        try:
            checker.feed(content)
            if checker.errors:
                file_errors['html_tags'].extend(checker.errors)
            if checker.tags_stack:
                for tag, pos in checker.tags_stack:
                    file_errors['html_tags'].append(f"Unclosed tag: <{tag}> opened at line {pos[0]}")
        except Exception as e:
            file_errors['html_tags'].append(f"HTML Parsing error: {e}")

    return file_errors

def main():
    print("Starting repository verification...")
    total_files = 0
    errors_count = 0
    bom_files = []
    encoding_errors = []
    katex_adjacent_errors = []
    katex_underscore_errors = []
    katex_setext_errors = []
    html_tag_errors = []

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if file.endswith(CHECK_EXTENSIONS):
                file_path = os.path.join(root, file)
                # Skip the verification script itself to avoid self-reporting
                if file_path == os.path.join('.', 'scripts', 'verify_repo.py'):
                    continue
                total_files += 1
                res = check_file(file_path)
                
                has_error = False
                if res['bom']:
                    bom_files.append(file_path)
                    has_error = True
                if res['encoding']:
                    encoding_errors.append((file_path, res['encoding']))
                    has_error = True
                if res['katex_adjacent']:
                    katex_adjacent_errors.append((file_path, res['katex_adjacent']))
                    has_error = True
                if res['katex_text_underscore']:
                    katex_underscore_errors.append((file_path, res['katex_text_underscore']))
                    has_error = True
                if res['katex_setext']:
                    katex_setext_errors.append((file_path, res['katex_setext']))
                    has_error = True
                if res['html_tags']:
                    html_tag_errors.append((file_path, res['html_tags']))
                    has_error = True
                
                if has_error:
                    errors_count += 1

    print(f"\nScan complete. Total checked files: {total_files}")
    print(f"Files with issues: {errors_count}\n")

    if bom_files:
        print("=== Files with UTF-8 BOM ===")
        for f in bom_files:
            print(f"  {f}")
        print()

    if encoding_errors:
        print("=== Files with Encoding/Decode Errors (文字化け) ===")
        for f, errs in encoding_errors:
            print(f"  {f}:")
            for e in errs:
                print(f"    {e}")
        print()

    if html_tag_errors:
        print("=== Files with HTML Tag Issues ===")
        for f, errs in html_tag_errors:
            print(f"  {f}:")
            for e in errs:
                print(f"    {e}")
        print()

    if katex_underscore_errors:
        print("=== Files with KaTeX Underscore inside \\text{} ===")
        for f, errs in katex_underscore_errors:
            print(f"  {f}:")
            for e in errs:
                print(f"    {e}")
        print()

    if katex_setext_errors:
        print("=== Files with Bare '=' / '-' Lines Inside $$ Blocks (Setext heading hijack) ===")
        for f, errs in katex_setext_errors:
            print(f"  {f}:")
            for e in errs:
                print(f"    {e}")
        print()

    if katex_adjacent_errors:
        print("=== Files with Adjacent Japanese Characters and $ (No Space) ===")
        print(f"Found in {len(katex_adjacent_errors)} files. Showing summary counts:")
        for f, errs in katex_adjacent_errors:
            print(f"  {f} ({len(errs)} issues)")
            for e in errs[:3]:
                print(f"    {e}")
            if len(errs) > 3:
                print(f"    ... and {len(errs) - 3} more")
        print()

    print("=== Running Python Compilation Check ===")
    import compileall
    success = compileall.compile_dir('.', maxlevels=10, quiet=1, force=False)
    if success:
        print("All Python files compiled successfully!")
    else:
        print("Some Python files had compilation/syntax errors!")

if __name__ == '__main__':
    main()
