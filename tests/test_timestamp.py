#!/usr/bin/env python3
import importlib.util
from pathlib import Path

root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("groundcrew_doctor", root / "scripts/groundcrew-doctor.py")
assert spec is not None and spec.loader is not None
doctor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(doctor)
rule = {"type": "string", "format": "date-time"}

cases = {
    "2026-07-12T12:00:00Z": True,
    "2026-07-12T12:00:00.123+01:30": True,
    "2026-07-12T12:00:00.1Z": True,
    "2026-07-12T12:00:00.12+02:00": True,
    "2026-07-12T12:00:00.123456789Z": True,
    "2026-07-12": False,
    "2026-02-30T12:00:00Z": False,
    "2026-07-12T24:00:00Z": False,
    "2026-07-12T12:00:00+01:60": False,
    "2026-07-12T12:00:00+25:00": False,
    "2026-07-12T23:59:60Z": False,
    "2026-07-12t12:00:00Z": False,
}

for value, expected in cases.items():
    errors = []
    doctor.validate_value(value, rule, "$", errors)
    actual = not errors
    assert actual == expected, f"{value}: expected valid={expected}, errors={errors}"

print("timestamp contract tests passed")
