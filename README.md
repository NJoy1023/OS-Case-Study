# CPU Scheduling Simulator

A Python-based Operating Systems simulation program designed to demonstrate and compare different CPU Scheduling Algorithms through computed process metrics and Gantt Chart visualizations.

The simulator is implemented using Python with the help of Matplotlib and NumPy for graphical representation.

---

# Video Presentation
https://drive.google.com/file/d/1_Uh1bJKf5WO-lzUe0VZXCps3JdxucpDQ/view?usp=sharing

# Features

The program supports the following CPU Scheduling Algorithms:

1. First Come First Served (FCFS)
2. Shortest Job First (SJF – Non-Preemptive)
3. Shortest Remaining Time (SRT – Preemptive SJF)
4. Round Robin (RR)
5. Priority Scheduling (Non-Preemptive)
6. Priority Scheduling (Preemptive)
7. Priority + Round Robin

For each simulation, the program computes and displays:

- Waiting Time (WT)
- Turnaround Time (TAT)
- Completion Time (CT)
- Average Waiting Time
- Average Turnaround Time

The system also generates a Gantt Chart visualization to illustrate CPU execution flow.

---

# Requirements

Before running the program, ensure that the following are installed on your system:

- Python 3.x
- Matplotlib
- NumPy

---

# Installation Guide

## 1. Install Python

Download and install Python from the official website:

https://www.python.org/downloads/

During installation, make sure to enable:

```text
Add Python to PATH
```

---

## 2. Install Required Libraries

Open Command Prompt or Terminal and run:

```bash
pip install matplotlib numpy
```

If `pip` does not work, use:

```bash
py -m pip install matplotlib numpy
```

---

# How to Run the Program

## 1. Download or Clone the Repository

Using Git:

```bash
git clone https://github.com/your-username/your-repository-name.git
```

Or download the repository as a ZIP file from GitHub and extract it.

---

## 2. Open the Project Folder

Navigate to the folder containing:

```text
Source_Code.py
```

Example:

```bash
cd Desktop/CPU-Scheduling-CaseStudy
```

---

## 3. Execute the Program

Run the Python file using:

```bash
python Source_Code.py
```

or

```bash
py Source_Code.py
```

---

# Using the Program

After launching the program, select a scheduling algorithm from the menu:

```text
1. FCFS
2. SJF (Non-Preemptive)
3. SRT (Preemptive SJF)
4. Round Robin
5. Priority Scheduling (Non-Preemptive)
6. Priority Scheduling (Preemptive)
7. Priority + Round Robin
```

Then provide the required process information:

- Process Identifier
- Burst Time
- Arrival Time
- Priority Value (if required)
- Time Quantum (if required)

The program will then display:

- Process Scheduling Table
- Waiting Time
- Turnaround Time
- Completion Time
- Average WT and TAT
- Gantt Chart Visualization

---

# Example Input

```text
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

# Common Errors and Solutions

## ModuleNotFoundError: No module named 'matplotlib'

Install matplotlib using:

```bash
pip install matplotlib
```

---

## ModuleNotFoundError: No module named 'numpy'

Install numpy using:

```bash
pip install numpy
```

---

## 'python' is not recognized as an internal or external command

This means Python is either not installed or not added to the system PATH.

Solution:

- Reinstall Python
- Enable:

```text
Add Python to PATH
```

during installation.

---

# Program Termination

After each simulation, the program asks:

```text
Run another simulation?
1. Yes
2. No
```

Enter:

```text
2
```

to terminate the program.

---

# Developers

Developed as part of an Operating Systems Case Study project focused on analyzing and simulating CPU Scheduling Algorithms using Python.
