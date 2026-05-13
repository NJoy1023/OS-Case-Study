# CPU Scheduling Simulator

A Python-based Operating Systems simulation program that demonstrates different CPU Scheduling Algorithms and visualizes their execution using Gantt Charts.

Built using Python, Matplotlib, and NumPy.

---

# Features

This simulator supports the following scheduling algorithms:

1. First Come First Served (FCFS)
2. Shortest Job First (SJF – Non-Preemptive)
3. Shortest Remaining Time (SRT – Preemptive SJF)
4. Round Robin (RR)
5. Priority Scheduling (Non-Preemptive)
6. Priority Scheduling (Preemptive)
7. Priority + Round Robin

The program also calculates:

* Waiting Time (WT)
* Turnaround Time (TAT)
* Completion Time (CT)
* Average Waiting Time
* Average Turnaround Time

Additionally, the program generates a Gantt Chart visualization for every simulation.

---

# Requirements

Before running the program, make sure the following are installed:

* Python 3.x
* Matplotlib
* NumPy

---

# Installation

## 1. Install Python

Download Python from the official website:

[Python Official Website](https://www.python.org/downloads/?utm_source=chatgpt.com)

During installation, make sure to enable:

```text id="qbrkq5"
Add Python to PATH
```

---

## 2. Install Required Libraries

Open Command Prompt or Terminal and run:

```bash id="s0u68f"
pip install matplotlib numpy
```

If `pip` does not work, try:

```bash id="pjqj0h"
py -m pip install matplotlib numpy
```

---

# How to Run the Program

## 1. Download or Clone the Repository

Using Git:

```bash id="26d7je"
git clone https://github.com/your-username/your-repository-name.git
```

Or download the repository as ZIP from [GitHub](https://github.com?utm_source=chatgpt.com) and extract it.

---

## 2. Open the Project Folder

Navigate to the folder containing:

```text id="v9ztse"
OS-CPU-Scheduling-CaseSudy_FINALIZED.py
```

Example:

```bash id="m1pp9q"
cd Desktop/CPU-Scheduler
```

---

## 3. Run the Program

Execute the Python file using:

```bash id="z0mgtm"
python OS-CPU-Scheduling-CaseSudy_FINALIZED.py
```

or

```bash id="c4thlb"
py OS-CPU-Scheduling-CaseSudy_FINALIZED.py
```

---

# Using the Program

After running the program, choose a scheduling algorithm from the menu:

```text id="mhsl2s"
1. FCFS
2. SJF (Non-Preemptive)
3. SRT (Preemptive SJF)
4. Round Robin
5. Priority Scheduling (Non-Preemptive)
6. Priority Scheduling (Preemptive)
7. Priority + Round Robin
```

Then:

1. Enter the number of processes
2. Input:

   * Process ID
   * Burst Time
   * Arrival Time
   * Priority (if required)
   * Time Quantum (if required)

The program will display:

* Process scheduling table
* Waiting Time
* Turnaround Time
* Completion Time
* Average WT and TAT
* Gantt Chart visualization

---

# Example Input

```text id="crftft"
Enter choice: 1
Enter number of processes (>=3): 3

Process 1
Process Identifier: P1
Burst Time: 5
Arrival Time: 0

Process 2
Process Identifier: P2
Burst Time: 3
Arrival Time: 1

Process 3
Process Identifier: P3
Burst Time: 2
Arrival Time: 2
```

---

# Common Errors

## ModuleNotFoundError: No module named 'matplotlib'

Install matplotlib using:

```bash id="1a0nd9"
pip install matplotlib
```

---

## ModuleNotFoundError: No module named 'numpy'

Install numpy using:

```bash id="2c7sc7"
pip install numpy
```


# Program Termination

After each simulation, the program will ask:

```text id="rnwql8"
Run another simulation?
1. Yes
2. No
```

Enter:

```text id="d0n8mc"
2
```

to exit the program.

---


# Developers

Developed as part of an Operating Systems CPU Scheduling Case Study project.
