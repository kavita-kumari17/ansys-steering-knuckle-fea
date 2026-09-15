# FEA-Based Structural & Modal Analysis of a Steering Knuckle

Static structural and modal finite-element analysis of an automotive **front steering knuckle**, performed in **ANSYS Workbench** with geometry prepared in **ANSYS SpaceClaim**. The study validates the component against braking and cornering load cases, verifies the mesh through a convergence study, extracts the first six natural frequencies, and drives a lightweighting iteration that reduces mass by **12%** while holding a target factor of safety of **1.5**.

> CAE Project Engineer portfolio project — full pre-processing → solve → post-processing → reporting workflow.

---

## 1. Objective

The steering knuckle carries the vertical wheel load and transmits braking and cornering forces between the suspension and the wheel hub. The goals of this project were to:

1. Prepare and de-feature the CAD geometry for a clean, high-quality solid mesh.
2. Establish a **mesh-converged** stress result (peak stress stable to within 3%).
3. Evaluate structural strength under **braking** and **cornering** load cases (von Mises stress, total deformation, factor of safety).
4. Extract the first six **natural frequencies** via modal analysis to check for resonance in the operating range.
5. Iterate the geometry to **reduce mass** without dropping below a factor of safety of 1.5.

## 2. Tools & Methods

| Stage | Tool |
|-------|------|
| Geometry preparation / de-featuring | ANSYS SpaceClaim |
| Meshing (3D tetrahedral) | ANSYS Meshing |
| Static structural & modal solve | ANSYS Workbench (Mechanical) |
| Post-processing & plots | Python (pandas, matplotlib) |

**Material:** Forged Steel — E = 210 GPa, ν = 0.30, ρ = 7850 kg/m³, Yield = 420 MPa.

## 3. Analysis Workflow

### 3.1 Geometry preparation
- Imported the CAD solid and **de-featured** small fillets, logos, and manufacturing marks that do not affect stiffness.
- Extracted clean contact faces for the bearing bore, strut mounts, and steering-arm eye.

### 3.2 Meshing & convergence
- Generated a **3D tetrahedral** mesh with local refinement at fillets and the bearing bore.
- Ran a **mesh convergence study** (see [`data/mesh_convergence.csv`](data/mesh_convergence.csv)); peak von Mises stress changed by **< 3%** below a 2.0 mm element size, so 2.0 mm was selected as the converged mesh.

### 3.3 Materials, contacts & boundary conditions
- Assigned forged-steel properties.
- Defined **frictional contacts** at the bearing bore and bolted interfaces.
- Constrained the strut mount and lower ball-joint; applied wheel-hub reactions.

### 3.4 Load cases
| Case | Description | Applied load |
|------|-------------|--------------|
| Braking | Longitudinal reaction at the wheel centre | 8.5 kN longitudinal + vertical |
| Cornering | Lateral reaction during a hard turn | 6.0 kN lateral + vertical |

### 3.5 Solve
- **Static structural** for each load case (von Mises stress, total deformation).
- **Modal analysis** (free-free / mounted) for the first six modes.

## 4. Results

### Static structural (governing = braking case)
| Metric | Baseline | Optimized (−12% mass) |
|--------|----------|-----------------------|
| Mass (kg) | 2.86 | 2.52 |
| Max von Mises (MPa) | 236.2 | 248.9 |
| Max deformation (mm) | 0.457 | 0.489 |
| Factor of safety | 1.78 | 1.69 |

The optimized design keeps the factor of safety comfortably above the **1.5** target while removing **12%** of the mass.

### Modal (first six natural frequencies)
See [`data/modal_frequencies.csv`](data/modal_frequencies.csv). The first natural frequency (**~843 Hz**) sits well above the dominant road/suspension excitation range, so resonance is not a concern.

### Mesh convergence
![Mesh convergence plot](images/mesh_convergence.png)

*(Generate this plot locally with the script in section 5.)*

## 5. Reproduce the Post-Processing

```bash
cd scripts
pip install -r requirements.txt
python mesh_convergence.py     # plots stress/deformation vs element count -> images/mesh_convergence.png
python results_summary.py      # prints modal + static-result summary tables
```

## 6. Repository Structure

```
ansys-steering-knuckle-fea/
├── README.md
├── LICENSE
├── .gitignore
├── report/
│   └── CAE_Report_Steering_Knuckle.md   # full written CAE report
├── scripts/
│   ├── mesh_convergence.py
│   ├── results_summary.py
│   └── requirements.txt
├── data/
│   ├── mesh_convergence.csv
│   ├── modal_frequencies.csv
│   └── results_comparison.csv
├── geometry/
│   └── README.md                        # note on CAD source files
└── images/
    └── README.md                        # where result screenshots go
```

## 7. Notes
- Native solver files (`.wbpj`, ANSYS databases) and full CAD are large/proprietary and are **not** committed; this repository documents the methodology, result data, and post-processing so the study is fully reproducible in principle.
- Result values are the outcome of this analysis and are provided as CSVs for transparency and plotting.

## Author
**Kavita Kumari** — B.Tech Civil Engineering, VSSUT
GitHub: [kavita-kumari17](https://github.com/kavita-kumari17) · LinkedIn: [Kavita Kumari](https://tinyurl.com/kavita-kumari17)

Released under the [MIT License](LICENSE).
