"""Research-only regression checks for invalid-result handling."""

import contextlib
import io
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "30_Test_Data"))
sys.path.insert(0, str(PROJECT / "20_Software_Host"))

import nra_core_model as core
from clinical_report_generator import ClinicalReportGenerator
from fpga_interface import FPGAInterface
from main import NRA_IDEMaster
from patient_data_validator import PatientDataValidator
from safety_map_visualizer import SafetyMapVisualizer
import run_validation


SAMPLE = {
    "patient_id": "P001_SAMPLE",
    "cancer_type": "Type A",
    "cell_stiffness": 1.5,
    "cell_viscosity": 0.05,
    "cell_diameter": 12.0,
    "pore_size": 8.0,
    "flow_dp": 0.6,
    "drug_boost": 0.0,
}


class SafetyGuardsTest(unittest.TestCase):
    def test_nondefault_velocity_rejected_before_hardware_io(self):
        interface = FPGAInterface.__new__(FPGAInterface)
        interface.serial = object()  # Any I/O attempt would fail this test.
        result = interface.send_query({**SAMPLE, "deform_velocity": 0}, "Type A")
        self.assertEqual(result["error_code"], core.ERR_UNSUPPORTED_INPUT)
        self.assertFalse(result["is_jammed"])

    def test_type_b_has_no_valid_map(self):
        with self.assertRaisesRegex(ValueError, "INVALID"):
            SafetyMapVisualizer().generate_map(
                {**SAMPLE, "cancer_type": "Type B"}, "unused.png")

    def test_invalid_input_has_no_passable_map(self):
        with self.assertRaisesRegex(ValueError, "INVALID"):
            SafetyMapVisualizer().generate_map(
                {**SAMPLE, "cell_viscosity": 0}, "unused.png")
        with self.assertRaisesRegex(ValueError, "INVALID"):
            SafetyMapVisualizer().generate_map(
                {**SAMPLE, "drug_boost": 20}, "unused.png")

    def test_standalone_report_invalidates_fpga_discrepancy(self):
        expected = core.evaluate(SAMPLE)
        wrong = {"is_jammed": not expected["is_jammed"], "error_code": 0}
        report = ClinicalReportGenerator().generate(SAMPLE, wrong, source="FPGA")
        self.assertIn("Judgement : INVALID", report)
        self.assertIn("ERR_DISCREPANCY", report)

    def test_session_rejects_discrepancy_and_skips_map(self):
        system = NRA_IDEMaster.__new__(NRA_IDEMaster)
        system.fpga = SimpleNamespace(
            serial=object(),
            send_query=lambda data, kind: {
                "is_jammed": not core.evaluate(data, kind)["is_jammed"],
                "error_code": core.ERR_NONE,
            },
        )
        system.validator = PatientDataValidator()
        system.generator = ClinicalReportGenerator()
        system.visualizer = SafetyMapVisualizer()
        saved = []
        maps = []
        system.generator.save = lambda report, path: saved.append(report)
        system.visualizer.generate_map = lambda data, path: maps.append(path)
        with contextlib.redirect_stdout(io.StringIO()):
            ok = system.run_clinical_session(
                str(PROJECT / "30_Test_Data" / "sample_patient_data.json"),
                "unused",
            )
        self.assertFalse(ok)
        self.assertEqual(maps, [])
        self.assertEqual(len(saved), 1)
        self.assertIn("Judgement : INVALID", saved[0])
        self.assertIn("ERR_DISCREPANCY", saved[0])

    def test_validation_runner_fails_on_wrong_result(self):
        wrong_backend = SimpleNamespace(
            send_query=lambda data, kind: {
                "is_jammed": False,
                "error_code": core.ERR_COMM,
            }
        )
        with patch.object(run_validation, "FPGAInterface", return_value=wrong_backend):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertFalse(run_validation.run_automated_test())


if __name__ == "__main__":
    unittest.main()
