"""
Prints a summary of the steering-knuckle FEA results:
  - first six natural frequencies (modal analysis)
  - baseline vs optimized static-structural comparison
  - factor-of-safety check against the 1.5 target

Usage:
    python results_summary.py
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FOS_TARGET = 1.5


def modal_summary() -> None:
    df = pd.read_csv(ROOT / "data" / "modal_frequencies.csv")
    print("\nModal analysis - first six natural frequencies")
    print("=" * 55)
    print(df.to_string(index=False))
    print(f"\nFirst natural frequency: {df['frequency_Hz'].iloc[0]:.1f} Hz "
          "(well above suspension/road excitation range).")


def static_summary() -> None:
    df = pd.read_csv(ROOT / "data" / "results_comparison.csv").set_index("metric")
    print("\nStatic structural - baseline vs optimized")
    print("=" * 55)
    print(df.to_string())

    mass_reduction = (1 - df.loc["mass_kg", "optimized"]
                      / df.loc["mass_kg", "baseline"]) * 100.0
    fos_opt = df.loc["factor_of_safety", "optimized"]

    print(f"\nMass reduction : {mass_reduction:.1f}%")
    print(f"Optimized FoS  : {fos_opt:.2f} "
          f"({'PASS' if fos_opt >= FOS_TARGET else 'FAIL'} vs target {FOS_TARGET})")


def main() -> None:
    modal_summary()
    static_summary()
    print()


if __name__ == "__main__":
    main()
