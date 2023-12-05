class Task:
    def __init__(self, task_id, task_function, args=()):
        self.task_id = task_id
        self.task_function = task_function
        self.args = args
