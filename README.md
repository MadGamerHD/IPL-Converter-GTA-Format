**Mass VC→SA IPL Converter**

A simple cross‑platform GUI tool for batch‑converting Grand Theft Auto: Vice City `.ipl` map files into the SA (San Andreas) format. Ideal for modders who need to migrate or reuse Vice City IPLs in San Andreas.

---

## Key Features

* **Graphical Interface**
  Browse for your GTA VC installation folder and select an output directory—no command‑line needed.

* **Recursive File Discovery**
  Automatically scans subdirectories for all `.ipl` files in the chosen input path.

* **Field Extraction & Reformatting**
  Reads each IPL, extracts the essential 9 parameters (object ID, model ID, position XYZ, rotation, interior, player index, and flags), appends a default “-1” for streaming radius, and wraps them between `inst` / `end` markers.

* **Progress Tracking**
  Displays a live progress bar indicating how many files have been processed.

* **Robustness**

  * Skips empty or malformed lines
  * Creates necessary subfolders in the output directory
  * Ignores non‑IPL files

---

## How It Works

1. **Directory Selection**

   * Click **Browse…** under **Input GTA VC Directory** to pick your Vice City game folder.
   * Click **Browse…** under **Output Directory** for where converted files should go.

2. **Batch Conversion**

   * Hitting **Convert All IPL Files** spawns a background thread.
   * The tool walks through every folder under the input path, collecting `.ipl` files.
   * For each file:

     * Reads raw text, normalizes line endings.
     * Parses comma‑separated values, selecting only the fields needed by SA (`object ID, model ID, X, Y, Z, rotation, interior ID, player index, flags`).
     * Prepends `inst`, appends `end`, and writes the reformatted file to the corresponding path under the output directory.

3. **Completion**

   * Upon finishing, a pop‑up confirms the total number of files converted.

---

## Requirements

* Python 3.x
* `tkinter` (usually bundled with Python)

---

## Usage

1. Install Python 3 if you haven’t already.
2. Save the script and run:

   ```bash
   python3 mass_ipl_converter.py
   ```
3. Follow the GUI prompts to select folders and watch the conversion proceed.
