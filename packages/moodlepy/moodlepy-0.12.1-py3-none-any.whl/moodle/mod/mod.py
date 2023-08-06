from moodle import BaseMoodle
from . import BaseAssign, BaseForum, BaseLesson, BaseResource


class Mod(BaseMoodle):
    def __post_init__(self, moodle) -> None:
        self._assign = BaseAssign(moodle)
        self._forum = BaseForum(moodle)
        self._lesson = BaseLesson(moodle)
        self._resource = BaseResource(moodle)

    @property
    def assign(self) -> BaseAssign:
        return self._assign

    @property
    def forum(self) -> BaseForum:
        return self._forum

    @property
    def lesson(self) -> BaseLesson:
        return self._lesson

    @property
    def resource(self) -> BaseResource:
        return self._resource
