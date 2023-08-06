from typing import TypedDict


class WorkerInfo(TypedDict):
    wid: str
    handle_type: str
    max_handle_num: int
    curr_handle_num: int


class Task(TypedDict):
    tid: str
    task_type: str
    params: dict


if __name__ == '__main__':
    w = WorkerInfo(wid="my_wid", handle_type="type1", max_handle_num=10)
    print(w.get("curr_handle_num", 0))
    w["curr_handle_num"] = 10
    print(w)
