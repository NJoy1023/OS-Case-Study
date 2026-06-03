import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.cm as cm
import numpy as np


# ─── Data model ────────────────────────────────────────────────────────────────

class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid      = pid
        self.arrival  = arrival
        self.burst    = burst
        self.priority = priority
        self.waiting    = 0
        self.turnaround = 0
        self.completion = 0


# ─── Scheduling algorithms (unchanged logic) ───────────────────────────────────

class Scheduler:
    def __init__(self, processes):
        self.processes = processes
        self.gantt = []

    def reset(self):
        self.gantt = []
        for p in self.processes:
            p.waiting = p.turnaround = p.completion = 0

    def calculate_metrics(self, p, ct):
        p.completion  = ct
        p.turnaround  = ct - p.arrival
        p.waiting     = p.turnaround - p.burst

    # ── FCFS ──────────────────────────────────────────────────────────────────
    def fcfs(self):
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time = 0
        for p in processes:
            if time < p.arrival:
                self.gantt.append(("IDLE", time, p.arrival))
                time = p.arrival
            start = time
            time += p.burst
            self.calculate_metrics(p, time)
            self.gantt.append((p.pid, start, time))

    # ── SJF non-preemptive ────────────────────────────────────────────────────
    def sjf_non_preemptive(self):
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time, completed, n = 0, 0, len(processes)
        ready_queue, visited = [], [False] * n
        while completed < n:
            for i in range(n):
                if processes[i].arrival <= time and not visited[i]:
                    ready_queue.append(processes[i]); visited[i] = True
            if not ready_queue:
                na = min(processes[i].arrival for i in range(n) if not visited[i])
                self.gantt.append(("IDLE", time, na)); time = na; continue
            s = min(ready_queue, key=lambda p: p.burst); ready_queue.remove(s)
            start = time; time += s.burst
            self.calculate_metrics(s, time)
            self.gantt.append((s.pid, start, time)); completed += 1

    # ── SRT (preemptive SJF) ──────────────────────────────────────────────────
    def srt(self):
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time, completed, n = 0, 0, len(processes)
        rem = [p.burst for p in processes]
        visited = [False] * n; prev = None
        while completed < n:
            ri = [i for i in range(n) if processes[i].arrival <= time and not visited[i]]
            if not ri:
                na = min(processes[i].arrival for i in range(n) if not visited[i])
                self.gantt.append(("IDLE", time, na)); time = na; continue
            bi = min(ri, key=lambda i: rem[i])
            p = processes[bi]
            if prev != bi: self.gantt.append([p.pid, time, time + 1])
            else:          self.gantt[-1][2] += 1
            rem[bi] -= 1; time += 1; prev = bi
            if rem[bi] == 0:
                visited[bi] = True; completed += 1
                self.calculate_metrics(p, time)

    # ── Round Robin ───────────────────────────────────────────────────────────
    def round_robin(self, quantum):
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time, completed, n = 0, 0, len(processes)
        rem = [p.burst for p in processes]
        visited = [False] * n; added = [False] * n; rq = []
        for i in range(n):
            if processes[i].arrival <= time: rq.append(i); added[i] = True
        while completed < n:
            if not rq:
                na = min(processes[i].arrival for i in range(n) if not added[i])
                self.gantt.append(("IDLE", time, na)); time = na
                for i in range(n):
                    if processes[i].arrival <= time and not added[i]: rq.append(i); added[i] = True
                continue
            idx = rq.pop(0); p = processes[idx]
            run = min(rem[idx], quantum)
            start = time; time += run; rem[idx] -= run
            self.gantt.append((p.pid, start, time))
            for i in range(n):
                if processes[i].arrival <= time and not added[i]: rq.append(i); added[i] = True
            if rem[idx] == 0:
                visited[idx] = True; completed += 1; self.calculate_metrics(p, time)
            else: rq.append(idx)

    # ── Priority non-preemptive ───────────────────────────────────────────────
    def priority_non_preemptive(self):
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time, completed, n = 0, 0, len(processes)
        rq = []; visited = [False] * n
        while completed < n:
            for i in range(n):
                if processes[i].arrival <= time and not visited[i] and processes[i] not in rq:
                    rq.append(processes[i])
            if not rq:
                na = min(p.arrival for i, p in enumerate(processes) if not visited[i])
                self.gantt.append(("IDLE", time, na)); time = na; continue
            sel = min(rq, key=lambda p: (p.priority, p.arrival)); rq.remove(sel)
            for i in range(n):
                if processes[i].pid == sel.pid: visited[i] = True
            start = time; time += sel.burst
            self.calculate_metrics(sel, time)
            self.gantt.append((sel.pid, start, time)); completed += 1

    # ── Priority preemptive ───────────────────────────────────────────────────
    def priority_preemptive(self):
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time, completed, n = 0, 0, len(processes)
        rem = [p.burst for p in processes]; visited = [False] * n; prev = None
        while completed < n:
            ri = [i for i in range(n) if processes[i].arrival <= time and not visited[i]]
            if not ri:
                na = min(processes[i].arrival for i in range(n) if not visited[i])
                self.gantt.append(("IDLE", time, na)); time = na; prev = None; continue
            bi = min(ri, key=lambda i: (processes[i].priority, processes[i].arrival))
            p = processes[bi]
            if prev != bi: self.gantt.append([p.pid, time, time + 1])
            else:          self.gantt[-1][2] += 1
            rem[bi] -= 1; time += 1; prev = bi
            if rem[bi] == 0:
                visited[bi] = True; completed += 1; self.calculate_metrics(p, time)

    # ── Priority + Round Robin ────────────────────────────────────────────────
    def priority_round_robin(self, quantum):
        self.reset()
        processes = sorted(self.processes, key=lambda p: (p.priority, p.arrival))
        time, completed, n = 0, 0, len(processes)
        rem = [p.burst for p in processes]; visited = [False] * n
        added = [False] * n; rq = []
        while completed < n:
            for i in range(n):
                if processes[i].arrival <= time and not added[i]: rq.append(i); added[i] = True
            if not rq:
                na = min(processes[i].arrival for i in range(n) if not added[i])
                self.gantt.append(("IDLE", time, na)); time = na; continue
            bp = min(processes[i].priority for i in rq)
            idx = next(i for i in rq if processes[i].priority == bp); rq.remove(idx)
            p = processes[idx]; run = min(rem[idx], quantum)
            start = time; time += run; rem[idx] -= run
            self.gantt.append((p.pid, start, time))
            for i in range(n):
                if processes[i].arrival <= time and not added[i]: rq.append(i); added[i] = True
            if rem[idx] == 0:
                visited[idx] = True; completed += 1; self.calculate_metrics(p, time)
            else: rq.append(idx)

    def get_averages(self):
        n = len(self.processes)
        avg_wt  = round(sum(p.waiting    for p in self.processes) / n, 2)
        avg_tat = round(sum(p.turnaround for p in self.processes) / n, 2)
        return avg_wt, avg_tat


