import queue
import concurrent.futures
from config.singleton import SingletonMeta
from worker_pool.worker import Worker


class Pool(metaclass=SingletonMeta):
    def __init__(self, num_workers):
        self.task_queue = queue.Queue()
        self.workers = [Worker(i, self.task_queue) for i in range(num_workers)]

        for worker in self.workers:
            worker_thread = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            worker_thread.submit(worker.run)

    def add_task(self, task):
        self.task_queue.put(task)

    def wait_completion(self):
        self.task_queue.join()

    def close(self):
        for _ in self.workers:
            self.task_queue.put(None)  # Add None tasks to signal workers to exit
        self.task_queue.join()