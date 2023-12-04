import multiprocessing
from config.singleton import SingletonMeta

from worker_pool.worker import Worker


class Pool(metaclass=SingletonMeta):
    def __init__(self, num_workers):
        self.num_workers = num_workers
        self.tasks = multiprocessing.Queue()
        self.results = multiprocessing.Queue()
        self.workers: list[Worker] = []

    def start(self):
        for _ in range(self.num_workers):
            worker = Worker(self.tasks, self.results)
            worker.start()
            self.workers.append(worker)

    def submit(self, task):
        self.tasks.put(task)

    def join(self):
        for _ in range(self.num_workers):
            self.tasks.put(None)
        for worker in self.workers:
            worker.join()

    def get_results(self):
        results = []
        while not self.results.empty():
            result = self.results.get()
            results.append(result)
        return results