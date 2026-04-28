import os
import re


def normalize_md(text: str) -> str:
    # CRLF/CR → LF
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # 3行以上の連続空白行を1空行に圧縮
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 見出し前を1空行に統一
    text = re.sub(r'\n{2,}(#{1,6} )', r'\n\n\1', text)

    # 見出し直後の過剰空白を1空行に統一
    text = re.sub(r'(#{1,6} .+)\n{2,}', r'\1\n\n', text)

    # コードブロック前後: 3行以上 → 1空行を保持（0行にしない）
    text = re.sub(r'\n{3,}```', '\n\n```', text)
    text = re.sub(r'```\n{3,}', '```\n\n', text)

    # リスト前後: 3行以上 → 1空行を保持（段落境界を消さない）
    text = re.sub(r'\n{3,}(- )', r'\n\n\1', text)
    text = re.sub(r'(- .+)\n{3,}', r'\1\n\n', text)

    return text.strip() + '\n'


def process_directory(root_dir: str):
    changed = []
    unchanged = []

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        original = f.read()
                except UnicodeDecodeError:
                    print(f"SKIP (encoding error): {path}")
                    continue

                normalized = normalize_md(original)

                if original != normalized:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(normalized)
                    changed.append(path)
                    print(f"Normalized: {path}")
                else:
                    unchanged.append(path)
                    print(f"OK:         {path}")

    print()
    print(f"=== Result: {len(changed)} normalized, {len(unchanged)} unchanged ===")


if __name__ == '__main__':
    target_dir = './'
    process_directory(target_dir)
