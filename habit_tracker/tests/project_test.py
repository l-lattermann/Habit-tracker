import pytest
import coverage
import numpy as np
import pandas as pd
import pathlib

from habit_tracker import (SQL_functionalities,
                           class_habit as h,
                           analytics)


cov = coverage.Coverage()
cov.start()



class TestHabit:
    def setup_method(self):
        self.drinking = h.Habit("drinking")

    def test_empty_habit(self):
        # Test if all values are zero after habit creation
        assert self.drinking.name == "drinking"
        assert self.drinking.counter == 0
        assert self.drinking.streak == 0
        assert self.drinking.timer.time_data.empty
        assert self.drinking.timer.last_checked is None
        assert self.drinking.timer.offset is None
        assert self.drinking.timer.start_date is None
        assert self.drinking.timer.periodicity is None
        assert self.drinking.timer.timespan is None

        # Test setting up habit timer, checking if all values were set correctly
        self.drinking.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="days", periodicity=1)
        assert self.drinking.name == "drinking"
        assert self.drinking.counter == 0
        assert self.drinking.streak == 0
        assert self.drinking.timer.time_data.empty
        assert self.drinking.timer.last_checked is None
        assert self.drinking.timer.offset == pd.offsets.DateOffset(days=1)
        assert self.drinking.timer.start_date == np.datetime64("2023-11-06")
        assert self.drinking.timer.periodicity == 1
        assert self.drinking.timer.timespan == "days"

        # Test if habit is in habit list
        assert h.Habit.list["drinking"] == self.drinking

    def teardown_method(self):
        self.drinking.delete_habit()


class TestHabitCounter:
    def setup_method(self):
        # Create dates for testing
        self.habit = h.Habit("habit")  # Create habit
        self.now = np.datetime64("now", "D")  # Get current date
        self.last_day = self.now - pd.offsets.DateOffset(days=1)  # Calculate last day from current date
        self.last_week = self.now - pd.offsets.DateOffset(weeks=1)  # Calculate last week from current date
        self.last_month = self.now - pd.offsets.DateOffset(months=1)  # Calculate last month from current date
        self.future = self.now + pd.offsets.DateOffset(months=1)

    def test_check_habit(self):
        # Test if counter and streak increment correctly when habit is checked
        # days
        self.habit.timer.initialize(start_date=self.last_day, timespan="days", periodicity=1,
                                    last_checked=self.last_day)
        self.habit.counter = 0
        self.habit.streak = 0
        self.habit.check_habit()  # Streak and counter = zero -> check habit -> streak and counter = 1
        assert self.habit.counter == 1
        assert self.habit.streak == 1

        # weeks
        self.habit.timer.initialize(start_date=self.last_week, timespan="weeks", periodicity=1,
                                    last_checked=self.last_week)
        self.habit.counter = 0
        self.habit.streak = 0
        self.habit.check_habit()  # Streak and counter = zero -> check habit -> streak and counter = 1
        assert self.habit.counter == 1
        assert self.habit.streak == 1

        # months
        self.habit.timer.initialize(start_date=self.last_month, timespan="months", periodicity=1,
                                    last_checked=self.last_month)
        self.habit.counter = 0
        self.habit.streak = 0
        self.habit.check_habit()  # Streak and counter = zero -> check habit -> streak and counter = 1
        assert self.habit.counter == 1
        assert self.habit.streak == 1

        # Test if counter and streak behave correctly when habit is broken
        # Therefor create dates that are too far in the past
        self.two_days = self.now - pd.offsets.DateOffset(days=2)  # Offset now 2 days
        self.two_weeks = self.now - pd.offsets.DateOffset(weeks=2)  # Offset now 2 weeks
        self.two_months = self.now - pd.offsets.DateOffset(months=2)  # Offset now 2 months
        # days
        self.habit.timer.initialize(start_date=self.last_day, timespan="days", periodicity=1,
                                    last_checked=self.two_days)
        self.habit.counter = 10
        self.habit.streak = 10
        self.habit.check_habit()  # Streak and counter = 10 -> break habit -> streak = 10 and counter = 0
        assert self.habit.counter == 0
        assert self.habit.streak == 10

        # weeks
        self.habit.timer.initialize(start_date=self.last_week, timespan="weeks", periodicity=1,
                                    last_checked=self.two_weeks)
        self.habit.counter = 10
        self.habit.streak = 10
        self.habit.check_habit()  # Streak and counter = 10 -> break habit -> streak = 10 and counter = 0
        assert self.habit.counter == 0
        assert self.habit.streak == 10

        # months
        self.habit.timer.initialize(start_date=self.last_month, timespan="months", periodicity=1,
                                    last_checked=self.two_months)
        self.habit.counter = 10
        self.habit.streak = 10
        self.habit.check_habit()  # Streak and counter = 10 -> break habit -> streak = 10 and counter = 0
        assert self.habit.counter == 0
        assert self.habit.streak == 10

        # Check if check habit detects that next check is in the future correctly
        self.habit.timer.initialize(start_date=self.future, timespan="months", periodicity=1,
                                    last_checked=None)
        # Values make no sense but ensure that streak and counter are not manipulated when habit is in the future
        self.habit.counter = 10
        self.habit.streak = 10
        self.habit.check_habit()  # Streak and counter = 10 -> future habit -> streak = 10 and counter = 10
        assert self.habit.counter == 10
        assert self.habit.streak == 10

        # Check if check habit work with start date only when habit is broken
        self.habit.timer.initialize(start_date=self.last_month, timespan="days", periodicity=1,
                                    last_checked=None)
        # Values make no sense but ensure that streak and counter are not manipulated when habit is in the future
        self.habit.counter = 10
        self.habit.streak = 10
        self.habit.check_habit()  # Streak and counter = 10 -> break habit -> streak = 10 and counter = 0
        assert self.habit.counter == 0
        assert self.habit.streak == 10

    def teardown_method(self):
        self.habit.delete_habit()
        del self.habit
        del self


