from Task import Task
from Machine import Machine

class Manager:
    def __init__(self, n: int, m: int, task_list: list[Task], machine_list: list[Machine]) -> None:
        self._n = n
        self._m = m
        self._task_list = dict()
        self._machine_list = dict()
        for task in task_list:
            self._task_list[task.id] = task
        for machine in machine_list:
            self._machine_list[machine.id] = machine

        self._rcl_list = task_list.copy()
        
        self._next_added_task = (-1, -1, -1) # (task_id, machine_id, task_start_time)
    
    @property
    def n(self):
        return self._n
    
    @property
    def m(self):
        return self._m
    
    @property
    def task_list(self):
        return self._task_list
    
    @property
    def machine_list(self):
        return self._machine_list
    
    @property
    def next_added_task(self):
        return self._next_added_task
    
    @property
    def rcl_list(self):
        return self._rcl_list
    
    @next_added_task.setter
    def next_added_task(self, val: tuple):
        self._next_added_task = val

    @rcl_list.setter
    def rcl_list(self, val: list):
        self._rcl_list = val
    
    @staticmethod
    def _time_constraint(task: Task, machine: Machine, task_start_time: int) -> bool:
        flag = True
        if task_start_time < task.eraliest_start or task_start_time > task.latest_start:
            flag = False
        if task_start_time + task.duration > machine.end_time:
            flag = False
        return flag
    
    @staticmethod
    def _core_constraint(task: Task, machine: Machine, task_start_time: int) -> bool:
        flags = True
        if task_start_time < machine.start_time or task_start_time > machine.end_time:
            return False
        for t in range(task_start_time, task_start_time + task.duration):
            if machine.remaining_cores[t] < task.cores:
                flags = False
                break
        return flags
    
    def _able_to_add_task_to_machine(self, task_id: int, machine_id: int) -> bool:
        flag = False

        if self.task_list[task_id] is None:
            flag = False
        else:
            task = self.task_list[task_id]
            machine = self.machine_list[machine_id]

            for task_start_time in range(task.eraliest_start, task.latest_start + 1):
                if self._time_constraint(task, machine, task_start_time) == False:
                    continue
                else:
                    if self._core_constraint(task, machine, task_start_time):
                        flag = True
                        self.next_added_task = (task_id, machine_id, task_start_time)
                        break

        if flag == False:
            self.next_added_task = (-1, -1, -1)
        
        return flag
    
    def _add_task_to_machine(self, task_id: int, machine_id: int) -> None:
        task = self.task_list[task_id]
        machine = self.machine_list[machine_id]
        task_start_time = self.next_added_task[2]

        machine.add_task(task, task_start_time)


    def greedy(self):


        self.rcl_list.sort()

        # debugging
        for task in self.rcl_list:
            print(f"task_{task.id}: cores {task.cores}; duration {task.duration}; eraliest start {task.eraliest_start}; latest start {task.latest_start}")

        while self.rcl_list.__len__() > 0:

            task = self.rcl_list.pop(0)
            
            for machine_id in self.machine_list.keys():
                if self._able_to_add_task_to_machine(task.id, machine_id):
                    self._add_task_to_machine(task.id, machine_id)
                    break
    

    def local_search(self):
        pass

    def print_solution(self):

        obj_fun = 0

        for machine in self.machine_list.values():
            print(f"machine_{machine.id}: cores {machine.cores}; start time {machine.start_time}; shutdown time {machine.end_time}")
            for task_start_time, task_dict in machine.task_queue.items():
                if task_dict is not None:
                    for task_id, task in task_dict.items():
                        obj_fun += task.cores * task.duration
                        print(f"\t task_{task_id}: cores {task.cores}; start time {task_start_time}; end time {task_start_time + task.duration}")
            print()
        
        print(f"objective function value: {obj_fun}")


    