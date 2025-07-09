import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class Converter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GTA III/VC → San Andreas Converter")
        self.geometry("600x240")
        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self, padding=20)
        frm.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frm, text="Input GTA III/VC Directory:").grid(row=0, column=0, sticky=tk.W)
        self.in_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.in_var, width=45).grid(row=0, column=1)
        ttk.Button(frm, text="Browse…", command=self.browse_in).grid(row=0, column=2, padx=5)

        ttk.Label(frm, text="Output Directory:").grid(row=1, column=0, sticky=tk.W)
        self.out_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.out_var, width=45).grid(row=1, column=1)
        ttk.Button(frm, text="Browse…", command=self.browse_out).grid(row=1, column=2, padx=5)

        self.progress = ttk.Progressbar(frm, orient='horizontal', mode='determinate')
        self.progress.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=15)

        ttk.Button(frm, text="Convert All IPL & IDE Files", command=self.start).grid(
            row=3, column=0, columnspan=3, sticky=tk.EW
        )

        frm.columnconfigure(1, weight=1)

    def browse_in(self):
        p = filedialog.askdirectory(title="Select input GTA III/VC folder")
        if p: self.in_var.set(p)

    def browse_out(self):
        p = filedialog.askdirectory(title="Select output folder")
        if p: self.out_var.set(p)

    def start(self):
        inp, outp = self.in_var.get(), self.out_var.get()
        if not os.path.isdir(inp) or not os.path.isdir(outp):
            return messagebox.showerror("Error", "Select valid directories.")
        threading.Thread(target=self.convert_all, args=(inp, outp), daemon=True).start()

    def convert_all(self, inp, outp):
        files = []
        for root, _, names in os.walk(inp):
            for name in names:
                if name.lower().endswith(('.ipl', '.ide')):
                    src = os.path.join(root, name)
                    rel = os.path.relpath(src, inp)
                    files.append((src, os.path.join(outp, rel)))
        if not files: 
            return messagebox.showinfo("Info", "No .ipl or .ide files found.")
        
        self.progress['maximum'], self.progress['value'] = len(files), 0
        for src, dst in files:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            try:
                if src.lower().endswith('.ipl'):
                    self.convert_ipl(src, dst)
                else:
                    self.convert_ide(src, dst)
            except Exception as e:
                print("Error:", src, e)
            self.progress['value'] += 1
        messagebox.showinfo("Done", "All files converted.")

    def convert_ipl(self, src, dst):
        text = open(src, errors='ignore').read().replace('\r','\n').split('\n')
        insting, out = False, []
        for line in text:
            l = line.strip()
            parts = [p.strip() for p in l.split(',')]
            if len(parts) in (12,13,14) and parts[0].isdigit():
                if not insting:
                    out.append('inst'); insting = True
                ID, M = parts[0], parts[1]
                if len(parts) == 12:
                    pos, rot = parts[2:5], parts[8:12]
                    interior = '0'
                else:
                    interior, pos, rot = parts[2], parts[3:6], parts[9:13]
                out.append(', '.join([ID, M, interior] + pos + rot + ['-1']))
        if insting:
            out.append('end')
        with open(dst, 'w', newline='', encoding='utf-8') as f:
            f.write('\r\n'.join(out))

    def convert_ide(self, src, dst):
        text = open(src, errors='ignore').read().replace('\r','\n').split('\n')
        out, section = [], None
        for line in text:
            l = line.strip()
            low = l.lower()
            if low in ('objs','tobj','hier','peds'):
                if section:
                    out.append('end')
                section = low
                out.append(l); continue
            if low == 'end':
                section = None
                continue
            out.append(line) if not section else self.handle_line(section, l, out)
        if section:
            out.append('end')
        with open(dst, 'w', newline='', encoding='utf-8') as f:
            f.write('\r\n'.join(out))

    def handle_line(self, section, line, out):
        parts = [p.strip() for p in line.split(',')]
        if section == 'objs':
            try:
                if int(parts[3]) == 1:
                    out.append(f"{parts[0]}, {parts[1]}, {parts[2]}, {parts[4]}, {parts[-1]}")
                else:
                    out.append(line)
            except:
                out.append(line)
        elif section == 'tobj':
            try:
                if int(parts[3]) == 1:
                    out.append(f"{parts[0]}, {parts[1]}, {parts[2]}, {parts[4]}, {parts[-3]}, {parts[-2]}, {parts[-1]}")
                else:
                    out.append(line)
            except:
                out.append(line)
        elif section == 'peds':
            if len(parts) >= 7:
                base = parts[:7]
                anim, r1, r2 = (parts[7], parts[8], parts[9]) if len(parts) >= 10 else ('','-1','-1')
                sa = base + ['0', anim, r1, r2, '', '', '']
                out.append(', '.join(sa))
            else:
                out.append(line)
        else:
            out.append(line)


if __name__ == "__main__":
    Converter().mainloop()