class TestTimeFuncModule:

    def setup_method(self):
        # Create Dates for testing
        self.habit = h.Habit("habit")  # Create habit
        self.now = np.datetime64("now", "D")  # Get current date
        self.last_day = self.now - pd.offsets.DateOffset(days=1)  # Calculate last day from current date
        self.last_week = self.now - pd.offsets.DateOffset(weeks=1)  # Calculate last week from current date
        self.last_month = self.now - pd.offsets.DateOffset(months=1)  # Calculate last month from current date

    def test_timer_is_in_time(self):
        # Test the is_in_time_function with different combinations
        #
        # Check if in time is working correctly
        # With start_date, last_checked is none
        # days
        self.habit.timer.initialize(start_date=self.now, timespan="days", periodicity=1, last_checked=None)
        assert self.habit.timer.is_in_time() == 1
        # weeks
        self.habit.timer.initialize(start_date=self.now, timespan="weeks", periodicity=1, last_checked=None)
        assert self.habit.timer.is_in_time() == 1
        # months
        self.habit.timer.initialize(start_date=self.now, timespan="months", periodicity=1, last_checked=None)
        assert self.habit.timer.is_in_time() == 1

        # With last_checked, start_date is something
        # days
        self.habit.timer.initialize(start_date=self.now, timespan="days", periodicity=1, last_checked=self.last_day)
        assert self.habit.timer.is_in_time() == 1
        # weeks
        self.habit.timer.initialize(start_date=self.now, timespan="weeks", periodicity=1, last_checked=self.last_week)
        assert self.habit.timer.is_in_time() == 1
        # months
        self.habit.timer.initialize(start_date=self.now, timespan="months", periodicity=1, last_checked=self.last_month)
        assert self.habit.timer.is_in_time() == 1

        # Check if to late is working correctly
        # Therefor create start dates that are too far in the past
        self.two_days = self.now - pd.offsets.DateOffset(days=2)  # Offset now 2 days
        self.two_weeks = self.now - pd.offsets.DateOffset(weeks=2)  # Offset now 2 weeks
        self.two_months = self.now - pd.offsets.DateOffset(months=2)  # Offset now 2 months
        # With start_date
        # days
        self.habit.timer.initialize(start_date=self.two_days, timespan="days", periodicity=1, last_checked=None)
        assert self.habit.timer.is_in_time() == 0
        # weeks
        self.habit.timer.initialize(start_date=self.two_weeks, timespan="weeks", periodicity=1, last_checked=None)
        assert self.habit.timer.is_in_time() == 0
        # months
        self.habit.timer.initialize(start_date=self.two_months, timespan="months", periodicity=1, last_checked=None)
        assert self.habit.timer.is_in_time() == 0

        # With last_checked
        # days
        self.habit.timer.initialize(start_date=self.two_days, timespan="days", periodicity=1,
                                    last_checked=self.two_days)
        assert self.habit.timer.is_in_time() == 0
        # weeks
        self.habit.timer.initialize(start_date=self.two_weeks, timespan="weeks", periodicity=1,
                                    last_checked=self.two_weeks)
        assert self.habit.timer.is_in_time() == 0
        # months
        self.habit.timer.initialize(start_date=self.two_months, timespan="months", periodicity=1,
                                    last_checked=self.two_months)
        assert self.habit.timer.is_in_time() == 0

        # Check if in the future works correctly
        # Therefor create start dates that are in the future
        self.future_day = self.now + pd.offsets.DateOffset(days=1)  # Offset 1 day in the future
        self.future_week = self.now + pd.offsets.DateOffset(weeks=1)  # Offset 1 day in the future
        self.future_month = self.now + pd.offsets.DateOffset(months=1)  # Offset 1 day in the future
        # With start_date
        # days
        self.habit.timer.initialize(start_date=self.future_day, timespan="days", periodicity=1, last_checked=None)
        assert self.habit.timer.is_in_time() == 2
        # weeks
        self.habit.timer.initialize(start_date=self.future_week, timespan="weeks", periodicity=1, last_checked=None)
        assert self.habit.timer.is_in_time() == 2
        # months
        self.habit.timer.initialize(start_date=self.future_month, timespan="months", periodicity=1, last_checked=None)
        assert self.habit.timer.is_in_time() == 2

        # With last_check
        # days
        self.habit.timer.initialize(start_date=self.last_day, timespan="days", periodicity=1,
                                    last_checked=self.future_day)
        assert self.habit.timer.is_in_time() == 2
        # weeks
        self.habit.timer.initialize(start_date=self.last_week, timespan="weeks", periodicity=1,
                                    last_checked=self.future_week)
        assert self.habit.timer.is_in_time() == 2
        # months
        self.habit.timer.initialize(start_date=self.last_month, timespan="months", periodicity=1,
                                    last_checked=self.future_month)
        assert self.habit.timer.is_in_time() == 2

    def teardown_method(self):
        self.habit.delete_habit()
        del self.habit
        del self


