class Task:
    def __init__(self, func, args=(), kwargs=None):
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}

    def execute(self):
        return self.func(*self.args, **self.kwargs)
