import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class IPLIDEConverterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mass III/VC → SA IPL & IDE Converter")
        self.geometry("600x240")
        self._build_widgets()

    def _build_widgets(self):
        frm = ttk.Frame(self, padding=20)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Input GTA III/VC Directory:").grid(row=0, column=0, sticky=tk.W)
        self.input_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.input_var, width=45).grid(row=0, column=1)
        ttk.Button(frm, text="Browse…", command=self.browse_input).grid(row=0, column=2, padx=5)

        ttk.Label(frm, text="Output Directory:").grid(row=1, column=0, sticky=tk.W)
        self.output_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.output_var, width=45).grid(row=1, column=1)
        ttk.Button(frm, text="Browse…", command=self.browse_output).grid(row=1, column=2, padx=5)

        self.progress = ttk.Progressbar(frm, orient='horizontal', mode='determinate')
        self.progress.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=15)

        ttk.Button(frm, text="Convert All IPL & IDE Files", command=self.start_conversion) \
            .grid(row=3, column=0, columnspan=3, sticky=tk.EW)

        frm.columnconfigure(1, weight=1)

    def browse_input(self):
        path = filedialog.askdirectory(title="Select GTA III/VC directory")
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
        files = []
        for root, _, fnames in os.walk(in_dir):
            for f in fnames:
                ext = f.lower().rsplit('.', 1)[-1]
                if ext in ('ipl', 'ide'):
                    full = os.path.join(root, f)
                    rel  = os.path.relpath(full, in_dir)
                    files.append((full, rel, ext))

        total = len(files)
        if total == 0:
            messagebox.showinfo("No Files", "No .ipl or .ide files found.")
            return

        self.progress['maximum'] = total
        self.progress['value'] = 0

        for src, rel, ext in files:
            try:
                dst = os.path.join(out_dir, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if ext == 'ipl':
                    self.convert_ipl(src, dst)
                elif ext == 'ide':
                    self.convert_ide(src, dst)
            except Exception as e:
                print(f"Error converting {src}: {e}")
            self.progress['value'] += 1

        messagebox.showinfo("Done", f"Converted {total} files to SA format.")

    def convert_ipl(self, src_path, dst_path):
        with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw = f.read().replace('\r\n','\n').replace('\r','\n')
        lines = [l for l in raw.split('\n') if l.strip()]

        out = []
        saw_inst = False
        for line in lines:
            parts = [p.strip() for p in line.split(',')]
            L = len(parts)
            if L == 12:
                if not saw_inst:
                    out.append('inst'); saw_inst = True
                ID,Model = parts[0],parts[1]
                interior = '0'
                pos = parts[2:5]
                rot = parts[8:12]
                lod = '-1'
                out.append(', '.join([ID,Model,interior,*pos,*rot,lod]))
            elif L >= 13:
                if not saw_inst:
                    out.append('inst'); saw_inst = True
                ID,Model = parts[0],parts[1]
                interior = parts[2]
                pos = parts[3:6]
                rot = parts[9:13]
                lod = '-1'
                out.append(', '.join([ID,Model,interior,*pos,*rot,lod]))
        if saw_inst:
            out.append('end')
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write('\r\n'.join(out))

    def convert_ide(self, src_path, dst_path):
        with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.read().replace('\r\n','\n').split('\n')

        out = []
        current = None
        for line in lines:
            l = line.strip()
            if l.lower() in ('objs','tobj','hier','peds'):
                current = l.lower()
                out.append(l)
                continue
            if l.startswith('#') or not l:
                out.append(line)
                continue

            parts = [p.strip() for p in line.split(',')]
            if current == 'objs':
                try:
                    mesh = int(parts[3])
                    if mesh == 1:
                        out.append(f"{parts[0]}, {parts[1]}, {parts[2]}, {parts[4]}, {parts[-1]}")
                    else:
                        out.append(line)
                except:
                    out.append(line)
            elif current == 'tobj':
                try:
                    mesh = int(parts[3])
                    timeon, timeoff = parts[-2], parts[-1]
                    if mesh == 1:
                        out.append(f"{parts[0]}, {parts[1]}, {parts[2]}, {parts[4]}, {parts[-3]}, {timeon}, {timeoff}")
                    else:
                        out.append(line)
                except:
                    out.append(line)
            elif current == 'hier':
                out.append(line)
            elif current == 'peds':
                L = len(parts)
                if L == 7:
                    base = parts
                    flags, anim, r1, r2 = '0', '', '-1', '-1'
                elif L >= 10:
                    base = parts[:7]
                    anim, r1, r2 = parts[7], parts[8], parts[9]
                    flags = '0'
                else:
                    out.append(line)
                    continue
                sa = [*base, flags, anim, r1, r2, '', '', '']
                out.append(', '.join(sa))
            else:
                out.append(line)

        out.append('end')
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write('\r\n'.join(out))

if __name__ == '__main__':
    app = IPLIDEConverterGUI()
    app.mainloop()