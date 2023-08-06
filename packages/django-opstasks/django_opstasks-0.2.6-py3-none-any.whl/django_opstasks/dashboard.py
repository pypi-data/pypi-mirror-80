from json import loads
from logging import getLogger

from django_redis import get_redis_connection
from django_opstasks.models import TaskResult


LOGGER = getLogger('django')
PRE_DEFINED_QUEUES = ['BJ', 'IN', 'ID', 'SG', 'PHI']


class OpstasksBroker():
    def __init__(self):
        self.redis_connection = get_redis_connection('opstasks')

    def workers(self):
        """
        Get workers from key is "_kombu.binding.celery.pidbox" in the OpstasksBroker,
        return a list
        """
        LOGGER.info('Get workers from key is "_kombu.binding.celery.pidbox" in the OpstasksBroker')
        redis_connection = get_redis_connection('opstasks')
        workers = redis_connection.smembers('_kombu.binding.celery.pidbox')
        LOGGER.info("return %s", workers)
        return workers

    def task_in_queues(self):
        """
        获取队列中的任务
        """
        tasks_list = []
        count = []
        total = 0
        tasks = lambda queue: self.redis_connection.lrange(queue, 0, -1)
        for queue in PRE_DEFINED_QUEUES:
            count.append(f'"{queue}": {len(tasks(queue))}')
            total += len(tasks(queue))
            for task in tasks(queue):
                task = loads(task)
                _temp = {
                    "datetime": "2020-09-25 21:07:00",
                    "task": task['headers']['task'],
                    "queue": task['properties']['delivery_info']['routing_key']
                }
                tasks_list.append(_temp)
        return {
            "list": tasks_list,
            "count": ','.join(count),
            "total": total,
        }


class OpstasksBackend():
    def __init__(self):
        self.task_results = TaskResult.objects.all()

    def execution_trend(self):
        """
        [['2019-10-10', 200], ['2019-10-11', 400], ['2019-10-12', 650]
        """
        results = []
        import datetime
        today = datetime.datetime.utcnow()
        days = list(reversed([today - datetime.timedelta(days=num) for num in range(30)]))
        for day in days:
            result = self.task_results.filter(
                date_start__year=day.year,
                date_start__month=day.month,
                date_start__day=day.day)
            results.append([day.strftime('%Y-%m-%d'), len(result)])
        return results

    def tasks_exe_count_in_queue(self):
        """
        number of task executions in the queue
          [
            {"value": 90, "name": 'BJ'},
            {"value": 30, "name": 'SG'},
            {"value": 10, "name": 'IN'},
            {"value": 20, "name": 'ID'},
            {"value": 10, "name": 'PHI'}
          ]
        """
        results = []
        for queue in PRE_DEFINED_QUEUES:
            result = {
                "value": self.task_results.filter(queue=queue).count(),
                "name": queue
            }
            results.append(result)
        return results

    def workers_in_queue(self):
        # TODO
        return [
            {"value": 0, "name": 'BJ'},
            {"value": 0, "name": 'SG'},
            {"value": 0, "name": 'IN'},
            {"value": 0, "name": 'ID'},
            {"value": 0, "name": 'PHI'}
        ]

    def tasks_total_count_with_all(self):
        return self.task_results.count()


def create_dashboard_dataset():
    broker = OpstasksBroker()
    backend = OpstasksBackend()
    data = {
        "title": "分布式任务系统",
        "notifications": [{"level": 'success', "message": '欢迎使用运维分布式任务系统'},],
        "task": {
            "in_queues": broker.task_in_queues(),
            "execution_trend": backend.execution_trend()
        },
        "workers_count": len(broker.workers()),
        "queue": {
            "queues": PRE_DEFINED_QUEUES,
            "status": 'OK',
            "worker": backend.workers_in_queue(),
            "tasks_run_count": backend.tasks_exe_count_in_queue()
        },
        "tasks_total_count": backend.tasks_total_count_with_all(),
    }
    return data
