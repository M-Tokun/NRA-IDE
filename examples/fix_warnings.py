import os
import glob

# 00〜10から始まるHTMLファイルを検索
files = glob.glob('examples/0[0-9]_*.html') + glob.glob('examples/10_*.html')

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. viewportメタタグの追加
    if '<meta name="viewport"' not in content:
        content = content.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">')

    # 2. backdrop-filterのSafari対応
    if 'backdrop-filter: blur' in content and '-webkit-backdrop-filter' not in content:
        content = content.replace('backdrop-filter: blur', '-webkit-backdrop-filter: blur(8px);\n            backdrop-filter: blur')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"完了しました！ 合計 {len(files)} 個のファイルを修正しました。")
