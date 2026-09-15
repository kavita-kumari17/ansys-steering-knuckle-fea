# CAE Project Report — Steering Knuckle
**Static Structural & Modal Analysis (ANSYS Workbench)**

**Author:** Kavita Kumari · **Component:** Front steering knuckle · **Solver:** ANSYS Workbench (Mechanical)

---

## 1. Introduction
The steering knuckle is a safety-critical suspension component that supports the wheel hub and bearing while reacting braking, cornering, and vertical road loads. Failure or excessive deflection directly affects steering geometry and vehicle stability. This report documents a finite-element study to (a) confirm structural adequacy under representative load cases, (b) check dynamic behaviour via modal analysis, and (c) reduce mass while retaining an adequate factor of safety.

## 2. Geometry & Idealisation
The CAD solid was imported into **ANSYS SpaceClaim** and cleaned:
- Removed cosmetic fillets, text, and casting marks (de-featuring) that do not affect global stiffness.
- Split faces to create well-defined contact and load-application regions (bearing bore, strut mount, lower ball-joint, steering-arm eye).
- Verified a watertight solid suitable for tetrahedral meshing.

## 3. Material
| Property | Value |
|----------|-------|
| Material | Forged steel |
| Young's modulus, E | 210 GPa |
| Poisson's ratio, ν | 0.30 |
| Density, ρ | 7850 kg/m³ |
| Yield strength, σy | 420 MPa |

## 4. Mesh & Convergence
A **3D tetrahedral** mesh was used with local refinement at fillets and the bearing bore. A convergence study reduced the element size from 5.0 mm to 1.2 mm:

| Element size (mm) | Elements | Max von Mises (MPa) | Δ vs previous |
|-------------------|----------|---------------------|---------------|
| 5.0 | 42,150 | 198.4 | — |
| 4.0 | 68,420 | 212.7 | +7.2% |
| 3.0 | 121,300 | 224.1 | +5.4% |
| 2.5 | 189,600 | 231.6 | +3.3% |
| 2.0 | 312,400 | 236.2 | +2.0% |
| 1.5 | 548,900 | 238.5 | +1.0% |
| 1.2 | 812,300 | 239.3 | +0.3% |

Peak stress stabilised to **within 3%** at and below a **2.0 mm** element size, which was selected as the production mesh (balancing accuracy and solve cost).

## 5. Boundary Conditions & Load Cases
- **Constraints:** strut-mount face and lower ball-joint fixed/pinned as appropriate.
- **Contacts:** frictional contact at the bearing bore and bolted interfaces.

| Load case | Description | Applied load |
|-----------|-------------|--------------|
| Braking | Longitudinal + vertical reaction at wheel centre | 8.5 kN |
| Cornering | Lateral + vertical reaction during hard turn | 6.0 kN |

## 6. Results

### 6.1 Static structural
The **braking** case governed. For the baseline design the peak von Mises stress was **236.2 MPa** with a maximum deformation of **0.457 mm**, giving a factor of safety of **420 / 236.2 = 1.78**.

### 6.2 Modal
| Mode | Frequency (Hz) | Shape |
|------|----------------|-------|
| 1 | 842.6 | First bending |
| 2 | 1187.3 | First torsion |
| 3 | 1564.9 | Second bending |
| 4 | 2103.7 | Lateral bending |
| 5 | 2456.1 | Second torsion |
| 6 | 2894.5 | Combined bending-torsion |

The lowest natural frequency (~843 Hz) is far above the dominant road/suspension excitation band, so resonance risk is low.

### 6.3 Lightweighting iteration
Material was removed from low-stress regions (web thinning and rib re-profiling) and the model re-solved:

| Metric | Baseline | Optimized |
|--------|----------|-----------|
| Mass (kg) | 2.86 | 2.52 |
| Max von Mises (MPa) | 236.2 | 248.9 |
| Factor of safety | 1.78 | 1.69 |

Result: **12% mass reduction** with the factor of safety maintained **above the 1.5 target**.

## 7. Conclusions
1. The baseline knuckle is structurally adequate (FoS 1.78) under the governing braking case.
2. Modal behaviour is acceptable — no resonance in the operating range.
3. A 12% lighter design is feasible while retaining FoS ≥ 1.5.

## 8. Recommendations / Future Work
- Add a fatigue (S-N) assessment for cyclic braking/cornering loads.
- Include a combined braking + cornering load case for a worst-case envelope.
- Validate the optimized design with a physical or higher-fidelity nonlinear contact model.
