import pandas as pd
from numpy import datetime64 as time


# Create class time functionalities
class TimeFunc:
    def __init__(self):
        """
        This class presents a timer module that can be used by class habit.\n\n

        self.start_date = None \n
        self.timespan = None \n
        self.last_checked = None \n
        self.periodicity = None \n
        self.offset = None \n\n
        self.initialize(self, start_date: time, timespan: str, periodicity: int, last_checked=None) \n
        self.is_in_time(self)
        """
        self.start_date = None
        self.timespan = None
        self.last_checked = None
        self.periodicity = None
        self.offset = None
        self.time_data = pd.Series()

    def initialize(self, start_date: time, timespan: str, periodicity: int, last_checked=None):
        """
        Sets all attributes of TimeFunc object.
        :param start_date:  datetime64 object
        :param timespan: "days", "weeks", "months"
        :param periodicity: int number i.e.: 1 for 1 day
        :param last_checked: datetime64 object
        :return:
        """

        # days
        if timespan == "days":
            self.start_date = start_date
            self.periodicity = periodicity
            self.timespan = timespan
            self.offset = pd.offsets.DateOffset(days=periodicity)
            self.last_checked = last_checked

        # weeks
        if timespan == "weeks":
            self.start_date = start_date
            self.periodicity = periodicity
            self.timespan = timespan
            self.offset = pd.offsets.DateOffset(weeks=periodicity)
            self.last_checked = last_checked

        # months
        if timespan == "months":
            self.start_date = start_date
            self.periodicity = periodicity
            self.timespan = timespan
            self.offset = pd.offsets.DateOffset(months=periodicity)
            self.last_checked = last_checked

        if timespan not in ["months", "weeks", "days"]:
            raise NameError("typo in timespan argument")

    def is_in_time(self) -> int:
        """
        Checks if a timespan is met compared to the current local date.
        Returns 1 for is in time, 2 for is in the future, 0 for is in past
        :return: int
        """

        # For timespan days
        if self.timespan == "days":

            if self.last_checked is None:  # When last checked none use start date
                # When started today
                if self.start_date == time("now", "D"):
                    return 1
                # When has not been checked on start date
                elif self.start_date + self.offset <= time("now", "D"):
                    return 0
                # When the next possible check is in the future
                elif self.start_date > time("now", "D") or self.start_date + self.offset > time("now", "D"):
                    return 2

            # When next possible check is today
            elif self.last_checked + self.offset == time("now", "D"):
                return 1
            # When next possible check is in the future
            elif self.last_checked + self.offset > time("now", "D"):
                return 2
            # When next possible check is in the past
            elif self.last_checked + self.offset < time("now", "D"):
                return 0

        elif self.timespan == "weeks":

            # Check if last checked is None
            if self.last_checked is None:       # When last checked none use start date
                # Get necessary values from timer
                start_week = pd.Timestamp(self.start_date).week  # Get week number from start date
                start_year = pd.Timestamp(self.start_date).year  # Get year number from start date
                current_year = pd.Timestamp(time("now", "D")).year  # Get current year number
                current_week = pd.Timestamp(time("now", "D")).week  # Get current week number
                next_check_year = pd.Timestamp(self.start_date + self.offset).year  # Get year number for next check
                next_check_week = pd.Timestamp(self.start_date + self.offset).week  # Get week number for next check

                # When Start week is in current week
                if start_week == current_week and start_year == current_year:
                    return 1

                # When next possible check is in the future
                elif (next_check_week > current_week and next_check_year == current_year or
                      next_check_year > current_year):
                    return 2
                # When next possible check is in the past
                elif (next_check_week < current_week and next_check_year == current_year
                      or next_check_year < current_year):
                    return 0
            else:
                # Get necessary values from timer
                next_check_week = pd.Timestamp(self.last_checked + self.offset).week  # Get week number for next check
                next_check_year = pd.Timestamp(self.last_checked + self.offset).year  # Get year number for next check
                current_week = pd.Timestamp(time("now", "D")).week                    # Get current week number
                current_year = pd.Timestamp(time("now", "D")).year                    # Get current year number

                # When next possible check is in current week
                if next_check_week == current_week and next_check_year == current_year:
                    return 1

                # When next possible check is in the future
                elif (next_check_week > current_week and next_check_year == current_year or
                      next_check_year > current_year):
                    return 2

                # When next possible check is in the past
                elif (next_check_week < current_week and next_check_year == current_year or
                      next_check_year < current_year):
                    return 0

        elif self.timespan == "months":

            if self.last_checked is None:       # When last checked none use start date
                # Get necessary values from timer
                start_month = pd.Timestamp(self.start_date).month                     # Get month number from start_date
                start_year = pd.Timestamp(self.start_date).year                       # Get year number from start_date
                current_month = pd.Timestamp(time("now", "D")).month                  # Get current month number
                current_year = pd.Timestamp(time("now", "D")).year                    # Get current year number
                next_check_month = pd.Timestamp(self.start_date + self.offset).month  # Get month number for next check
                next_check_year = pd.Timestamp(self.start_date + self.offset).year    # Get year number for next check

                # When start month is current month
                if start_month == current_month and start_year == current_year:
                    return 1

                # When next possible check is in the future
                elif (next_check_month > current_month and next_check_year == current_year or
                      next_check_year > current_year):
                    return 2

                # When next possible check is in the past
                elif next_check_month < current_month or next_check_year < current_year:
                    return 0
            else:
                # Get necessary values from timer
                next_check_month = pd.Timestamp(self.last_checked + self.offset).month  # Get month number for next check
                next_check_year = pd.Timestamp(self.last_checked + self.offset).year    # Get year number for next check
                current_month = pd.Timestamp(time("now", "D")).month                    # Get current month number
                current_year = pd.Timestamp(time("now", "D")).year                      # Get current year number

                # When next possible check is current month
                if next_check_month == current_month and next_check_year == current_year:
                    return 1

                # When next possible check is in the future
                elif (next_check_month > current_month and next_check_year == current_year or
                      next_check_year > current_year):
                    return 2

                # When next possible check is in the past
                elif (next_check_month < current_month and next_check_year == current_year or
                      next_check_year < current_year):
                    return 0
