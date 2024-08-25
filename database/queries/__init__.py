# database.queries.__init__.py

from .task_queries import (
    get_tasks_by_date,
    get_all_tasks,
    create_task,
    update_task_status,
    delete_task
)

__all__ = [
    'get_tasks_by_date',
    'get_all_tasks',
    'create_task',
    'update_task_status',
    'delete_task'
]
