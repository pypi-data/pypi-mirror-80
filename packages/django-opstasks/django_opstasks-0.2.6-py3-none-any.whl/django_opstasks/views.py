from celery.utils.log import get_task_logger
from django_opstasks.common.response import OpstasksResponse
from django_opstasks.common.response import AsyncResultResponse

LOGGER = get_task_logger('django')


# Create your views here.
def error_test(request):
    if request.method == "GET":
        from django_opstasks.tasks import error
        result = error.apply_async()
        if result.get():
            return AsyncResultResponse(result)
    return OpstasksResponse('Method Not Allowed', 405)


def sync_task_to_database(request):
    if request.method == "GET":
        from django_opstasks.tasks import sync_task_to_database as task
        result = task.apply_async()
        return AsyncResultResponse(result)
    return OpstasksResponse('Method Not Allowed', 405)
