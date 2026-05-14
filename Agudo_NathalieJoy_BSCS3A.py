import matplotlib.pyplot as plt


class Process:
    # holds individual process data
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.waiting = 0
        self.turnaround = 0
        self.completion = 0


class Scheduler:
    # manages all scheduling algorithms
    def __init__(self, processes):
        self.processes = processes
        self.gantt = []

    # reset all process metrics
    def reset(self):
        self.gantt = []
        for p in self.processes:
            p.waiting = 0
            p.turnaround = 0
            p.completion = 0

    # compute waiting and turnaround
    def calculate_metrics(self, p, completion_time):
        p.completion = completion_time
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.burst

    # first come first served
    def fcfs(self):
        # sort by arrival
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time = 0

        for p in processes:
            # handle idle time
            if time < p.arrival:
                self.gantt.append(("IDLE", time, p.arrival))
                time = p.arrival

            # execute process
            start = time
            time += p.burst
            finish = time

            # store results
            self.calculate_metrics(p, finish)
            self.gantt.append((p.pid, start, finish))

        self.display("FCFS")
        self.plot_gantt("FCFS")

    # shortest job first nonpreemptive
    def sjf_non_preemptive(self):
        # initialize tracking
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time = 0
        completed = 0
        n = len(processes)
        ready_queue = []
        visited = [False] * n

        while completed < n:
            # add arrived processes
            for i in range(n):
                if processes[i].arrival <= time and not visited[i]:
                    ready_queue.append(processes[i])
                    visited[i] = True

            # handle idle cpu
            if not ready_queue:
                next_arrival = None
                for i in range(n):
                    if not visited[i]:
                        if next_arrival is None or processes[i].arrival < next_arrival:
                            next_arrival = processes[i].arrival
                self.gantt.append(("IDLE", time, next_arrival))
                time = next_arrival
                continue

            # pick shortest job
            shortest = min(ready_queue, key=lambda p: p.burst)
            ready_queue.remove(shortest)

            # run to completion
            start = time
            time += shortest.burst

            # record metrics
            self.calculate_metrics(shortest, time)
            self.gantt.append((shortest.pid, start, time))

            completed += 1

        self.display("SJF (Non-Preemptive)")
        self.plot_gantt("SJF")

    # shortest remaining time preemptive
    def srt(self):
        # setup remaining bursts
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time = 0
        completed = 0
        n = len(processes)
        remaining_burst = []
        for p in processes:
            remaining_burst.append(p.burst)
        visited = [False] * n
        prev = None

        while completed < n:
            # find ready processes
            ready_indices = []
            for i in range(n):
                if processes[i].arrival <= time and not visited[i]:
                    ready_indices.append(i)

            # handle idle time
            if not ready_indices:
                next_arrival = None
                for i in range(n):
                    if not visited[i]:
                        if next_arrival is None or processes[i].arrival < next_arrival:
                            next_arrival = processes[i].arrival
                self.gantt.append(("IDLE", time, next_arrival))
                time = next_arrival
                continue

            # pick shortest remaining
            best_index = ready_indices[0]
            for i in ready_indices:
                if remaining_burst[i] < remaining_burst[best_index]:
                    best_index = i

            # execute one unit
            p = processes[best_index]

            if prev != best_index:
                self.gantt.append([p.pid, time, time + 1])
            else:
                self.gantt[-1][2] += 1

            remaining_burst[best_index] -= 1
            time += 1
            prev = best_index

            # check for completion
            if remaining_burst[best_index] == 0:
                visited[best_index] = True
                completed += 1
                self.calculate_metrics(p, time)

        self.display("SRT (Preemptive SJF)")
        self.plot_gantt("SRT")

    # round robin with quantum
    def round_robin(self, quantum):
        # initialize queues
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time = 0
        completed = 0
        n = len(processes)
        remaining_burst = [p.burst for p in processes]
        visited = [False] * n
        ready_queue = []
        added = [False] * n

        # add initial processes
        for i in range(n):
            if processes[i].arrival <= time:
                ready_queue.append(i)
                added[i] = True

        while completed < n:
            # handle empty queue
            if not ready_queue:
                next_arrival = None
                for i in range(n):
                    if not added[i]:
                        if next_arrival is None or processes[i].arrival < next_arrival:
                            next_arrival = processes[i].arrival
                self.gantt.append(("IDLE", time, next_arrival))
                time = next_arrival
                for i in range(n):
                    if processes[i].arrival <= time and not added[i]:
                        ready_queue.append(i)
                        added[i] = True
                continue

            # get next process
            idx = ready_queue.pop(0)
            p = processes[idx]

            # determine run time
            if remaining_burst[idx] < quantum:
                run_time = remaining_burst[idx]
            else:
                run_time = quantum

            # execute time slice
            start = time
            time += run_time
            remaining_burst[idx] -= run_time

            # record execution
            self.gantt.append((p.pid, start, time))

            # add newly arrived
            for i in range(n):
                if processes[i].arrival <= time and not added[i]:
                    ready_queue.append(i)
                    added[i] = True

            # check completion
            if remaining_burst[idx] == 0:
                visited[idx] = True
                completed += 1
                self.calculate_metrics(p, time)
            else:
                ready_queue.append(idx)

        self.display("Round Robin")
        self.plot_gantt("Round Robin")

    # priority nonpreemptive
    def priority_non_preemptive(self):
        # sort by arrival
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time = 0
        completed = 0
        n = len(processes)
        ready_queue = []
        visited = [False] * n

        while completed < n:
            # add arrived processes
            for i in range(n):
                if processes[i].arrival <= time and not visited[i] and processes[i] not in ready_queue:
                    ready_queue.append(processes[i])

            # handle idle time
            if not ready_queue:
                next_arrival = min(p.arrival for i, p in enumerate(processes) if not visited[i])
                self.gantt.append(("IDLE", time, next_arrival))
                time = next_arrival
                continue

            # pick highest priority
            selected = min(ready_queue, key=lambda p: (p.priority, p.arrival))
            ready_queue.remove(selected)

            # mark as visited
            for i in range(n):
                if processes[i].pid == selected.pid:
                    visited[i] = True

            # run to completion
            start = time
            time += selected.burst

            # record results
            self.calculate_metrics(selected, time)
            self.gantt.append((selected.pid, start, time))

            completed += 1

        self.display("Priority Scheduling (Non-Preemptive)")
        self.plot_gantt("Priority (Non-Preemptive)")

    # priority preemptive
    def priority_preemptive(self):
        # setup remaining bursts
        self.reset()
        processes = sorted(self.processes, key=lambda p: p.arrival)
        time = 0
        completed = 0
        n = len(processes)
        remaining_burst = [p.burst for p in processes]
        visited = [False] * n
        prev = None

        while completed < n:
            # find ready processes
            ready_indices = []
            for i in range(n):
                if processes[i].arrival <= time and not visited[i]:
                    ready_indices.append(i)

            # handle idle time
            if not ready_indices:
                next_arrival = None
                for i in range(n):
                    if not visited[i]:
                        if next_arrival is None or processes[i].arrival < next_arrival:
                            next_arrival = processes[i].arrival
                self.gantt.append(("IDLE", time, next_arrival))
                time = next_arrival
                prev = None
                continue

            # pick highest priority
            best_index = ready_indices[0]
            for i in ready_indices:
                if (processes[i].priority, processes[i].arrival) < (processes[best_index].priority, processes[best_index].arrival):
                    best_index = i

            # execute one unit
            p = processes[best_index]

            if prev != best_index:
                self.gantt.append([p.pid, time, time + 1])
            else:
                self.gantt[-1][2] += 1

            remaining_burst[best_index] -= 1
            time += 1
            prev = best_index

            # check completion
            if remaining_burst[best_index] == 0:
                visited[best_index] = True
                completed += 1
                self.calculate_metrics(p, time)

        self.display("Priority Scheduling (Preemptive)")
        self.plot_gantt("Priority (Preemptive)")

    # priority with round robin
    def priority_round_robin(self, quantum):
        # initialize tracking
        self.reset()
        processes = sorted(self.processes, key=lambda p: (p.priority, p.arrival))
        time = 0
        completed = 0
        n = len(processes)
        remaining_burst = [p.burst for p in processes]
        visited = [False] * n
        added = [False] * n
        ready_queue = []

        while completed < n:
            # add newly arrived
            for i in range(n):
                if processes[i].arrival <= time and not added[i]:
                    ready_queue.append(i)
                    added[i] = True

            # handle idle time
            if not ready_queue:
                next_arrival = min(
                    processes[i].arrival for i in range(n) if not added[i]
                )
                self.gantt.append(("IDLE", time, next_arrival))
                time = next_arrival
                continue

            # pick highest priority group
            best_priority = min(processes[i].priority for i in ready_queue)
            idx = next(i for i in ready_queue if processes[i].priority == best_priority)
            ready_queue.remove(idx)

            # run time slice
            p = processes[idx]
            run_time = min(remaining_burst[idx], quantum)

            start = time
            time += run_time
            remaining_burst[idx] -= run_time

            # record execution
            self.gantt.append((p.pid, start, time))

            # add newly arrived after slice
            for i in range(n):
                if processes[i].arrival <= time and not added[i]:
                    ready_queue.append(i)
                    added[i] = True

            # check completion
            if remaining_burst[idx] == 0:
                visited[idx] = True
                completed += 1
                self.calculate_metrics(p, time)
            else:
                ready_queue.append(idx)

        self.display("Priority + Round Robin")
        self.plot_gantt("Priority + Round Robin")

    # display results table
    def display(self, algo_name):
        print(f"\n=== {algo_name} ===")
        is_priority_algo = "Priority" in algo_name

        if is_priority_algo:
            print("\nPID\tAT\tBT\tPRIO\tWT\tTAT\tCT")
            print("-" * 60)
        else:
            print("\nPID\tAT\tBT\tWT\tTAT\tCT")
            print("-" * 50)

        total_wt = 0
        total_tat = 0

        for p in self.processes:
            if is_priority_algo:
                print(f"{p.pid}\t{p.arrival}\t{p.burst}\t{p.priority}\t{p.waiting}\t{p.turnaround}\t{p.completion}")
            else:
                print(f"{p.pid}\t{p.arrival}\t{p.burst}\t{p.waiting}\t{p.turnaround}\t{p.completion}")
            total_wt += p.waiting
            total_tat += p.turnaround

        n = len(self.processes)
        print("-" * (60 if is_priority_algo else 50))
        print(f"\nAvg WT: {round(total_wt / n, 2)}")
        print(f"Avg TAT: {round(total_tat / n, 2)}")

    # plot gantt chart
    def plot_gantt(self, title):
        fig, ax = plt.subplots()
        import matplotlib.cm as cm
        import numpy as np

        unique_pids = list(set([pid for pid, _, _ in self.gantt if pid != "IDLE"]))
        color_map = {}
        colors = cm.tab20(np.linspace(0, 1, len(unique_pids)))
        for i, pid in enumerate(unique_pids):
            color_map[pid] = colors[i]

        idle_color = 'lightgray'

        for pid, start, end in self.gantt:
            label = str(pid)

            if pid == "IDLE":
                color = idle_color
            else:
                color = color_map[pid]

            ax.barh(0, end - start, left=start, color=color, edgecolor='black')
            ax.text((start + end) / 2, 0, label, ha='center', va='center')

        ax.set_xlabel("Time")
        ax.set_yticks([])
        ax.set_title(f"Gantt Chart - {title}")

        max_time = int(self.gantt[-1][2])
        ax.set_xticks(list(range(max_time + 1)))

        plt.show()


