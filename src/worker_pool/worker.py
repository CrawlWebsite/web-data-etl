import multiprocessing

class Worker(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            task = self.task_queue.get()
            print(task)
            if task is None:
                break
            result = task.execute()
            self.result_queue.put(result)