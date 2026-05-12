@echo off
chcp 65001 >nul
echo ===================================================
echo  VS Code ディープキャッシュクリア スクリプト
echo ===================================================
echo.
echo 【警告】
echo 実行する前に、現在開いているすべての VS Code ウィンドウを
echo 完全に閉じてください（保存されていないデータは失われます）。
echo.
pause

echo.
echo バックグラウンドに残っている VS Code プロセスを終了しています...
taskkill /F /IM Code.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo.
echo キャッシュフォルダを削除しています...

set "VSCODE_DIR=%APPDATA%\Code"

if exist "%VSCODE_DIR%\Cache" (
    rmdir /S /Q "%VSCODE_DIR%\Cache"
    echo [OK] Cache フォルダを削除しました
)

if exist "%VSCODE_DIR%\CachedData" (
    rmdir /S /Q "%VSCODE_DIR%\CachedData"
    echo [OK] CachedData フォルダを削除しました
)

if exist "%VSCODE_DIR%\CachedExtensionVSIXs" (
    rmdir /S /Q "%VSCODE_DIR%\CachedExtensionVSIXs"
    echo [OK] CachedExtensionVSIXs フォルダを削除しました
)

if exist "%VSCODE_DIR%\Code Cache" (
    rmdir /S /Q "%VSCODE_DIR%\Code Cache"
    echo [OK] Code Cache フォルダを削除しました
)

echo.
echo 削除処理が完了しました。
echo 次回 VS Code 起動時に、キャッシュが再構築されます（少し時間がかかる場合があります）。
echo.
echo 任意のキーを押して画面を閉じてください。
pause
