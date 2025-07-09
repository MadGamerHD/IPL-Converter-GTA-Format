import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# GUI Application
class IPLConverterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mass VC→SA IPL Converter")
        self.geometry("500x200")
        self._build_widgets()

    def _build_widgets(self):
        frm = ttk.Frame(self, padding=20)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Input GTA VC Directory:").grid(row=0, column=0, sticky=tk.W)
        self.input_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.input_var, width=40).grid(row=0, column=1)
        ttk.Button(frm, text="Browse…", command=self.browse_input).grid(row=0, column=2)

        ttk.Label(frm, text="Output Directory:").grid(row=1, column=0, sticky=tk.W)
        self.output_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.output_var, width=40).grid(row=1, column=1)
        ttk.Button(frm, text="Browse…", command=self.browse_output).grid(row=1, column=2)

        self.progress = ttk.Progressbar(frm, orient='horizontal', mode='determinate')
        self.progress.grid(row=2, column=0, columnspan=3, pady=15, sticky=tk.EW)

        ttk.Button(frm, text="Convert All IPL Files", command=self.start_conversion).grid(
            row=3, column=0, columnspan=3, pady=5, sticky=tk.EW
        )

    def browse_input(self):
        path = filedialog.askdirectory(title="Select GTA VC directory")
        if path:
            self.input_var.set(path)

    def browse_output(self):
        path = filedialog.askdirectory(title="Select output directory")
        if path:
            self.output_var.set(path)

    def start_conversion(self):
        in_dir = self.input_var.get()
        out_dir = self.output_var.get()
        if not os.path.isdir(in_dir) or not os.path.isdir(out_dir):
            messagebox.showerror("Error", "Please select valid input and output directories.")
            return
        threading.Thread(target=self.convert_all, args=(in_dir, out_dir), daemon=True).start()

    def convert_all(self, in_dir, out_dir):
        ipl_files = []
        for root, _, files in os.walk(in_dir):
            for f in files:
                if f.lower().endswith('.ipl'):
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, in_dir)
                    ipl_files.append((full, rel))

        total = len(ipl_files)
        if total == 0:
            messagebox.showinfo("No IPLs", "No .ipl files found in the input directory.")
            return

        self.progress['maximum'] = total
        self.progress['value'] = 0

        for src, rel in ipl_files:
            try:
                dst_path = os.path.join(out_dir, rel)
                self.convert_file(src, dst_path)
            except Exception as e:
                print(f"Error converting {src}: {e}")
            self.progress['value'] += 1

        messagebox.showinfo("Done", f"Converted {total} files.")

    def convert_file(self, src_path, dst_path):
        # Ensure output subfolders
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        out_lines = ['inst']
        for line in lines:
            if not line.strip():
                continue
            parts = line.split(',')
            if len(parts) >= 13:
                selected = [parts[i].strip() for i in [0,1,2,3,4,9,10,11,12]]
                selected.append('-1')
                formatted_line = ', '.join(selected)
                out_lines.append(formatted_line)
        out_lines.append('end')
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write('\r\n'.join(out_lines))

if __name__ == '__main__':
    app = IPLConverterGUI()
    app.mainloop()
