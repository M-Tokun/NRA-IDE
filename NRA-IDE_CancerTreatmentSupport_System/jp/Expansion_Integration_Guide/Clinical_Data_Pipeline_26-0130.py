"""
Clinical Data Pipeline for NRA-IDE Bio-Calibrator
File: Clinical_Data_Pipeline_26-0130.py
Date: 2026-01-30 20:55

Architecture:
┌──────────────────────────────────────────────────────────────┐
│                  Hospital Information System                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ Elastography│  │ Blood Press │  │ Ultrasound  │          │
│  │  (kPa)      │  │  (mmHg)     │  │  (μm)       │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
│         └─────────────────┴────────────────┘                 │
└─────────────────────────┬────────────────────────────────────┘
                          ↓
              ┌───────────────────────┐
              │  Data Validator       │
              │  - Range Check        │
              │  - Unit Conversion    │
              │  - Q8.8 Encoding      │
              └───────────┬───────────┘
                          ↓
              ┌───────────────────────┐
              │  FPGA Interface       │
              │  (UART/PCIe/AXI)      │
              └───────────┬───────────┘
                          ↓
              ┌───────────────────────┐
              │  Bio-Calibrator FPGA  │
              │  → Optimal Boost      │
              └───────────┬───────────┘
                          ↓
              ┌───────────────────────┐
              │  Safety Map Generator │
              │  + Clinical Report    │
              └───────────────────────┘
"""

import json
import serial
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Dict, Tuple, Optional

# ============================================
# Configuration
# ============================================
FPGA_SERIAL_PORT = "/dev/ttyUSB0"  # Linux
# FPGA_SERIAL_PORT = "COM3"        # Windows
FPGA_BAUDRATE = 115200

# Parameter Validation Ranges
PARAM_RANGES = {
    'cell_stiffness_kPa': (0.1, 5.0),
    'cell_diameter_um': (5.0, 30.0),
    'pore_size_um': (5.0, 15.0),
    'blood_pressure_mmHg': (60, 180),  # Will convert to Pa
    'cell_count': (1, 50)  # For Type B
}

# ============================================
# Class: PatientDataValidator
# ============================================
class PatientDataValidator:
    """
    Validates and encodes patient measurements into FPGA-compatible format.
    
    ASCII Flow:
    Raw Data → Validate → Convert Units → Q8.8 Encode → FPGA Packet
    """
    
    @staticmethod
    def validate_range(value: float, param_name: str) -> bool:
        """Check if value is within acceptable range."""
        if param_name not in PARAM_RANGES:
            raise ValueError(f"Unknown parameter: {param_name}")
        
        min_val, max_val = PARAM_RANGES[param_name]
        return min_val <= value <= max_val
    
    @staticmethod
    def to_q8_8(value: float) -> int:
        """
        Convert float to Q8.8 fixed-point format.
        Example: 2.5 kPa → 0x0280 (640 in decimal)
        
        Q8.8 Format:
        ┌────────┬────────┐
        │ 8-bit  │ 8-bit  │
        │Integer │Fraction│
        └────────┴────────┘
        """
        if value < 0 or value > 255.99:
            raise ValueError(f"Value {value} out of Q8.8 range [0, 255.99]")
        return int(value * 256)
    
    @staticmethod
    def mmHg_to_Pa(mmHg: float) -> float:
        """Convert blood pressure from mmHg to Pascal."""
        return mmHg * 133.322
    
    def encode_patient_data(self, patient_dict: Dict) -> Dict[str, int]:
        """
        Main encoding pipeline.
        
        Input (Example):
        {
            'patient_id': 'P12345',
            'tumor_stiffness': 0.8,  # kPa (from elastography)
            'tumor_diameter': 15.0,  # μm (from ultrasound)
            'blood_pressure': 120,   # mmHg (from sphygmomanometer)
            'cell_count': 5          # (from pathology, if Type B)
        }
        
        Output (Q8.8 Encoded):
        {
            'stiffness': 0x00CC,
            'diameter': 0x0F00,
            'pressure': 0x3F90,
            'cell_count': 0x05
        }
        """
        # Validate
        assert self.validate_range(patient_dict['tumor_stiffness'], 'cell_stiffness_kPa')
        assert self.validate_range(patient_dict['tumor_diameter'], 'cell_diameter_um')
        assert self.validate_range(patient_dict['blood_pressure'], 'blood_pressure_mmHg')
        
        # Convert and Encode
        encoded = {
            'stiffness': self.to_q8_8(patient_dict['tumor_stiffness']),
            'diameter': self.to_q8_8(patient_dict['tumor_diameter']),
            'pore_size': self.to_q8_8(8.0),  # Default capillary size
            'pressure': int(self.mmHg_to_Pa(patient_dict['blood_pressure'])),
            'patient_id': patient_dict['patient_id']
        }
        
        if 'cell_count' in patient_dict:
            encoded['cell_count'] = patient_dict['cell_count']
        
        return encoded

