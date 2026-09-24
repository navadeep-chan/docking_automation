# AutoDock Vina Automated Blind Docking

## Overview
This Python script automates blind molecular docking using AutoDock Vina. It processes prepared receptor and ligand PDBQT files, dynamically calculates the docking box from receptor coordinates, generates Vina configuration files, runs the docking calculations, and organizes the output structures and log files.

## Requirements
- Python 3.x
- AutoDock Vina (`vina.exe`)
- Prepared receptor files in `.pdbqt` format
- Prepared ligand files in `.pdbqt` format
- Windows environment

## Important: Before Running
**Please confirm that AutoDock Vina is already installed on your computer and that `vina.exe` is available.**

Before running the script, please double-check the Vina executable path specified in `auto_docking.py`:

```python
vina_exe = r"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina.exe"
```

If this is **not the same path on your computer**, please edit the `vina_exe` path in `auto_docking.py` to match the location of your `vina.exe`.

## Input
The script will request:
1. Protein folder containing prepared `.pdbqt` files
2. Ligand folder containing prepared `.pdbqt` files
3. Grid-box margin
4. Energy range
5. Exhaustiveness
6. Maximum number of output poses

## Running the Script
Open a terminal in the project directory and run:

```bash
python auto_docking.py
```

Follow the prompts displayed by the script.

## Output
The script automatically creates:
- `config_files/` — AutoDock Vina configuration files
- `results/` — docking results for each protein–ligand combination
  - `structures/` — output docked poses (`.pdbqt`)
  - `logs/` — Vina log files

## Notes
- Receptor and ligand structures must be properly prepared PDBQT files before running the script.
- The docking box is calculated automatically from the receptor atomic coordinates for blind docking.
- The number of docking calculations is determined by the number of proteins × number of ligands.

