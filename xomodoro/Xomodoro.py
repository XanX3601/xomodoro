import time

from .XomodoroState import XomodoroState


class Xomodoro:
    # constructor **************************************************************
    def __init__(
        self,
        focus_total=25,
        long_break_total=25,
        short_break_total=5,
        focus_till_long_break=4,
    ):
        self.__state = XomodoroState.stopped

        self.__state_to_sesstion_total = {
            XomodoroState.focus: focus_total * 60,
            XomodoroState.long_break: long_break_total * 60,
            XomodoroState.short_break: short_break_total * 60,
            XomodoroState.stopped: None,
        }

        self.__session_start = time.time()
        self.__session_total = self.__state_to_sesstion_total[self.__state]
        self.__session_elapsed = 0

        self.__focus_count_since_long_break = 0
        self.__focus_till_long_break = focus_till_long_break

    # control ******************************************************************
    def start(self):
        self.__state = XomodoroState.focus

        self.__session_start = time.time()
        self.__session_total = self.__state_to_sesstion_total[self.__state]
        self.__session_elapsed = 0

    def update(self):
        if self.__state == XomodoroState.stopped:
            return

        self.__session_elapsed = time.time() - self.__session_start

        if self.__session_elapsed >= self.__session_total:
            # focus since long break
            if self.__state == XomodoroState.focus:
                self.__focus_count_since_long_break += 1
            elif self.__state == XomodoroState.long_break:
                self.__focus_count_since_long_break = 0

            # state transition
            if (
                self.__state == XomodoroState.focus
                and self.__focus_count_since_long_break >= self.__focus_till_long_break
            ):
                self.__state = XomodoroState.long_break
            elif self.__state == XomodoroState.focus:
                self.__state = XomodoroState.short_break
            elif (
                self.__state == XomodoroState.short_break
                or self.__state == XomodoroState.long_break
            ):
                self.__state = XomodoroState.focus

            # reset
            self.__session_start = time.time()
            self.__session_total = self.__state_to_sesstion_total[self.__state]
            self.__session_elapsed = 0

    # property *****************************************************************
    @property
    def seconds(self):
        return self.__session_elapsed

    @property
    def state(self):
        return self.__state

    @property
    def total_seconds(self):
        return self.__session_total
