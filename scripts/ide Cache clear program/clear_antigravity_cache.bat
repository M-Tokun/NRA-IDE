@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

echo ===================================================
echo  Antigravity (AI) キャッシュクリア スクリプト
echo ===================================================
echo.
echo 【警告】
echo この操作は Antigravity の会話履歴、記憶（Brain）、
echo および一時ファイルを削除します。
echo 設定ファイル（user_settings.pb）などは保持されます。
echo.
echo 実行する前に VS Code を完全に閉じてください。
echo.
set /p SURE="本当に実行しますか？ (Y/N): "
if /i "!SURE!" neq "Y" exit /b

echo.
echo バックグラウンドの VS Code を終了しています...
taskkill /F /IM Code.exe /T 2>nul
timeout /t 2 /nobreak >nul

set "AG_DIR=%USERPROFILE%\.gemini\antigravity"

if not exist "!AG_DIR!" (
    echo [Error] Antigravity のディレクトリが見つかりません: !AG_DIR!
    pause
    exit /b
)

echo.
echo キャッシュデータを削除中...

rem 削除対象リスト
set "TARGETS=brain knowledge browser_recordings html_artifacts scratch code_tracker context_state annotations"

for %%T in (!TARGETS!) do (
    if exist "!AG_DIR!\%%T" (
        rmdir /S /Q "!AG_DIR!\%%T"
        echo [OK] %%T を削除しました
    )
)

echo.
echo 処理が完了しました。
echo 次回起動時、Antigravity はクリーンな状態で開始されます。
echo.
pause
