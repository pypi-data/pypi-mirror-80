from abc import (
    ABCMeta,
)
from typing import (
    Optional,
)

from function_tools.helpers import (
    BaseFunctionHelper,
    BaseRunnerHelper,
)
from function_tools.validators import (
    BaseValidator,
)


class HelperMixin(metaclass=ABCMeta):
    """
    Миксин для появления помощника у сущности
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._helper: Optional[BaseFunctionHelper] = None

        self._prepare_helper()

    def _prepare_helper(self):
        """
        Точка расширения для создания помощника.
        """


class ValidatorMixin(metaclass=ABCMeta):
    """
    Миксин для появления валидатора у сущности
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._validator: Optional[BaseValidator] = None

        self._prepare_validator()

    def _prepare_validator(self):
        """
        Точка расширения для создания валидатора
        """

    def validate(self):
        """
        Публичный метод для запуска валидатора сущности
        """
        if self._validator:
            self._validator.validate(self)


class GlobalHelperMixin(metaclass=ABCMeta):
    """
    Миксин добавляющий возможность установки глобального помощника
    """
    def __init__(self, *args, global_helper=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._global_helper: Optional[BaseRunnerHelper] = (
            global_helper or
            self._prepare_global_helper()
        )

    def _prepare_global_helper(self):
        """
        Предназначен для определения глобального помощника
        """

    def set_global_helper(
        self,
        global_helper: BaseRunnerHelper,
    ):
        """
        Публичный метод для установки глобального помощника
        """
        self._global_helper = global_helper
