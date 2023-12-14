from Machine import Machine
from Manager import Manager
from Task import Task


if __name__ == "__main__":

    with open("../data/problem_10_20_5.txt") as f:
    # with open("../data/sample.txt") as f:
        lines = f.readlines()
    
    machine_id = 1
    task_id = 1

    machine_list = []
    task_list = []

    for line in lines:
        if line.startswith("machine"):
            _, cores, start_time, end_time = line.strip().split(' ')
            cores = int(cores)
            start_time = int(start_time)
            end_time = int(end_time)
            
            machine = Machine(machine_id, cores, start_time, end_time)
            machine_list.append(machine)

            machine_id += 1
        elif line.startswith("task"):
            _, cores, duration, eraliest_start, latest_start = line.strip().split(' ')
            cores = int(cores)
            eraliest_start = int(eraliest_start)
            latest_start = int(latest_start)
            duration = int(duration)

            task = Task(task_id, cores, eraliest_start, latest_start, duration)
            task_list.append(task)

            task_id += 1
        else:
            continue

    manager = Manager(len(task_list), len(machine_list), task_list, machine_list)

    manager.greedy()

    manager.print_solution()
