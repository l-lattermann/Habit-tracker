import numpy as np
from habit_tracker import class_TimeFunc as Ts


# Create class Habit
class Habit:
    list = {}

    def __init__(self, name: str):
        """
        Instances of Habit store all data about habits. \n
        self.name = name \n
        self.timer = TimeFunc() \n
        self.counter = 0 \n
        self.streak = 0 \n\n
        check_habit(self) \n
        delete_habit(self)\n

        :param name: Name for habit, will be set as key in Habit.list{}
        """

        self.name = name
        self.timer = Ts.TimeFunc()      # Class TimeFunc host all the time related functionalities
        self.counter = 0
        self.streak = 0
        Habit.list[self.name] = self    # Put habit into habit list to access it easily

    def check_habit(self) -> int:
        """
        Checks the offset and either increases the h counter by one or breaks the habit.
        Returns 0 if habit was broken, 1 if habit was checked, 2 if habit was not checked
        because its in the future.
        :return: int
        """

        is_in_time = self.timer.is_in_time()        # Is 1 for yes, 0 for to late, 2 for in the future

        if is_in_time == 1:
            self.counter += 1       # increase counter by one
            self.timer.last_checked = np.datetime64("now", "D")     # set last_check today
            self.timer.time_data[np.datetime64("now")] = "checked"        # Insert the check event into time_data

            if self.counter > self.streak:      # if counter is bigger than streak, increase counter
                self.streak = self.counter

            return 1    # habit was checked

        elif is_in_time == 0:
            self.counter = 0        # Habit was broken, set counter to zero

            if self.timer.last_checked is None:     # If habit was not checked before use start date
                x = self.timer.start_date
            else:
                x = self.timer.last_checked + self.timer.offset     # next possible check date

            # Insert failed into time_data series for all dates that should have been checked
            while x < np.datetime64("now"):
                self.timer.time_data[x] = "failed"
                x += self.timer.offset      # Iterate through all dates that should have been checked
            self.timer.last_checked = np.datetime64("now", "D")     # set last_checked today
            return 0    # habit was broken

        elif is_in_time == 2:
            return 2    # habit can not be checked because in future

    def delete_habit(self):
        """
        Deletes habit from habit list.
        :return:
        """
        Habit.list.pop(self.name)
        del self
