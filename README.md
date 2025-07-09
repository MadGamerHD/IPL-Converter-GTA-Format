**Mass III/VC → SA IPL & IDE Converter**
A standalone GUI tool for batch‑converting Grand Theft Auto III and Vice City map placement and definition files into San Andreas–compatible formats.

---

## How it works

1. **Directory Selection**

   * **Input**: Point the tool at a directory containing `.ipl` (Item Placement) and `.ide` (Item Definition) files from GTA III or Vice City.
   * **Output**: Choose an empty (or existing) folder where the converted San Andreas files will be written, preserving sub‑directory structure.

2. **Batch Processing**

   * Recursively scans the input folder for all `.ipl` and `.ide` files.
   * Displays a progress bar indicating total files and conversion progress.
   * Runs file conversions on a background thread to keep the UI responsive.

3. **IPL Conversion**

   * **GTA III `.ipl`** (12‑field):

     * Fields: `ID, ModelName, PosX, PosY, PosZ, ScaleX, ScaleY, ScaleZ, RotX, RotY, RotZ, RotW`
     * Converts to San Andreas format:

       ```
       inst
       ID, ModelName, 0, PosX, PosY, PosZ, RotX, RotY, RotZ, RotW, -1
       …  
       end
       ```

       * Sets **interior** to `0` (default)
       * Skips scale (SA does not support per-instance scaling)
       * Appends LOD index `-1`

   * **Vice City `.ipl`** (13+ field):

     * Fields: `ID, ModelName, Interior, PosX, PosY, PosZ, ScaleX, ScaleY, ScaleZ, RotX, RotY, RotZ, RotW`
     * Converts to San Andreas format:

       ```
       inst
       ID, ModelName, Interior, PosX, PosY, PosZ, RotX, RotY, RotZ, RotW, -1
       …  
       end
       ```

       * Preserves **Interior** value
       * Skips scale
       * Sets LOD index to `-1`

4. **IDE Conversion**

   * Parses and converts the following sections, handling GTA III and VC variants into SA equivalents:

     * **`objs`** (map object definitions):

       * Type 1–3 entries copied directly
       * Single-mesh entries optionally rewritten to SA “Type 4” (dropping mesh count)
     * **`tobj`** (timed objects):

       * Type 1–3 entries copied directly
       * Single-mesh entries optionally rewritten to SA “Type 4” (dropping mesh count)
     * **`hier`** (cutscene object list): copied identically
     * **`peds`** (pedestrian definitions):

       * GTA III entries extended with default SA fields (`Flags=0`, empty voice, etc.)
       * Vice City entries preserve anim & radio fields and fill SA‑only fields with defaults

   * All other sections, comments, and unsupported entries are passed through unchanged.

5. **Output**

   * Writes each converted file to the matching relative path under the output directory.
   * Ensures all intermediate directories exist before writing.
   * Upon completion, notifies the user of total files converted.

---

**Requirements:**

* Python 3.x
* `tkinter` for the GUI

Just run the script, select your source and target directories, and click **Convert All IPL & IDE Files** to migrate your GTA III/VC map data to San Andreas format.
