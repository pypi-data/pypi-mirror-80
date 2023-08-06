import atexit
import json
from json import JSONDecodeError
from multiprocessing import Process
from uuid import uuid4 as uuid

from kazoo.client import KazooClient

from telecom_coworker import log
from telecom_coworker.models import WorkerInfo, Task


class Coworker(object):
    def __init__(self, namespace, hosts="localhost:2181", worker_id=None):
        self.namespace = namespace
        self.zk = KazooClient(hosts=hosts)
        self.worker_id = worker_id if worker_id is not None else f"worker-{uuid()}"

        self._current_task_ids = set()
        self._current_task_infos = dict()
        self._current_task_processes = dict()

    def run(self, handle_type, handle_num, func):
        self.zk.start()
        self.zk.ensure_path(f"{self.namespace}/assign/{self.worker_id}")

        @self.zk.ChildrenWatch(f"{self.namespace}/assign/{self.worker_id}")
        def watch_assign_task(children):
            next_tasks_ids = set(children)

            canceled_task_ids = self._current_task_ids - next_tasks_ids
            self.handle_canceled_tasks(canceled_task_ids)

            added_task_ids = next_tasks_ids - self._current_task_ids
            self.handle_added_tasks(added_task_ids, func)

            self._current_task_ids = next_tasks_ids

        worker_info = WorkerInfo(wid=self.worker_id, handle_type=handle_type, max_handle_num=handle_num)
        self.zk.create(f"{self.namespace}/workers/{self.worker_id}",
                       json.dumps(worker_info).encode("utf-8"), ephemeral=True)

        atexit.register(self.close)

    def close(self):
        if self.zk and self.zk.connected:
            self.zk.stop()
            self.zk.close()

    def handle_canceled_tasks(self, canceled_task_ids):
        log.info(f"handle canceled tasks: {canceled_task_ids}")
        for tid in canceled_task_ids:
            process = self._current_task_processes.get(tid)
            log.info(f"KILL task process: {process.ident}")
            if process:
                process.terminate()

                self._current_task_processes.pop(tid)
                self._current_task_infos.pop(tid)

    def handle_added_tasks(self, added_task_ids, func):
        log.info(f"handle added tasks {added_task_ids}")
        for tid in added_task_ids:
            try:
                task_content, _ = self.zk.get(f"{self.namespace}/assign/{self.worker_id}/{tid}")
                task: Task = json.loads(task_content.decode('utf-8'))
            except JSONDecodeError as e:
                log.error(e.msg, stack_info=True)
                continue

            process = Process(target=func, kwargs=task["params"])
            process.start()
            log.info(f"TASK[{task}] run on PID: {process.ident}")

            self._current_task_infos[tid] = task
            self._current_task_processes[tid] = process
