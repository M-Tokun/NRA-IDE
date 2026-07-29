import importlib.util
import re
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_HANDOFF = REPO_ROOT / "examples" / "session_handoff_2026-03-08_0237.md"


def load_module(relative_path: str, module_name: str):
    path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class LegacyDemoStateMigrationTests(unittest.TestCase):
    def test_current_demo_sources_do_not_use_legacy_fail_state_names(self):
        roots = (REPO_ROOT / "examples", REPO_ROOT / "nra-core" / "implementation")
        suffixes = {".py", ".html", ".md"}
        for root in roots:
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix not in suffixes or path == HISTORICAL_HANDOFF:
                    continue
                text = path.read_text(encoding="utf-8-sig")
                self.assertNotIn("FAIL_CLOSED", text, str(path))
                self.assertNotIn("FAIL-CLOSED", text, str(path))
                self.assertIsNone(re.search(r"\bR_FAIL\b", text), str(path))

    def test_historical_handoff_remains_identifiable_as_history(self):
        text = HISTORICAL_HANDOFF.read_text(encoding="utf-8-sig")
        self.assertIn("FAIL-CLOSED", text)

    def test_power_grid_rupture_latches_and_new_evaluation_archives_history(self):
        demo = load_module(
            "examples/nra_ide_demo14_powergrid_2026-03-21.py",
            "legacy_demo14_for_test",
        )
        grid = demo.PowerGridNRA()
        grid.fsm = demo.FSMState.RUPTURE_BOUNDARY
        grid.channel.R = 0.1
        grid._recover = True
        grid._update_fsm()
        self.assertEqual(grid.fsm, demo.FSMState.RUPTURE_BOUNDARY)

        grid.history.append({"fsm": "RUPTURE_BOUNDARY"})
        grid.start_new_evaluation()
        self.assertEqual(grid.fsm, demo.FSMState.PERMIT)
        self.assertEqual(grid.archived_histories[-1]["final_state"], "RUPTURE_BOUNDARY")
        self.assertEqual(grid.archived_histories[-1]["history"][-1]["fsm"], "RUPTURE_BOUNDARY")

    def test_clinical_rupture_survives_intervention_and_archives_old_history(self):
        demo = load_module(
            "examples/nra_ide_demo15_or_icu_2026-03-21.py",
            "legacy_demo15_for_test",
        )
        vital = demo.VitalSignNRA()
        vital.fsm = demo.FSMState.RUPTURE_BOUNDARY
        vital.R_total = 0.1
        vital.residual_debt = 0.0
        vital.warmup_pct = 100.0

        vital.trigger_intervene()
        vital._update_fsm(1.0)
        self.assertEqual(vital.fsm, demo.FSMState.RUPTURE_BOUNDARY)

        vital.history.append({"fsm": "RUPTURE_BOUNDARY"})
        vital.start_new_patient_evaluation()
        self.assertEqual(vital.fsm, demo.FSMState.WARMUP)
        self.assertEqual(vital.archived_histories[-1]["final_state"], "RUPTURE_BOUNDARY")

    def test_clinical_html_uses_canonical_rupture_value_and_new_history_entry(self):
        for language in ("EN", "JP"):
            path = REPO_ROOT / "examples" / f"15_or_icu_continuum_{language}.html"
            text = path.read_text(encoding="utf-8-sig")
            self.assertNotRegex(text, r"phase\s*===\s*['\"]CLOSED['\"]")
            self.assertIn("startNewPatientEvaluation", text)
            self.assertIn("archivedHistories", text)

    def test_confession_demo_keeps_fail_closed_as_operational_suppression(self):
        for language in ("EN", "JP"):
            path = REPO_ROOT / "examples" / f"47_FPGA_Demo_SPEED_{language}.html"
            text = path.read_text(encoding="utf-8-sig")
            self.assertIn("Fail-Closed suppression", text)
            self.assertNotIn("FAIL_CLOSED", text)


if __name__ == "__main__":
    unittest.main()