class TestAnalytics:

    def setup_method(self):
        # Create habits, so every calculation of the functions below is executed
        self.drinking = h.Habit("drinking")
        self.smoking = h.Habit("smoking")
        self.learning = h.Habit("learning")
        self.smoking.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="days", periodicity=1)
        self.drinking.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="days", periodicity=1)
        self.learning.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="weeks", periodicity=1)

    def test_same_periodicity(self):
        # Create a dataframe to compare to
        compare_frame = pd.DataFrame(data=[["smoking", "learning"], ["drinking", np.NaN]],
                                     columns=[('days', 1), ('weeks', 1)])
        # Compare both frames
        pd.testing.assert_frame_equal(analytics.same_periodicity(), compare_frame)

    def test_list_all_habits(self):
        # Check if habits were listed correctly
        assert analytics.list_all_habits() == ["drinking", "smoking", "learning"]

    def test_all_values_table(self):
        # Create dataframe to compare to
        compare_frame = pd.DataFrame(data=[[np.datetime64("2023-11-06"), None, "every 1 days", 0, 0, 0, 0, 0],
                                           [np.datetime64("2023-11-06"), None, "every 1 days", 0, 0, 0, 0, 0],
                                           [np.datetime64("2023-11-06"), None, "every 1 weeks", 0, 0, 0, 0, 0]],
                                     index=["drinking", "smoking", "learning"],
                                     columns=["Start date", "Last checked", "Periodicity", "Times checked",
                                              "Times failed", "Checked in %", "Longest streak", "Current counter"]
                                     )
        # Compare both frames
        pd.testing.assert_frame_equal(analytics.all_values_table(), compare_frame, check_dtype=False)

    def test_can_check_today(self):
        # Check if all habits are listed that are in time or in the past
        assert analytics.can_check_today() == ['drinking', 'smoking', 'learning']

    def test_sort_by_streak(self):
        # Set streak values
        self.drinking.streak = 1
        self.smoking.streak = 2
        self.learning.streak = 3

        # Create a frame to compare to
        compare_frame = pd.DataFrame(data=[1, 2, 3],
                                     index=["drinking", "smoking", "learning"],
                                     columns=["Longest streak"])

        # Compare both frames
        pd.testing.assert_frame_equal(analytics.sort_by_streak(), compare_frame, check_dtype=False)

    def test_sort_by_checked_ratio_positive(self):
        analytics.sort_by_checked_ratio_negative()
        pass

    def test_sort_by_checked_ratio_negative(self):
        analytics.sort_by_checked_ratio_positive()
        pass

    def teardown_method(self):
        self.drinking.delete_habit()
        self.smoking.delete_habit()
        self.learning.delete_habit()


class TestSQLFunctionalities:

    def setup_method(self):
        # Create habits, so every calculation of the functions below is executed
        self.drinking = h.Habit("drinking")
        self.smoking = h.Habit("smoking")
        self.learning = h.Habit("learning")
        self.smoking.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="days", periodicity=1)
        self.drinking.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="days", periodicity=1)
        self.learning.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="weeks", periodicity=1)

        # Create a database object
        self.database = SQL_functionalities.Database("pytest.db")

    def test_save_all_and_restore_all(self, monkeypatch):
        # Monkeypatch the "input" function, so that it returns "."
        monkeypatch.setattr('builtins.input', lambda: ".")
        self.database.save_all()

        # Monkeypatch the "input" function, so that it returns "."
        monkeypatch.setattr('builtins.input', lambda: ".")
        self.database.restore_all()

    def test_save_time_data(self, monkeypatch):

        # Monkeypatch the "input" function, so that it returns "."
        monkeypatch.setattr('builtins.input', lambda: ".")

        # Check habit to generate time data
        self.drinking.check_habit()
        self.smoking.check_habit()
        self.learning.check_habit()
        self.database.save_all()

    def test_close_connection(self):
        self.database.close_connection()

    def teardown_method(self):
        del self.drinking
        del self.smoking
        del self.learning
        self.database.con.close()
        path = pathlib.Path("pytest.db")
        path.unlink()


pytest.main()

cov.stop()
cov.save()
cov.html_report(directory='coverage_reports')
