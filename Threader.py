import queue


class manager():

    def __init__(self):
        self.task_queue = queue.Queue()
        self.after(500, self.poll)

    def poll(self):
        while not self.task_queue.empty():
            task = self.task_queue.get()
            task()
        self.root.after(500, self.poll)

    def add_task(self, task):
        self.task_queue.put(task)

    def callback(self):
        os._exit(0)
