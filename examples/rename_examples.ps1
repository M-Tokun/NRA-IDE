# NRA-IDE examples リネーム完全版
# 実行前に必ずバックアップを確認すること
Set-Location "G:\OneDrive\AI-IDE-NRA\NRA-IDE\examples"

# ── 12〜16番：日付・バージョン除去 ──
Rename-Item "12v2_agri_mol_antagonism_2026-03-08_0213.html" `
            "12_agri_mol_antagonism_JP.html" -ErrorAction SilentlyContinue

Rename-Item "13_photosynthesis_layer5_2026-03-08_0224.html" `
            "13_photosynthesis_layer5_JP.html" -ErrorAction SilentlyContinue

Rename-Item "NRA_IDE_Demo14_PowerGrid_Transition_2026-03-21.html" `
            "14_powergrid_transition_JP.html" -ErrorAction SilentlyContinue

Rename-Item "NRA_IDE_Demo15_OR_ICU_Continuum_2026-03-21.html" `
            "15_or_icu_continuum_JP.html" -ErrorAction SilentlyContinue

Rename-Item "NRA-IDE_Passive_Safety.html" `
            "16_passive_safety_JP.html" -ErrorAction SilentlyContinue

# ── test-tempから昇格 ──
Copy-Item "test-temp\氷から水への相転移nra_ide_water_ice_20260324_2216.html" `
          "17_water_ice_phase_transition_JP.html" -ErrorAction SilentlyContinue

Copy-Item "test-temp\chain_tension_nra_ide_2026-03-19_0113.html" `
          "18_chain_tension_JP.html" -ErrorAction SilentlyContinue

Copy-Item "test-temp\air_pressure_nra_ide_2026-03-19_0209.html" `
          "19_air_pressure_JP.html" -ErrorAction SilentlyContinue

Copy-Item "test-temp\water_pressure_nra_ide_2026-03-19_0202.html" `
          "20_water_pressure_JP.html" -ErrorAction SilentlyContinue

Copy-Item "test-temp\NRA-IDE_CABG_Monitor.html" `
          "21_cabg_monitor_JP.html" -ErrorAction SilentlyContinue

Copy-Item "test-temp\NRA-IDE_Vascular_Monitor_局所血管_細胞状態遷移_手術支援版_.html" `
          "22_vascular_monitor_JP.html" -ErrorAction SilentlyContinue

# ── double-damperから昇格 ──
Copy-Item "double-damper-autonomous-driving-safety-architecture\nra_ide_sample_demo_2026-03-07_1922.html" `
          "23_sample_demo_JP.html" -ErrorAction SilentlyContinue

Copy-Item "double-damper-autonomous-driving-safety-architecture\nra_ide_sample_demo_2026-03-07_1922_EN.html" `
          "23_sample_demo_EN.html" -ErrorAction SilentlyContinue

Copy-Item "double-damper-autonomous-driving-safety-architecture\nra_ide_vehicle_mandatory_boundary_demo_2026-03-07_1931.html" `
          "24_vehicle_mandatory_boundary_JP.html" -ErrorAction SilentlyContinue

Copy-Item "double-damper-autonomous-driving-safety-architecture\nra_ide_vehicle_mandatory_boundary_demo_2026-03-07_1931_EN.html" `
          "24_vehicle_mandatory_boundary_EN.html" -ErrorAction SilentlyContinue

# ── 確認 ──
Write-Host "`n完了。現在のexamplesファイル一覧:" -ForegroundColor Cyan
Get-ChildItem "*.html" | Sort-Object Name | Select-Object Name