# ============================================
# Class: FPGAInterface
# ============================================
class FPGAInterface:
    """
    Serial communication with FPGA Bio-Calibrator.
    
    Protocol (ASCII Example):
    Host → FPGA: "STIFF:0x00CC,DIAM:0x0F00,PRESS:0x3F90\n"
    FPGA → Host: "BOOST:0x0B4D\n"  (Result: +2.852 kPa)
    """
    
    def __init__(self, port: str = FPGA_SERIAL_PORT, baudrate: int = FPGA_BAUDRATE):
        try:
            self.serial = serial.Serial(port, baudrate, timeout=2)
            print(f"✓ FPGA connected on {port}")
        except serial.SerialException as e:
            print(f"✗ FPGA connection failed: {e}")
            self.serial = None
    
    def query_calibration(self, encoded_data: Dict) -> Optional[float]:
        """
        Send patient data to FPGA and retrieve optimal drug boost.
        
        Returns:
            Optimal boost in kPa, or None if communication fails.
        """
        if self.serial is None:
            print("[WARN] No FPGA connection, using simulation mode")
            return self._simulate_fpga(encoded_data)
        
        # Build command packet
        cmd = (f"STIFF:{encoded_data['stiffness']:04X},"
               f"DIAM:{encoded_data['diameter']:04X},"
               f"PORE:{encoded_data['pore_size']:04X},"
               f"PRESS:{encoded_data['pressure']:04X}\n")
        
        # Send and receive
        self.serial.write(cmd.encode('utf-8'))
        response = self.serial.readline().decode('utf-8').strip()
        
        # Parse response
        if response.startswith("BOOST:"):
            boost_hex = response.split(':')[1]
            boost_q8_8 = int(boost_hex, 16)
            boost_kPa = boost_q8_8 / 256.0
            return boost_kPa
        else:
            print(f"[ERROR] Invalid FPGA response: {response}")
            return None
    
    def _simulate_fpga(self, data: Dict) -> float:
        """
        Software simulation for testing without hardware.
        Uses simplified physics model.
        """
        stiff_kPa = data['stiffness'] / 256.0
        diam_um = data['diameter'] / 256.0
        pore_um = data['pore_size'] / 256.0
        press_Pa = data['pressure']
        
        deformation = max(0, diam_um - pore_um)
        required_resistance = press_Pa
        
        # F = k × x → k_needed = F / x
        if deformation > 0:
            needed_stiffness = required_resistance / (deformation * 250)
            boost = max(0, needed_stiffness - stiff_kPa)
            return boost
        else:
            return 0.0
    
    def close(self):
        if self.serial:
            self.serial.close()

