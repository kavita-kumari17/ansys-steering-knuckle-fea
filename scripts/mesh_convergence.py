"""
Mesh convergence post-processing for the steering-knuckle FEA.

Reads data/mesh_convergence.csv, computes the percentage change in peak
von Mises stress between successive refinements, identifies the converged
element size (< 3% change), and saves a convergence plot to images/.

Usage:
    python mesh_convergence.py
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "mesh_convergence.csv"
IMAGES = ROOT / "images"
CONVERGENCE_TOL = 3.0  # percent


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    # Finer meshes first (largest element count last -> sort by element count)
    df = df.sort_values("num_elements").reset_index(drop=True)
    df["stress_pct_change"] = df["max_von_mises_MPa"].pct_change() * 100.0
    return df


def find_converged(df: pd.DataFrame):
    """Return the first row whose |stress % change| drops below the tolerance."""
    converged = df[df["stress_pct_change"].abs() < CONVERGENCE_TOL]
    if converged.empty:
        return None
    return converged.iloc[0]


def make_plot(df: pd.DataFrame) -> Path:
    IMAGES.mkdir(exist_ok=True)
    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.plot(df["num_elements"] / 1000, df["max_von_mises_MPa"],
             "o-", color="#1f4e79", label="Max von Mises")
    ax1.set_xlabel("Number of elements (thousands)")
    ax1.set_ylabel("Max von Mises stress (MPa)", color="#1f4e79")
    ax1.tick_params(axis="y", labelcolor="#1f4e79")
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(df["num_elements"] / 1000, df["max_deformation_mm"],
             "s--", color="#c0392b", label="Max deformation")
    ax2.set_ylabel("Max deformation (mm)", color="#c0392b")
    ax2.tick_params(axis="y", labelcolor="#c0392b")

    plt.title("Steering Knuckle — Mesh Convergence Study")
    fig.tight_layout()
    out = IMAGES / "mesh_convergence.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def main() -> None:
    df = load_data()
    print("\nMesh convergence study")
    print("=" * 60)
    print(df.to_string(index=False,
                       formatters={"stress_pct_change": lambda v: f"{v:6.2f}%"
                                   if pd.notna(v) else "    - "}))

    row = find_converged(df)
    if row is not None:
        print("\nConverged mesh (stress change < %.1f%%):" % CONVERGENCE_TOL)
        print(f"  Element size : {row['element_size_mm']} mm")
        print(f"  Elements     : {int(row['num_elements']):,}")
        print(f"  Peak stress  : {row['max_von_mises_MPa']} MPa")
    else:
        print("\nNo converged mesh found within tolerance.")

    out = make_plot(df)
    print(f"\nSaved plot -> {out.relative_to(ROOT)}\n")


if __name__ == "__main__":
    main()
