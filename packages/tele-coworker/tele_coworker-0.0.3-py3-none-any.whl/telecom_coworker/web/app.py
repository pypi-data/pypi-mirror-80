from flask import Flask, request

from telecom_coworker.client import Client
from telecom_coworker.models import Task
from telecom_coworker.web import ok, fail
from telecom_coworker.web.config import Config

app = Flask(__name__)
app.config.from_object(Config)

tele_client = Client(namespace=app.config['ZK_NAMESPACE'],
                     hosts=app.config['ZK_HOSTS'])
tele_client.connect()


@app.route('/task', methods=['POST'])
def create_task():
    try:
        task: Task = request.json
    except AttributeError as e:
        return fail(40, "需要参数: task_type:str[len>5], params:dict")

    if len(task["task_type"]) < 5:
        return fail(41, '需要参数: task_type:str[len>5]')

    tid = tele_client.add_task(task["task_type"], **task['params'])

    return ok({"task_id": tid})


@app.route('/task/<uuid:task_id>/cancel', methods=['GET', 'POST'])
def cancel_task(task_id):
    result = tele_client.cancel_task(task_id)
    if result:
        return ok()
    else:
        return fail('没有找到对应的Task')
