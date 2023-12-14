# Problem Define

Given $N$ tasks, $M$ machine

Each task $i$ has require cores $c_i$, earliest start time $h_s^{(i)}$, latest start time $h_e^{(i)}$, and duration $d_i$

Each machine $k$ has cores $M_k$, start time $T_s^{(k)}$, and end time $T_e^{(k)}$

The objective is to maximize all tasks' that can be run on the machine cores multiplied by the duration of the task, i.e. $\max{\sum_{A \subseteq [N]}} \sum_{i \in A}d_i \times c_i$, where $A$ is the set of tasks that can be run on the machine.

The constraints are:

1. Core constraint: $\forall k \in [M], \forall t \in [T_s^{(k)}, T_e^{(k)}], \sum_{i \in A_k}c_i \leq M_k$, where $A_k$ is the set of tasks that can be run on machine $k$ at time $t$.
2. Start time constraint: $\forall i \in [N], \max{(h_s^{(i)},T_s^{(k)})} \leq t \lt h_e^{(i)} \Rightarrow i \in A_k$, where $A_k$ is the set of tasks that can be run on machine $k$ at time $t$.
3. End time constraint: $\forall i \in [N],T_e^{k} \geq t + d_i \Rightarrow i \in A_k$, where $A_k$ is the set of tasks that can be run on machine $k$ at time $t$, and $t$ is the start time of task $i$ on machine $k$.



