import numpy as np
import pandas as pd

from habit_tracker import class_habit as h

def same_periodicity():
    """
    Returns a data frame with columns as tuples of (periodicity, timespan).
    :return: pandas.Dataframe
    """
    # Create a series for all tuples
    period_list = pd.Series()

    # Create a list from all habits where the name is the index
    # and the value is a tuple of ('timespan', 'periodicity').
    # I.e.: habit_name : ('daily', 1)
    for x in h.Habit.list:
        period_list[x] = (h.Habit.list[x].timer.timespan,
                          h.Habit.list[x].timer.periodicity)

    period_list.drop_duplicates()       # drop the duplicates in period list

    # Set up a dataframe with all ('timespan', 'periodicity') tuples as columns
    # and the corresponding habits as values
    same_period_frame = pd.DataFrame()
    for x in period_list:
        indices_of_value = np.array(period_list.loc[period_list == x].index)
        same_period_frame[x] = pd.Series(indices_of_value)

    return same_period_frame


def list_all_habits():
    """
    Returns a list of all currently tracked habits
    :return: list
    """
    # Create a list for all habits
    habit_list = []
    for x in h.Habit.list:
        habit_list.append(x)        # fill the list from habit_list dictionary

    return habit_list


def all_values_table():
    """
    Creates a Pandas dataframe with all available stats about all habits.
    :return: pandas.Dataframe
    """
    # List of all needed columns
    column_list = ["Start date", "Last checked", "Periodicity", "Times checked",
                   "Times failed", "Checked in %", "Longest streak", "Current counter"]

    # Create an empty dataframe with the column list and habit names
    all_values_frame = pd.DataFrame(index=h.Habit.list, columns=column_list)

    # Insert data into dataframe
    for x in h.Habit.list:
        all_values_frame["Start date"][x] = h.Habit.list[x].timer.start_date        # Insert start date
        all_values_frame["Last checked"][x] = h.Habit.list[x].timer.last_checked    # Insert last checked
        all_values_frame["Periodicity"][x] = ("every " + str(h.Habit.list[x].timer.periodicity) + " " +
                                              str(h.Habit.list[x].timer.timespan))  # Insert periodicity
        try:
            # Count "checked" in time_data and insert
            all_values_frame["Times checked"][x] = h.Habit.list[x].timer.time_data.value_counts()["checked"]
        except KeyError:
            # If time_data empty
            all_values_frame["Times checked"][x] = 0

        try:
            # Count "failed" in time_data and insert
            all_values_frame["Times failed"][x] = h.Habit.list[x].timer.time_data.value_counts()["failed"]
        except KeyError:
            # If time_data is empty
            all_values_frame["Times failed"][x] = 0

        # Calculate and insert checked/(checked+failed)
        try:
            # Will throw error if failed count is zero
            failed_count = h.Habit.list[x].timer.time_data.value_counts()["failed"]
        except KeyError:
            failed_count = 0    # If zero, set zero
        try:
            # Will throw error if checked count is zero
            checked_count = h.Habit.list[x].timer.time_data.value_counts()["checked"]
        except KeyError:
            checked_count = 0   # If zero, set zero

        try:
            # Expression throws error if time_data is empty because 0/(0+0)
            all_values_frame["Checked in %"][x] = ((checked_count/(failed_count+checked_count)) * 100).__round__()
        except ZeroDivisionError:
            all_values_frame["Checked in %"][x] = 0     # If empty, set zero

        all_values_frame["Longest streak"][x] = h.Habit.list[x].streak      # Insert longest streak
        all_values_frame["Current counter"][x] = h.Habit.list[x].counter    # Insert counter

    return all_values_frame


def can_check_today():
    """
    Returns a list of all habits that can be checked today
    :return: list
    """
    # Create a list for all habits that can be checked
    check_today_list = []

    # Fill the list with habits
    for x in h.Habit.list:
        if h.Habit.list[x].timer.is_in_time() == 1:     # Append if habit is in time
            check_today_list.append(x)
        if h.Habit.list[x].timer.is_in_time() == 0:     # Append if habit is too late
            check_today_list.append(x)

    return check_today_list


def sort_by_streak():
    """
    Returns a Series of all habits sorted by longest streak.
    :return: pandas.Series
    """
    data_frame = all_values_table()[["Longest streak"]]     # Column Longest streak into Series
    return data_frame.sort_values(by="Longest streak")      # Return Series sorted by longest streak


def sort_by_checked_ratio_positive():
    """
    Returns a Series of all habits sorted by "checked in %" descending.
    :return:  pandas.Series
    """
    data_frame = all_values_table()[["Checked in %"]]       # Create a Series from column Checked in %
    return data_frame.sort_values(by="Checked in %", ascending=False)       # Return sorted descending


def sort_by_checked_ratio_negative():
    """
    Returns a Series of all habits sorted by "checked in %" ascending.
    :return:  pandas.Series
    """
    data_frame = all_values_table()[["Checked in %"]]       # Create a Series from column Checked in %
    return data_frame.sort_values(by="Checked in %", ascending=True)        # Return sorted descending
