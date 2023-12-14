class Machine:
    @property
    def id(self):
        return self._id

    @property
    def cores(self):
        return self._cores
    
    @property
    def remaining_cores(self):
        return self._remaining_cores

    @property
    def start_time(self)->int:
        return self._start_time
    
    @property
    def end_time(self):
        return self._end_time
    
    @property
    def task_queue(self):
        return self._task_queue

    def __init__(self, id, cores, start_time, end_time) -> None:
        self._id = id
        self._cores = cores
        self._remaining_cores = dict()
        self._start_time = start_time
        self._end_time = end_time
        self._task_queue = dict()
        for i in range(start_time, end_time + 1):
            self._task_queue[i] = dict()
            self._remaining_cores[i] = cores
        
    def add_task(self, task, task_start_time) -> None:
        self.task_queue[task_start_time][task.id] = task
        
        for t in range(task_start_time, task_start_time + task.duration):
            self.remaining_cores[t] -= task.cores
    
    def remove_task(self, task_start_time, task_id) -> bool:
        if self.task_queue[task_start_time] is not None:
            task = self.task_queue[task_start_time][task_id]
            
            for t in range(task_start_time, task_start_time + task.duration):
                self.remaining_cores[t] += task.cores

            self.task_queue[task_start_time].pop(task_id)
            return True
        else:
            return False
    

    