# get user input for processes
def get_input(choice):
    needs_priority = choice in [5, 6, 7]

    while True:
        try:
            n = int(input("Enter number of processes (>=3): "))
            if n >= 3:
                break
            print("Minimum is 3 processes.")
        except ValueError:
            print("Please enter a valid integer.")

    processes = []

    for i in range(n):
        print(f"\nProcess {i + 1}")
        pid = input("Process Identifier: ")

        while True:
            try:
                bt = int(input("Burst Time: "))
                at = int(input("Arrival Time: "))

                if needs_priority:
                    pr = int(input("Priority (Lower Value = Higher Priority): "))
                else:
                    pr = 0

                break
            except ValueError:
                print("Please enter valid integers.")

        processes.append(Process(pid, at, bt, pr))

    return processes


# main program entry point
def main():
    print("\nChoose Scheduling Algorithm:")
    print("1. FCFS")
    print("2. SJF (Non-Preemptive)")
    print("3. SRT (Preemptive SJF)")
    print("4. Round Robin")
    print("5. Priority Scheduling (Non-Preemptive)")
    print("6. Priority Scheduling (Preemptive)")
    print("7. Priority + Round Robin")

    while True:
        try:
            choice = int(input("Enter choice: "))
            if choice in range(1, 8):
                break
            print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Please enter a valid integer.")

    processes = get_input(choice)
    scheduler = Scheduler(processes)

    if choice == 1:
        scheduler.fcfs()
    elif choice == 2:
        scheduler.sjf_non_preemptive()
    elif choice == 3:
        scheduler.srt()
    elif choice == 4:
        while True:
            try:
                quantum = int(input("\nEnter Time Quantum: "))
                break
            except ValueError:
                print("Please enter a valid integer.")
        scheduler.round_robin(quantum)
    elif choice == 5:
        scheduler.priority_non_preemptive()
    elif choice == 6:
        scheduler.priority_preemptive()
    elif choice == 7:
        while True:
            try:
                quantum = int(input("Enter Time Quantum: "))
                break
            except ValueError:
                print("Please enter a valid integer.")
        scheduler.priority_round_robin(quantum)
    else:
        print("Invalid choice")


# run simulation loop
while True:
    main()
    print("\nRun another simulation?")
    print("1. Yes")
    print("2. No")

    while True:
        try:
            again = int(input("Enter choice: "))
            if again in [1, 2]:
                break
            print("Please enter 1 or 2 only.")
        except ValueError:
            print("Please enter a valid integer.")

    if again == 2:
        print("Exiting program...")
        break