import unittest

from jobs import worker
from jobs.task import BaseTask


class WorkerTest(unittest.TestCase):
    def test_work_timeout(self):
        task = TestTask(False, 3)
        worker.work(task)
        self.assertEqual(1, task.counter_done)
        self.assertEqual(4, task.counter_ready)
        self.assertEqual(1, task.counter_do)

    def test_work_done(self):
        task = TestTask(True)
        worker.work(task)
        self.assertEqual(1, task.counter_done)
        self.assertEqual(1, task.counter_ready)
        self.assertEqual(0, task.counter_do)

    def test_simply_do_work(self):
        task = TestTask(False)
        worker.work(task)
        self.assertEqual(1, task.counter_done)
        self.assertEqual(1, task.counter_ready)
        self.assertEqual(1, task.counter_do)


class TestTask(BaseTask):
    def __init__(self, tdone: bool, retry: int = 0):
        super().__init__(None, None)
        self.counter_ready = 0
        self.counter_do = 0
        self.counter_done = 0
        self.tdone = tdone
        self.retry = retry

    def done(self):
        self.counter_done += 1
        return self.tdone

    def do(self):
        self.counter_do += 1
        return 'http://google.ch'

    def ready(self):
        self.counter_ready += 1
        return self.counter_ready > self.retry


if __name__ == '__main__':
    unittest.main()
