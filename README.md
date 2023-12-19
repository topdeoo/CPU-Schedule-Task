# Problem Definition

Given $N$ tasks, $M$ machine

Each task $i$ has require cores $c_i$, earliest start time $h_s^{(i)}$, latest start time $h_e^{(i)}$, and duration $d_i$

Each machine $k$ has cores $M_k$, start time $T_s^{(k)}$, and end time $T_e^{(k)}$

The objective is to maximize all tasks' that can be run on the machine cores multiplied by the duration of the task, i.e. $\max{\sum_{A \subseteq [N]}} \sum_{i \in A}d_i \times c_i$, where $A$ is the set of tasks that can be run on the machine.

The constraints are:

1. Each time slot, the sum of cores of all tasks running on the machine cannot exceed the machine cores.

2. Each task can only be run on the machine if the start time of the task is later than the start time of the machine.

3. Each task can only be run on the machine if the end time of the task is earlier than the end time of the machine.

4. Each task can only be run on the machine if the sum of cores of all tasks running on the machine cannot exceed the machine cores.

5. Each task can only be run on the machine if the start time of the task is later than or equal the earliest start time of the task.

6. Each task can only be run on the machine if the start time of the task is earlier than or equal the latest start time of the task.

Formally, the constraints are (maybe not complete):

1. Core constraint: $\forall k \in [M], \forall t \in [T_s^{(k)}, T_e^{(k)}], \sum_{i \in A_k}c_i \leq M_k$, where $A_k$ is the set of tasks that can be run on machine $k$ at time $t$.
2. Start time constraint: $\forall i \in [N], \max{(h_s^{(i)},T_s^{(k)})} \leq t \lt h_e^{(i)} \Rightarrow i \in A_k$, where $A_k$ is the set of tasks that can be run on machine $k$ at time $t$.
3. End time constraint: $\forall i \in [N],T_e^{k} \geq t + d_i \Rightarrow i \in A_k$, where $A_k$ is the set of tasks that can be run on machine $k$ at time $t$, and $t$ is the start time of task $i$ on machine $k$.

# Implementation

Main code is in `src/.main.py`, just run `python main.py` to run the code.

The code does not implement the local search strategy, just the greedy strategy.

Also, there is a gurobi implementation in `src/gurobi.py`, before run, you should make sure install the `gurobipy` package, and run `python gurobi.py` to run the code.

