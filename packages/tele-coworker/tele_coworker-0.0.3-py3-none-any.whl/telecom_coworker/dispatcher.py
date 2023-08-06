"""Dispatcher run

Usage:
  dispatcher.py NAMESPACE ZK_HOSTS
"""
import json
import logging
import random
from collections import defaultdict
from functools import reduce

import click
from kazoo.client import KazooClient

from telecom_coworker import log
from telecom_coworker.cache.tasks_cache import TasksCache
from telecom_coworker.cache.workers_cache import WorkersCache
from telecom_coworker.models import Task
from telecom_coworker.models import WorkerInfo
from telecom_coworker.utils import set_interval, search_dict_by_keys


class Dispatcher(object):

    def __init__(self, namespace, hosts="localhost:2181"):
        self.namespace = namespace
        self.zk = KazooClient(hosts=hosts)
        self.namespace = namespace
        self._tasks_cache = None
        self._workers_cache = None
        self._assign_cache = None

        self._worker_infos = dict()
        self._task_infos = dict()

    def _watch_tasks(self, next_tasks):
        self._tasks_cache.update(next_tasks)
        self.assign_tasks()

    def _watch_workers(self, next_workers):
        self._workers_cache.update(next_workers)
        self.assign_tasks()

    def _master_func(self):
        log.info("I ready to by a good dispatcher")
        self._tasks_cache = TasksCache(set(self.zk.get_children(f"{self.namespace}/tasks")))
        self._workers_cache = WorkersCache(set(self.zk.get_children(f"{self.namespace}/workers")))
        self._tasks_cache.next_version(self.canceled_tasks_handle, self.added_tasks_handle)
        self._workers_cache.next_version(self.lost_workers_handle, self.added_workers_handle)

        self._assign_cache = self._assign_load()

        self.zk.ChildrenWatch(f"{self.namespace}/tasks")(self._watch_tasks)
        self.zk.ChildrenWatch(f"{self.namespace}/workers")(self._watch_workers)

    def canceled_tasks_handle(self, canceled_tasks):
        log.info(f"canceled tasks: {canceled_tasks}")
        unassign_worker_task = search_dict_by_keys(self._assign_cache, canceled_tasks)
        self._unassign_tasks(unassign_worker_task)

        for t in canceled_tasks:
            if t in self._task_infos:
                self._task_infos.pop(t)

    def lost_workers_handle(self, lost_workers):
        log.info(f"lost workers: {lost_workers}")
        self._unassign_workers(lost_workers)

        for w in lost_workers:
            if w in self._worker_infos:
                self._worker_infos.pop(w)

    def added_workers_handle(self, added_workers):
        log.info(f"added workers: {added_workers}")
        for w in added_workers:
            worker_info, _ = self.zk.get(f"{self.namespace}/workers/{w}")
            w_info: WorkerInfo = json.loads(worker_info.decode('utf-8'))
            self._worker_infos[w] = w_info

    def added_tasks_handle(self, added_tasks):
        log.info(f"added tasks: {added_tasks}")
        for t in added_tasks:
            task_info, _ = self.zk.get(f"{self.namespace}/tasks/{t}")
            t_info: Task = json.loads(task_info.decode('utf-8'))
            self._task_infos[t] = t_info

    def assign_tasks(self):
        self._tasks_cache.next_version(self.canceled_tasks_handle, self.added_tasks_handle)
        self._workers_cache.next_version(self.lost_workers_handle, self.added_workers_handle)

        assigned_tasks = reduce(lambda s1, s2: s1 | s2, self._assign_cache.values(), set())
        unassigned_tasks = self._tasks_cache.tasks - assigned_tasks

        dt = defaultdict(list)
        for ut in unassigned_tasks:
            dt[self._task_infos[ut]["task_type"]].append(self._task_infos[ut])

        assign_count = {w: len(tasks) for w, tasks in self._assign_cache.items()}

        dw = defaultdict(list)
        for w in self._worker_infos.values():
            dw[w["handle_type"]].append(w)

        for task_type in dt:
            tasks = dt[task_type]

            for t in tasks:
                workers = [w for w in dw[task_type] if w.get("max_handle_num", 2) - assign_count.get(w['wid'], 0) > 0]
                if not workers:
                    log.warning(f"WARNING: Task type {task_type} need more worker")
                    break
                w = random.choice(workers)
                self.assign_task_to_worker(t, w)
                assign_count[w['wid']] = assign_count.get(w['wid'], 0) + 1

    def assign_task_to_worker(self, task, worker):
        t = task["tid"]
        w = worker['wid']
        log.info("assign task %s to worker: %s", t, w)
        task_content = json.dumps(task).encode("utf-8")
        self.zk.create(f"{self.namespace}/assign/{w}/{t}", task_content, makepath=True)
        self._assign_cache[w].add(t)

    def _assign_load(self):
        m = defaultdict(set)

        assigned_workers = self.zk.get_children(f"{self.namespace}/assign")
        valid_assigned_workers = []
        invalid_assigned_workers = []
        for w in assigned_workers:
            if w in self._workers_cache.workers:
                valid_assigned_workers.append(w)
            else:
                invalid_assigned_workers.append(w)

        for w in invalid_assigned_workers:
            self.zk.delete(f"{self.namespace}/assign/{w}", recursive=True)

        for w in valid_assigned_workers:
            children = self.zk.get_children(f"{self.namespace}/assign/{w}")
            for task in children:
                m[w].add(task)

        return m

    def _unassign_tasks(self, worker_task_map: defaultdict):
        for w, tasks in worker_task_map.items():
            log.info("unassign task: %s by worker: %s", tasks, w)

            for t in tasks:
                self.zk.delete(f"{self.namespace}/assign/{w}/{t}")
                self._assign_cache[w].discard(t)

    def _unassign_workers(self, workers):
        for w in workers:
            self.zk.delete(f"{self.namespace}/assign/{w}", recursive=True)
            if w in self._assign_cache:
                self._assign_cache.pop(w)

    def _ensure_base_node(self):
        self.zk.ensure_path(f"{self.namespace}/tasks")
        self.zk.ensure_path(f"{self.namespace}/workers")
        self.zk.ensure_path(f"{self.namespace}/assign")

    def run(self):
        self.zk.start()
        self._ensure_base_node()
        election = self.zk.Election(f"{self.namespace}/master")
        election.run(self._master_func)

    def inspect(self):
        log.info(
            f"dispatch cache: w: {len(self._workers_cache)} t: {len(self._tasks_cache)} a: {len(self._assign_cache)} i: {len(self._worker_infos)}")
        log.info(f"assign cache: {self._assign_cache}")


@click.command()
@click.argument("namespace")
@click.argument("zk_hosts")
def main(namespace, zk_hosts):
    logging.basicConfig(level=logging.INFO)

    dispatcher = Dispatcher(namespace, zk_hosts)
    dispatcher.run()

    set_interval(dispatcher.inspect)


if __name__ == '__main__':
    main()