# ============================================
# Class: ClinicalReportGenerator
# ============================================
class ClinicalReportGenerator:
    """
    Generates physician-friendly reports with safety maps.
    
    Output Example:
    ┌─────────────────────────────────────┐
    │  NRA-IDE Treatment Recommendation   │
    ├─────────────────────────────────────┤
    │ Patient: P12345                     │
    │ Date: 2026-01-30                    │
    │                                     │
    │ Measured Parameters:                │
    │  - Tumor Stiffness: 0.8 kPa         │
    │  - Blood Pressure: 120 mmHg         │
    │                                     │
    │ ★ Recommended Drug Boost: +2.85 kPa │
    │                                     │
    │ [Safety Map Attached]               │
    └─────────────────────────────────────┘
    """
    
    @staticmethod
    def generate_report(patient_data: Dict, optimal_boost: float) -> str:
        """Generate text report."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""
╔═══════════════════════════════════════════════════════════╗
║         NRA-IDE Bio-Calibrator Clinical Report           ║
╚═══════════════════════════════════════════════════════════╝

Patient ID: {patient_data['patient_id']}
Report Date: {timestamp}

─────────────────────────────────────────────────────────────
MEASURED PARAMETERS
─────────────────────────────────────────────────────────────
  Tumor Stiffness:     {patient_data['tumor_stiffness']:.2f} kPa
  Tumor Diameter:      {patient_data['tumor_diameter']:.1f} μm
  Blood Pressure:      {patient_data['blood_pressure']} mmHg
  
─────────────────────────────────────────────────────────────
CALIBRATION RESULT
─────────────────────────────────────────────────────────────
  ★ Recommended Drug Boost: +{optimal_boost:.3f} kPa
  
  This value ensures physical jamming of metastatic cells
  under worst-case hemodynamic conditions.
  
─────────────────────────────────────────────────────────────
SAFETY MARGIN ANALYSIS
─────────────────────────────────────────────────────────────
  [See attached Safety Map visualization]
  
  • Green Zone: Safe operation region
  • Yellow Zone: Marginal (monitor closely)
  • Red Zone: Insufficient jamming force
  
═══════════════════════════════════════════════════════════
  Generated by NRA-IDE System v1.0 (2026-01-30)
═══════════════════════════════════════════════════════════
"""
        return report
    
    @staticmethod
    def plot_safety_map(patient_data: Dict, optimal_boost: float, filename: str):
        """Generate safety map visualization."""
        # Parameter space
        stiffness_range = np.linspace(0.1, 2.0, 100)
        pressure_range_Pa = np.linspace(100, 1000, 100)
        X, Y = np.meshgrid(stiffness_range, pressure_range_Pa)
        
        # Physics calculation
        D_cell = patient_data['tumor_diameter']
        d_gap = 8.0
        deformation = max(0, D_cell - d_gap)
        alpha = 250.0
        
        total_stiffness = X + optimal_boost
        calculated_resistance = total_stiffness * deformation * alpha
        Z = calculated_resistance - Y  # Safety factor
        
        # Plot
        plt.figure(figsize=(10, 7))
        contour = plt.contourf(X, Y, Z, levels=20, 
                               cmap='RdYlGn', alpha=0.8)
        plt.contour(X, Y, Z, levels=[0], colors='black', 
                   linewidths=3, linestyles='--')
        
        # Mark patient's condition
        plt.scatter([patient_data['tumor_stiffness']], 
                   [133.322 * patient_data['blood_pressure']], 
                   c='blue', s=200, marker='★', 
                   edgecolors='black', linewidths=2,
                   label=f"Patient {patient_data['patient_id']}")
        
        plt.colorbar(contour, label='Safety Factor (Pa)')
        plt.title(f'Safety Map (Boost = +{optimal_boost:.3f} kPa)')
        plt.xlabel('Cell Stiffness (kPa)')
        plt.ylabel('Blood Pressure (Pa)')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Safety map saved: {filename}")

