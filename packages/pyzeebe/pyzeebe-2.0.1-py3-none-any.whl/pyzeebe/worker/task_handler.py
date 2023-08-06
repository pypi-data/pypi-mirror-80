import logging
from abc import abstractmethod
from typing import Tuple, List, Callable

from pyzeebe.common.exceptions import TaskNotFound, NoVariableNameGiven
from pyzeebe.decorators.zeebe_decorator_base import ZeebeDecoratorBase
from pyzeebe.job.job import Job
from pyzeebe.task.exception_handler import ExceptionHandler
from pyzeebe.task.task import Task
from pyzeebe.task.task_decorator import TaskDecorator


def default_exception_handler(e: Exception, job: Job) -> None:
    logging.warning(f"Task type: {job.type} - failed job {job}. Error: {e}.")
    job.set_failure_status(f"Failed job. Error: {e}")


class ZeebeTaskHandler(ZeebeDecoratorBase):
    def __init__(self, before: List[TaskDecorator] = None, after: List[TaskDecorator] = None):
        """
        Args:
            before (List[TaskDecorator]): Decorators to be performed before each task
            after (List[TaskDecorator]): Decorators to be performed after each task
        """
        super().__init__(before, after)
        self.tasks: List[Task] = []

    def task(self, task_type: str, exception_handler: ExceptionHandler = default_exception_handler,
             before: List[TaskDecorator] = None, after: List[TaskDecorator] = None, single_value: bool = False,
             variable_name: str = None):
        """Decorator to create a task
        single_value (bool): If the function returns a single value (int, string, list) and not a dictionary set this to
                             True.
        variable_name (str): If single_value then this will be the variable name given to zeebe:
                                    { <variable_name>: <function_return_value> }
        """
        if single_value and not variable_name:
            raise NoVariableNameGiven(task_type=task_type)

        elif single_value and variable_name:
            return self._non_dict_task(task_type=task_type, variable_name=variable_name,
                                       exception_handler=exception_handler, before=before, after=after)

        else:
            return self._dict_task(task_type=task_type, exception_handler=exception_handler, before=before, after=after)

    @abstractmethod
    def _dict_task(self, task_type: str, exception_handler: ExceptionHandler = default_exception_handler,
                   before: List[TaskDecorator] = None, after: List[TaskDecorator] = None):
        raise NotImplemented()

    @abstractmethod
    def _non_dict_task(self, task_type: str, variable_name: str,
                       exception_handler: ExceptionHandler = default_exception_handler,
                       before: List[TaskDecorator] = None, after: List[TaskDecorator] = None):
        raise NotImplemented()

    @staticmethod
    def _single_value_function_to_dict(variable_name: str, fn: Callable):
        def inner_fn(*args, **kwargs):
            return {variable_name: fn(*args, **kwargs)}

        return inner_fn

    def remove_task(self, task_type: str) -> Task:
        task_index = self._get_task_index(task_type)
        return self.tasks.pop(task_index)

    def get_task(self, task_type: str) -> Task:
        return self._get_task_and_index(task_type)[0]

    def _get_task_index(self, task_type: str) -> int:
        return self._get_task_and_index(task_type)[-1]

    def _get_task_and_index(self, task_type: str) -> Tuple[Task, int]:
        for index, task in enumerate(self.tasks):
            if task.type == task_type:
                return task, index
        raise TaskNotFound(f"Could not find task {task_type}")
