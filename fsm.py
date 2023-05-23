"""
Generating a Finite-State Machine (FSM)
to simulate an ordinary day in life
"""


import random
from time import sleep


def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper


class FSM:
    """
    Finite-State Machine class
    """
    def __init__(self) -> None:
        """
        Class content
        """
        # initialising start and possible states
        self._q0 = self._create_q0()
        self._q1 = self._create_q1()
        self._q2 = self._create_q2()
        self._q3 = self._create_q3()
        self._q4 = self._create_q4()
        self._q5 = self._create_q5()

        # initialising starting conditions
        self._current_state = self._q0
        self.finished = False

        # LOS (list of states)
        self.__los = {0: "SLEEP",
                      1: "WAKE UP",
                      2: "EAT",
                      3: "STUDY",
                      4: "RELAX"}
        # RES (random events) & probabilities
        self.__res = {"a": "FORGOT TO EAT",
                      "b": "DIDN'T HEAR THE ALARM CLOCK",
                      "c": "MET A FRIEND"}

        self.__res_probs = {"a": 0.2,
                            "b": 0.1,
                            "c": 0.5}

        # set up time periods for each state
        self.__sleeping_time = [0, 1, 2, 3, 4, 5, 6, 7]
        self.__waking_up = 8
        self.__eating_time = [9, 13, 18]
        self.__studying_time = [10, 11, 12, 14, 15, 16]
        self.__relax_time = [17, 19, 20, 21, 22, 23]
        self.__finish_time = 24

    def send(self, hour: int) -> None:
        """
        Send a value and initiate state change if possible
        :param hour: current hour
        :return: None
        """
        try:
            self._current_state.send(hour)
        except StopIteration:
            self.finished = True

    def day_finished(self) -> bool:
        """
        Check if the day is over.
        :return: True/False
        """
        if self.finished:
            return False
        return self._current_state == self._q5

    @prime
    def _create_q0(self) -> None:
        """
        Initiate state q0: SLEEP
        :return: None
        """
        while True:
            hour = yield
            re_chance = random.random()
            if hour == self.__waking_up:
                if re_chance < self.__res_probs["b"]:
                    print(f"It's {hour} o'clock. {self.__res['b']} happened! Now I do: {self.__los[0]}")
                    self._current_state = self._q0
                else:
                    print(f"It's {hour} o'clock. {self.__res['b']} did not happen! Currently I do: {self.__los[1]}")
                    self._current_state = self._q1
            elif hour in self.__studying_time:
                print(f"It's {hour} o'clock. I overslept! Now I do: {self.__los[3]}")
                self._current_state = self._q3
            else:
                print(f"It's {hour} o'clock. Currently I do: {self.__los[0]}")

    @prime
    def _create_q1(self) -> None:
        """
        Initialise state q1: AWAKE
        :return: None
        """
        while True:
            hour = yield
            re_chance = random.random()
            if hour in self.__eating_time and re_chance > self.__res_probs['a']:
                self._current_state = self._q2
                print(f"It's {hour} o'clock. Currently I do: {self.__los[2]}")
            elif hour in self.__eating_time and re_chance < self.__res_probs['a']:
                self._current_state = self._q3
                print(f"It's {hour} o'clock. {self.__res['a']} happened. Currently I do: {self.__los[3]}")
            elif hour in self.__studying_time:
                self._current_state = self._q3
                print(f"It's {hour} o'clock. Currently I do: {self.__los[3]}")
            else:
                print(f"It's {hour} o'clock. Currently I do: {self.__los[1]}")

    @prime
    def _create_q2(self) -> None:
        """
        Initialise state q2: EAT
        :return: None
        """
        while True:
            hour = yield
            if hour in self.__studying_time:
                self._current_state = self._q3
                print(f"It's {hour} o'clock. Currently I do: {self.__los[3]}")
            else:
                print(f"It's {hour} o'clock. Currently I do: {self.__los[2]}")

    @prime
    def _create_q3(self):
        """
        Initialise state q3: STUDY
        :return: None
        """
        while True:
            hour = yield
            re_chance = random.random()
            if hour in self.__relax_time:
                self._current_state = self._q4
                print(f"It's {hour} o'clock. Currently I do: {self.__los[4]}")
            elif hour in self.__eating_time and re_chance > self.__res_probs["a"]:
                self._current_state = self._q2
                print(f"It's {hour} o'clock. {self.__res['a']} did not happen! Now I do: {self.__los[2]}")
            elif hour in self.__eating_time and re_chance < self.__res_probs["a"]:
                print(f"It's {hour} o'clock. {self.__res['a']} happened! Currently I do: {self.__los[3]}")
            else:
                print(f"It's {hour} o'clock. Currently I do: {self.__los[3]}")

    @prime
    def _create_q4(self) -> None:
        """
        Initialise state q4: RELAX
        :return: None
        """
        while True:
            hour = yield
            re_chance = random.random()
            if hour == self.__finish_time and re_chance > self.__res_probs["a"]:
                self._current_state = self._q5
            elif re_chance < self.__res_probs["c"]:
                print(f"It's {hour} o'clock. {self.__res['c']} happened! Now I do: {self.__los[3]}")
                self._current_state = self._q3
            else:
                print(f"It's {hour} o'clock. Currently I do: {self.__los[4]}")

    @prime
    def _create_q5(self) -> None:
        """
        Initiate finish
        :return: None
        """
        while True:
            hour = yield
            if hour == self.__finish_time:
                print(f"It's {hour} o'clock. The day is over!")


def run(values) -> None:
    """
    Run the FSM
    :param values: list of hours
    :return: None
    """
    evaluator = FSM()
    for val in values:
        evaluator.send(val)
        sleep(1)


if __name__ == "__main__":
    vals = [i for i in range(24)]
    run(vals)