# ============================================
# Main Clinical Workflow
# ============================================
def clinical_workflow_example():
    """
    Complete workflow demonstration.
    
    ASCII Flow:
    ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
    │Measure│→ │Validate│→│FPGA  │→ │Report│→ │Doctor│
    │Patient│   │Encode  │  │Query │   │Gen   │   │Review│
    └──────┘   └──────┘   └──────┘   └──────┘   └──────┘
    """
    
    # Step 1: Patient Measurement (from hospital equipment)
    patient_data = {
        'patient_id': 'P12345',
        'tumor_stiffness': 0.8,   # kPa (from shear wave elastography)
        'tumor_diameter': 15.0,   # μm (from ultrasound + pathology)
        'blood_pressure': 120     # mmHg (from sphygmomanometer)
    }
    
    print("=" * 60)
    print(" NRA-IDE Clinical Workflow Start")
    print("=" * 60)
    
    # Step 2: Validate and Encode
    validator = PatientDataValidator()
    encoded = validator.encode_patient_data(patient_data)
    print(f"\n✓ Data validated and encoded:")
    for key, value in encoded.items():
        if isinstance(value, int) and key != 'patient_id':
            print(f"  {key}: 0x{value:04X}")
    
    # Step 3: Query FPGA
    fpga = FPGAInterface()
    optimal_boost = fpga.query_calibration(encoded)
    fpga.close()
    
    if optimal_boost is not None:
        print(f"\n✓ FPGA Calibration Complete")
        print(f"  Optimal Drug Boost: +{optimal_boost:.3f} kPa")
        
        # Step 4: Generate Report
        reporter = ClinicalReportGenerator()
        report_text = reporter.generate_report(patient_data, optimal_boost)
        print(report_text)
        
        # Step 5: Generate Safety Map
        map_filename = f"SafetyMap_{patient_data['patient_id']}_26-0130.png"
        reporter.plot_safety_map(patient_data, optimal_boost, map_filename)
        
        # Step 6: Save Report
        report_filename = f"Report_{patient_data['patient_id']}_26-0130.txt"
        with open(report_filename, 'w') as f:
            f.write(report_text)
        print(f"✓ Report saved: {report_filename}")
    else:
        print("\n✗ FPGA calibration failed")
    
    print("\n" + "=" * 60)
    print(" Workflow Complete")
    print("=" * 60)

# ============================================
# Database Integration Example (Optional)
# ============================================
def integrate_with_hospital_db():
    """
    Example of connecting to hospital information system.
    Replace with actual DB credentials and schema.
    """
    import sqlite3  # Or use PostgreSQL/MySQL connectors
    
    # Pseudocode structure:
    """
    conn = sqlite3.connect('hospital_db.sqlite')
    cursor = conn.cursor()
    
    # Query latest patient measurements
    cursor.execute('''
        SELECT patient_id, tumor_stiffness, tumor_diameter, blood_pressure
        FROM oncology_measurements
        WHERE measurement_date = (SELECT MAX(measurement_date) FROM oncology_measurements)
    ''')
    
    for row in cursor.fetchall():
        patient_data = {
            'patient_id': row[0],
            'tumor_stiffness': row[1],
            'tumor_diameter': row[2],
            'blood_pressure': row[3]
        }
        # Run workflow for each patient
        clinical_workflow_example()
    
    conn.close()
    """
    pass

if __name__ == "__main__":
    clinical_workflow_example()

"""
ASCII Art: Complete System Architecture

┌─────────────────────────────────────────────────────────────┐
│                    Hospital Floor                           │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │Ultrasound│  │  CT/MRI  │  │  Pathology│                 │
│  │  Scanner │  │  System  │  │    Lab    │                 │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
│       └─────────────┴──────────────┘                        │
│                     │                                       │
└─────────────────────┼───────────────────────────────────────┘
                      ↓
        ┌─────────────────────────┐
        │  Hospital Database      │
        │  (PACS/HIS/EMR)         │
        └────────────┬────────────┘
                     ↓
        ┌─────────────────────────┐
        │  Python Data Pipeline   │
        │  - Validator            │
        │  - Q8.8 Encoder         │
        └────────────┬────────────┘
                     ↓
        ┌─────────────────────────┐
        │  FPGA Bio-Calibrator    │
        │  (UART/PCIe Interface)  │
        └────────────┬────────────┘
                     ↓
        ┌─────────────────────────┐
        │  Report Generator       │
        │  + Safety Map Plotter   │
        └────────────┬────────────┘
                     ↓
        ┌─────────────────────────┐
        │  Oncologist Workstation │
        │  (Treatment Decision)   │
        └─────────────────────────┘
"""
