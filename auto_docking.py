import os
import subprocess

def calculate_blind_box(file_path, margin):

    x_coords, y_coords, z_coords = [], [], []
     
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith(("ATOM", "HETATM")):
                    x_coords.append(float(line[30:38]))
                    y_coords.append(float(line[38:46]))
                    z_coords.append(float(line[46:54]))

        if not x_coords:
            raise ValueError(f"No ATOM/HETATM coordinates found in {file_path}")

        xmin, xmax = min(x_coords), max(x_coords)
        ymin, ymax = min(y_coords), max(y_coords)
        zmin, zmax = min(z_coords), max(z_coords)


        return {
            "center_x": round((xmin + xmax) / 2, 3),
            "center_y": round((ymin + ymax) / 2, 3),
            "center_z": round((zmin + zmax) / 2, 3),
            "size_x": round((xmax - xmin) + margin, 3),
            "size_y": round((ymax - ymin) + margin, 3),
            "size_z": round((zmax - zmin) + margin, 3)
        }
    except Exception as e:
        print(f"[ERROR] Failed to calculate grid box for {file_path}: {e}")
        return None

# user inputs------------------------------------------------------------------

print("--- AutoDock Vina Blind Docking Setup ---")
protein_folder = input("Enter the folder path containing prepared proteins (.pdbqt): ").strip('"')
ligand_folder = input("Enter the folder path containing prepared ligands (.pdbqt): ").strip('"')

margin = float(input("Enter the grid box margin for blind docking (angstrom 1/2): "))
energy_range = int(input("Energy range: "))
exhaustiveness = int(input("Exhaustiveness / Search effort: "))
num_modes = int(input("Number of poses to output: "))

# system installed autodock vina path
vina_exe = r"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina.exe"

# folder setup-------------------------------------------------------------------------

config_folder = "config_files"
results_folder = "results"

os.makedirs(config_folder, exist_ok=True)
os.makedirs(results_folder, exist_ok=True)

proteins = [f for f in os.listdir(protein_folder) if f.endswith('.pdbqt')]
ligands = [f for f in os.listdir(ligand_folder) if f.endswith('.pdbqt')]

# pipeline-----------------------------------------------------------------------------------

for prot_file in proteins:
    prot_path = os.path.join(protein_folder, prot_file)
    prot_name = os.path.splitext(prot_file)[0]
    
    print(f"\nAnalyzing protein: {prot_name}")
    box = calculate_blind_box(prot_path, margin)
    
    if not box:
        print(f"[SKIP] Skipping {prot_name} due to grid box calculation failure.")
        continue

    for lig_file in ligands:
        lig_path = os.path.join(ligand_folder, lig_file)
        lig_name = os.path.splitext(lig_file)[0]
        
        pair_name = f"{prot_name}_{lig_name}"
        print(f"  -> Preparing docking for: {pair_name}")
        
        pair_dir = os.path.join(results_folder, pair_name)
        struct_dir = os.path.join(pair_dir, "structures")
        log_dir = os.path.join(pair_dir, "logs")
        
        os.makedirs(struct_dir, exist_ok=True)
        os.makedirs(log_dir, exist_ok=True)

        config_filename = f"{pair_name}_config.txt"
        config_path = os.path.join(config_folder, config_filename)

        config_text = (
            f"receptor = {prot_path}\n"
            f"ligand = {lig_path}\n\n"
            f"center_x = {box['center_x']}\n"
            f"center_y = {box['center_y']}\n"
            f"center_z = {box['center_z']}\n\n"
            f"size_x = {box['size_x']}\n"
            f"size_y = {box['size_y']}\n"
            f"size_z = {box['size_z']}\n\n"
            f"energy_range = {energy_range}\n"
            f"exhaustiveness = {exhaustiveness}\n"
            f"num_modes = {num_modes}\n"
        )
        
        try:
            with open(config_path, 'w') as config_file:
                config_file.write(config_text)
        except Exception as e:
            print(f"[ERROR] Could not write config file for {pair_name}: {e}")
            continue

        output_pdbqt = os.path.join(struct_dir, f"{pair_name}_out.pdbqt")
        log_file = os.path.join(log_dir, f"{pair_name}_log.txt")
        
        cmd = [
            vina_exe,
            "--config", config_path,
            "--out", output_pdbqt,
            "--log", log_file
        ]
        
        print(f"     Running Vina for {pair_name}...")
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"     [SUCCESS] Completed {pair_name}")
        except subprocess.CalledProcessError as e:
            print(f"     [CRITICAL ERROR] Vina crashed for {pair_name}.")
            print(f"     Vina Output: {e.stderr}")
        except FileNotFoundError:
            print(f"     [CRITICAL ERROR] Could not find vina.exe at: {vina_exe}")
            print("     Please verify the installation path.")
            break
print("\n\n====================================")
print("Pipeline execution finished")
print("====================================")