# ─── GUI ───────────────────────────────────────────────────────────────────────

ALGO_OPTIONS = [
    "FCFS",
    "SJF (Non-Preemptive)",
    "SRT (Preemptive SJF)",
    "Round Robin",
    "Priority (Non-Preemptive)",
    "Priority (Preemptive)",
    "Priority + Round Robin",
]

NEEDS_PRIORITY = {4, 5, 6}   # 1-indexed algo choice
NEEDS_QUANTUM  = {3, 6}       # 1-indexed


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduling Simulator")
        self.configure(bg="#1e1e2e")
        self.resizable(True, True)

        # ── style ──────────────────────────────────────────────────────────
        style = ttk.Style(self)
        style.theme_use("clam")
        BG   = "#1e1e2e"
        SURF = "#2a2a3d"
        ACC  = "#7c6af7"
        FG   = "#cdd6f4"
        style.configure(".",             background=BG,   foreground=FG,   font=("Segoe UI", 10))
        style.configure("TFrame",        background=BG)
        style.configure("Card.TFrame",   background=SURF, relief="flat")
        style.configure("TLabel",        background=BG,   foreground=FG)
        style.configure("Card.TLabel",   background=SURF, foreground=FG)
        style.configure("Head.TLabel",   background=BG,   foreground=ACC,
                        font=("Segoe UI", 12, "bold"))
        style.configure("TCombobox",     fieldbackground=SURF, background=SURF,
                        foreground=FG,   selectbackground=ACC)
        style.configure("TEntry",        fieldbackground=SURF, foreground=FG,
                        insertcolor=FG)
        style.configure("Accent.TButton", background=ACC, foreground="#fff",
                        font=("Segoe UI", 10, "bold"), relief="flat", padding=6)
        style.map("Accent.TButton",
                  background=[("active", "#9b8cf8"), ("pressed", "#5a4fcf")])
        style.configure("Danger.TButton", background="#f38ba8", foreground="#1e1e2e",
                        font=("Segoe UI", 10, "bold"), relief="flat", padding=6)
        style.configure("Treeview",       background=SURF, foreground=FG,
                        fieldbackground=SURF, rowheight=26,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#313244", foreground=ACC,
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", ACC)])

        self.BG = BG; self.SURF = SURF; self.ACC = ACC; self.FG = FG

        self._build_ui()

    # ── layout ─────────────────────────────────────────────────────────────────
    def _build_ui(self):
        BG = self.BG; SURF = self.SURF; ACC = self.ACC; FG = self.FG

        root_pad = ttk.Frame(self)
        root_pad.pack(fill="both", expand=True, padx=16, pady=16)

        # title
        ttk.Label(root_pad, text="⚙  CPU Scheduling Simulator",
                  style="Head.TLabel",
                  font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 12))

        # ── top row: config + process table ──────────────────────────────────
        top = ttk.Frame(root_pad); top.pack(fill="x", pady=(0, 12))

        # config card
        cfg = ttk.Frame(top, style="Card.TFrame", padding=14)
        cfg.pack(side="left", fill="y", padx=(0, 10))

        def clabel(text, row, col=0):
            ttk.Label(cfg, text=text, style="Card.TLabel",
                      font=("Segoe UI", 9)).grid(row=row, column=col,
                      sticky="w", pady=3, padx=(0, 8))

        clabel("Algorithm", 0)
        self.algo_var = tk.StringVar(value=ALGO_OPTIONS[0])
        algo_cb = ttk.Combobox(cfg, textvariable=self.algo_var,
                               values=ALGO_OPTIONS, state="readonly", width=28)
        algo_cb.grid(row=0, column=1, pady=3, sticky="w")
        algo_cb.bind("<<ComboboxSelected>>", self._on_algo_change)

        clabel("Time Quantum", 1)
        self.quantum_var = tk.StringVar(value="2")
        self.quantum_entry = ttk.Entry(cfg, textvariable=self.quantum_var, width=8)
        self.quantum_entry.grid(row=1, column=1, pady=3, sticky="w")

        ttk.Separator(cfg, orient="horizontal").grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=8)

        clabel("Process ID", 3)
        self.pid_var = tk.StringVar()
        ttk.Entry(cfg, textvariable=self.pid_var, width=10).grid(
            row=3, column=1, pady=3, sticky="w")

        clabel("Burst Time", 4)
        self.bt_var = tk.StringVar()
        ttk.Entry(cfg, textvariable=self.bt_var, width=10).grid(
            row=4, column=1, pady=3, sticky="w")

        clabel("Arrival Time", 5)
        self.at_var = tk.StringVar()
        ttk.Entry(cfg, textvariable=self.at_var, width=10).grid(
            row=5, column=1, pady=3, sticky="w")

        clabel("Priority", 6)
        self.pr_var = tk.StringVar(value="0")
        self.pr_entry = ttk.Entry(cfg, textvariable=self.pr_var, width=10)
        self.pr_entry.grid(row=6, column=1, pady=3, sticky="w")

        btn_row = ttk.Frame(cfg, style="Card.TFrame")
        btn_row.grid(row=7, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btn_row, text="+ Add Process", style="Accent.TButton",
                   command=self._add_process).pack(side="left", padx=(0, 6))
        ttk.Button(btn_row, text="✕ Remove", style="Danger.TButton",
                   command=self._remove_process).pack(side="left")

        # process table card
        tbl_frame = ttk.Frame(top, style="Card.TFrame", padding=10)
        tbl_frame.pack(side="left", fill="both", expand=True)

        ttk.Label(tbl_frame, text="Processes", style="Card.TLabel",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))

        cols = ("PID", "Arrival", "Burst", "Priority")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
                                 height=8, selectmode="browse")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=80, anchor="center")
        vsb = ttk.Scrollbar(tbl_frame, orient="vertical",
                            command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="left", fill="y")

        # ── run button ────────────────────────────────────────────────────────
        run_row = ttk.Frame(root_pad); run_row.pack(fill="x", pady=(0, 12))
        ttk.Button(run_row, text="▶  Run Simulation", style="Accent.TButton",
                   command=self._run).pack(side="left")
        ttk.Button(run_row, text="⟳  Clear All", style="Danger.TButton",
                   command=self._clear_all).pack(side="left", padx=8)

        # ── results area ─────────────────────────────────────────────────────
        res_frame = ttk.Frame(root_pad, style="Card.TFrame", padding=10)
        res_frame.pack(fill="both", expand=True)

        # results table
        res_cols = ("PID", "AT", "BT", "Priority", "WT", "TAT", "CT")
        self.res_tree = ttk.Treeview(res_frame, columns=res_cols,
                                     show="headings", height=6,
                                     selectmode="none")
        for c in res_cols:
            self.res_tree.heading(c, text=c)
            self.res_tree.column(c, width=80, anchor="center")
        self.res_tree.pack(fill="x", pady=(0, 8))

        # avg stats bar
        stat_bar = ttk.Frame(res_frame, style="Card.TFrame")
        stat_bar.pack(fill="x", pady=(0, 8))
        self.avg_wt_var  = tk.StringVar(value="Avg WT: –")
        self.avg_tat_var = tk.StringVar(value="Avg TAT: –")
        ttk.Label(stat_bar, textvariable=self.avg_wt_var,
                  style="Card.TLabel",
                  font=("Segoe UI", 10, "bold")).pack(side="left", padx=12)
        ttk.Label(stat_bar, textvariable=self.avg_tat_var,
                  style="Card.TLabel",
                  font=("Segoe UI", 10, "bold")).pack(side="left")

        # gantt canvas
        self.fig, self.ax = plt.subplots(figsize=(10, 1.8))
        self.fig.patch.set_facecolor("#2a2a3d")
        self.ax.set_facecolor("#2a2a3d")
        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=res_frame)
        self.canvas_widget.get_tk_widget().pack(fill="x")

        self._on_algo_change()

    # ── helpers ────────────────────────────────────────────────────────────────
    def _algo_index(self):
        return ALGO_OPTIONS.index(self.algo_var.get()) + 1   # 1-indexed

    def _on_algo_change(self, _=None):
        idx = self._algo_index()
        state_q = "normal" if idx in NEEDS_QUANTUM  else "disabled"
        state_p = "normal" if idx in NEEDS_PRIORITY else "disabled"
        self.quantum_entry.configure(state=state_q)
        self.pr_entry.configure(state=state_p)

    def _add_process(self):
        pid = self.pid_var.get().strip()
        if not pid:
            messagebox.showwarning("Input error", "Process ID cannot be empty.")
            return
        try:
            bt = int(self.bt_var.get())
            at = int(self.at_var.get())
            pr = int(self.pr_var.get()) if self.pr_entry["state"] == "normal" else 0
        except ValueError:
            messagebox.showwarning("Input error",
                                   "Burst Time, Arrival Time and Priority must be integers.")
            return

        # prevent duplicate PIDs
        for row in self.tree.get_children():
            if self.tree.item(row)["values"][0] == pid:
                messagebox.showwarning("Duplicate", f"PID '{pid}' already exists.")
                return

        self.tree.insert("", "end", values=(pid, at, bt, pr))
        self.pid_var.set(""); self.bt_var.set("")
        self.at_var.set(""); self.pr_var.set("0")

    def _remove_process(self):
        sel = self.tree.selection()
        if sel: self.tree.delete(sel[0])

    def _clear_all(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        for row in self.res_tree.get_children(): self.res_tree.delete(row)
        self.avg_wt_var.set("Avg WT: –"); self.avg_tat_var.set("Avg TAT: –")
        self.ax.clear()
        self.ax.set_facecolor("#2a2a3d")
        self.canvas_widget.draw()

    # ── run simulation ─────────────────────────────────────────────────────────
    def _run(self):
        rows = self.tree.get_children()
        if len(rows) < 3:
            messagebox.showwarning("Not enough processes",
                                   "Please add at least 3 processes.")
            return

        processes = []
        for row in rows:
            v = self.tree.item(row)["values"]
            processes.append(Process(str(v[0]), int(v[1]), int(v[2]), int(v[3])))

        sched = Scheduler(processes)
        idx   = self._algo_index()

        try:
            if idx == 1: sched.fcfs()
            elif idx == 2: sched.sjf_non_preemptive()
            elif idx == 3: sched.srt()
            elif idx == 4:
                q = int(self.quantum_var.get())
                sched.round_robin(q)
            elif idx == 5: sched.priority_non_preemptive()
            elif idx == 6: sched.priority_preemptive()
            elif idx == 7:
                q = int(self.quantum_var.get())
                sched.priority_round_robin(q)
        except Exception as e:
            messagebox.showerror("Simulation error", str(e))
            return

        self._show_results(sched)
        self._draw_gantt(sched)

    # ── populate results table ─────────────────────────────────────────────────
    def _show_results(self, sched):
        for row in self.res_tree.get_children():
            self.res_tree.delete(row)

        for p in sched.processes:
            self.res_tree.insert("", "end",
                values=(p.pid, p.arrival, p.burst, p.priority,
                        p.waiting, p.turnaround, p.completion))

        avg_wt, avg_tat = sched.get_averages()
        self.avg_wt_var.set(f"Avg Waiting Time: {avg_wt}")
        self.avg_tat_var.set(f"   |   Avg Turnaround: {avg_tat}")

    # ── draw gantt chart ───────────────────────────────────────────────────────
    def _draw_gantt(self, sched):
        self.ax.clear()
        self.ax.set_facecolor("#2a2a3d")

        unique_pids = list(dict.fromkeys(
            pid for pid, _, _ in sched.gantt if pid != "IDLE"))
        palette = cm.tab20(np.linspace(0, 1, max(len(unique_pids), 1)))
        color_map = {pid: palette[i] for i, pid in enumerate(unique_pids)}

        for pid, start, end in sched.gantt:
            color = "#555566" if pid == "IDLE" else color_map[pid]
            self.ax.barh(0, end - start, left=start, color=color,
                         edgecolor="#1e1e2e", linewidth=0.8, height=0.5)
            mid = (start + end) / 2
            label_color = "#aaaaaa" if pid == "IDLE" else "#ffffff"
            if (end - start) > 0.4:
                self.ax.text(mid, 0, str(pid), ha="center", va="center",
                             fontsize=8, color=label_color,
                             fontweight="bold")

        max_time = int(sched.gantt[-1][2])
        self.ax.set_xlim(0, max_time)
        self.ax.set_yticks([])
        self.ax.set_xticks(range(max_time + 1))
        self.ax.tick_params(axis="x", colors="#cdd6f4", labelsize=8)
        self.ax.set_xlabel("Time", color="#cdd6f4", fontsize=9)
        self.ax.set_title(
            f"Gantt Chart — {self.algo_var.get()}",
            color="#cdd6f4", fontsize=10, pad=6)
        for spine in self.ax.spines.values():
            spine.set_visible(False)

        # legend patches
        patches = [mpatches.Patch(color=color_map[p], label=str(p))
                   for p in unique_pids]
        if patches:
            self.ax.legend(handles=patches, loc="upper right",
                           facecolor="#313244", labelcolor="#cdd6f4",
                           fontsize=7, framealpha=0.8,
                           edgecolor="#555566")

        self.fig.tight_layout()
        self.canvas_widget.draw()


# ─── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()