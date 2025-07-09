## 🛠️ GTA III/VC to San Andreas IDE/IPL Converter

This tool is designed to convert GTA III and Vice City `.ide` and `.ipl` files into a format compatible with GTA San Andreas. It automatically processes all supported sections and ensures clean, game-ready output with no formatting issues.

### 🔄 What It Does

* **Converts `.ide` and `.ipl` files** from GTA III/VC format to San Andreas format.
* **Supports key IDE sections**:

  * `objs` – Object definitions
  * `tobj` – Timed objects
  * `peds` – Pedestrian models
  * `hier` – Hierarchy/object structure
* **Processes `inst` sections** in `.ipl` files, updating position, rotation, interior, and flags correctly for San Andreas.
* **Automatically adjusts formatting**, removes extra blank lines, and ensures proper `end` blocks.

### 📁 Features

* Batch converts all `.ide` and `.ipl` files in a selected folder.
* Maintains original folder structure in the output directory.
* No extra dependencies – runs as a standalone desktop application.
* User-friendly interface built with Tkinter.
* Progress bar included for large conversions.

### ✅ Output Format

* Compatible with San Andreas engine specifications.
* Ensures consistent formatting with Windows-style line endings.
* Only includes one `end` per section, with no trailing empty lines.

### 💡 Ideal For

* Modders porting maps or models from GTA III or Vice City to San Andreas.
* Developers working on GTA engines or tools needing IDE/IPL compatibility.
* Clean file preparation before importing into map editors like MEd or Moo Mapper.
