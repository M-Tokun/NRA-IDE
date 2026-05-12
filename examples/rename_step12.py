import os
import subprocess

# スクリプトがあるディレクトリ（examples）に移動
os.chdir(os.path.dirname(os.path.abspath(__file__)))

renames = [
    ("NRA-IDE_AutoDrive_POC_2_JP.html", "42_AutoDrive_POC_2_JP.html"),
    ("NRA-IDE_AutoDrive_POC_2_EN.html", "42_AutoDrive_POC_2_EN.html"),
    ("NRA-IDE_AutoDrive_POC_3_JP.html", "43_AutoDrive_POC_3_JP.html"),
    ("NRA-IDE_AutoDrive_POC_3_EN.html", "43_AutoDrive_POC_3_EN.html"),
    ("NRA-IDE_RobotArm_POC_1_JP.html", "44_RobotArm_POC_1_JP.html"),
    ("NRA-IDE_RobotArm_POC_1_EN.html", "44_RobotArm_POC_1_EN.html"),
    ("NRA-IDE_HybridCalc_vs_Traditional_2026-04-20_2041_JP.html", "45_HybridCalc_vs_Traditional_JP.html"),
    ("NRA-IDE_HybridCalc_vs_Traditional_2026-04-20_2041_EN.html", "45_HybridCalc_vs_Traditional_EN.html"),
    ("NRA-IDE_Connection_vs_Mixing_Risk_1.html", "46_Connection_vs_Mixing_JP.html"),
    ("NRA-IDE_Connection_vs_Mixing_EN.html", "46_Connection_vs_Mixing_EN.html"),
    ("NRA-IDE_FPGA_Demo_2026-03-14_2157_SPEED.html", "47_FPGA_Demo_SPEED_JP.html"),
    ("NRA-IDE_人体5要素相関_実数値推移デモ.html", "48_Human_5Factors_Correlation_JP.html"),
    ("NRA_Architecture_Infographic.html", "49_Architecture_Infographic_JP.html"),
    ("NRA_Architecture_Infographic_EN.html", "49_Architecture_Infographic_EN.html"),
    ("制約は制限ではない。制約こそが知性を駆動する力である。.html", "50_Constraint_Philosophy_JP.html"),
]

for old, new in renames:
    if os.path.exists(old):
        print(f"Renaming {old} -> {new}")
        subprocess.run(f'git mv "{old}" "{new}"', shell=True)
    else:
        print(f"Skipped {old} (Not found)")

print("\nDone!")
