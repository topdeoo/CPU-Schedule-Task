class Task:
    def __init__(self, id: int, cores: int, eraliest_start:int, latest_start: int, duration: int) -> None:
        self._id = id
        self._cores = cores
        self._eraliest_start = eraliest_start
        self._latest_start = latest_start
        self._duration = duration
    
    @property
    def cores(self):
        return self._cores
    
    @property
    def eraliest_start(self):
        return self._eraliest_start
    
    @property
    def latest_start(self):
        return self._latest_start
    
    @property
    def duration(self):
        return self._duration
    
    @property
    def id(self):
        return self._id
    
    def __lt__(self, other):
        return self.cores * self.duration > other.cores * other.duration

