import threading


class Worker(threading.Thread):
    def __init__(self, thread_id, task_queue):
        super(Worker, self).__init__()
        self.thread_id = thread_id
        self.task_queue = task_queue

    def run(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                break  # Exit when a None task is encountered
            print(f"Thread {self.thread_id} processing Task {task.task_id}")
            task.task_function(*task.args)
            self.task_queue.task_done()