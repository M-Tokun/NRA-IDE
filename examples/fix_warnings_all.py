import os
import glob
import re

# examplesフォルダ内のすべてのHTMLファイルを取得
files = glob.glob('g:/git-M-Tokun/AI-IDE-NRA/NRA-IDE/examples/*.html')

processed_count = 0

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        
        # 1. viewportメタタグの追加（まだ存在しない場合のみ）
        if '<meta name="viewport"' not in content:
            content = content.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
            # 小文字のutf-8などのパターンにも対応
            content = content.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">')

        # 2. backdrop-filterのSafari対応
        if 'backdrop-filter: blur' in content and '-webkit-backdrop-filter' not in content:
            # 既にプレフィックスがある場合は除外するための正規表現や単純置換
            content = content.replace('backdrop-filter: blur', '-webkit-backdrop-filter: blur(8px);\n            backdrop-filter: blur')

        # 変更があった場合のみ保存
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            processed_count += 1
            print(f"修正しました: {os.path.basename(file_path)}")

    except Exception as e:
        print(f"エラー発生 ({os.path.basename(file_path)}): {e}")

print(f"\n完了しました！ 合計 {len(files)} 個中、 {processed_count} 個のファイルを修正しました。")
