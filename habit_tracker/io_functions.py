import numpy as np
import datetime
import questionary
import os
import traceback

from habit_tracker import (class_habit as h,
                           analytics,
                           SQL_functionalities)


header = "\n" \
         "***********************************************************************************\n" \
         "*                                   HABIT TRACKER                                 *\n" \
         "***********************************************************************************"


def start_up() -> bool:
    """
    Shows start screen and start mode selection. Returns True if test mode is selected.
    :return: bool
    """
    # Intro message for habit tracker
    intro_message = "***************************************************\n" \
                    "*            Welcome to Habit-tracker-project!            *\n" \
                    "*            Life is your choice...               *\n"\
                    "*            Please select start mode!            *\n"\
                    "***************************************************"

    # Clear screen an print header
    os.system("cls")
    print(intro_message)

    # Select start mode
    start = questionary.select(
        "Please select start mode: ", choices=[
            "Normal - load save data and begin",
            "Test mode - load test data and explore the app"
        ]).ask()

    if start == "Normal - load save data and begin":
        restore_all_from_database("habit_tracker/data/habits.db")      # Load save data for mode normal
        return False

    elif start == "Test mode - load test data and explore the app":
        restore_all_from_database("habit_tracker/data/test_data.db")      # Load test data for mode test
        return True


def save_all_to_database(save_file: str):
    """
    Saves everything to database 'save_file'
    :param save_file: File name for .db file
    :return:
    """

    try:
        database = SQL_functionalities.Database(save_file)      # Create database object
        try:
            database.save_all()
            database.close_connection()

        except Exception as e:      # Catch all exceptions from save function and trace back
            print(e)
            traceback.print_exc()
            print("Saving to database failed")
            print("Press any key to go back")
            input()

    except Exception as e:      # Catch all exceptions from database class and trace back
        print(e)
        traceback.print_exc()
        print("Database connection failed!")
        print("Press any key to go back")
        input()


def create_new_habit(save_file: str):
    """
    Let user create a new habit.
    :param save_file: File name for .db file
    :return:
    """

    while True:     # Loop breaks when habit was created successfully

        # Variable to pass to initialize_timer function later on
        start_date = None
        periodicity = None
        timespan = None

        # Set name for habit
        print("Creating habit...\n")
        while True:     # Loop breaks when name was entered correctly
            print("Enter habit name. Must contain at least one character and can only be 15 characters long")
            in_name = input()
            if in_name and not in_name.isspace() and len(in_name) < 16:     # Check if name length is ok and not empty
                if in_name not in h.Habit.list:     # Check if name already exists
                    h.Habit(in_name)
                    name = in_name
                    break
                else:
                    print("Name already exists!")
                    pass

        # Set timespan for habit
        timespan_q = questionary.select(
            f"Which timespan you want to check the habit {name} in?", choices=[
                "Daily",
                "Weekly",
                "Monthly"
            ]).ask()
        if timespan_q == "Daily":
            timespan = "days"

        elif timespan_q == "Weekly":
            timespan = "weeks"

        elif timespan_q == "Monthly":
            timespan = "months"

        # Set periodicity for habit
        periodicity_q = questionary.select(
            f"In which period you want to check the habit {name}?", choices=[
                "Every 1 " + str(timespan),
                "Every 2 " + str(timespan),
                "Every 3 " + str(timespan),
                "Set custom periodicity"
            ]).ask()

        if periodicity_q == "Every 1 " + str(timespan):
            periodicity = 1

        elif periodicity_q == "Every 2 " + str(timespan):
            periodicity = 2

        elif periodicity_q == "Every 3 " + str(timespan):
            periodicity = 3

        elif periodicity_q == "Set custom periodicity":
            while True:     # Loop breaks when periodicity was entered correctly
                print("Enter periodicity. Must be an integer number between 1 and 30")
                number = input()
                try:
                    number = int(number)    # Check if number is int type
                    if 1 <= number <= 30:    # Check if number is between 1 and 30
                        periodicity = number
                        break
                    else:
                        print("Number to big!")

                except ValueError:
                    print("Try again with only numbers!\n")

        # Set start date for habit
        start_date_q = questionary.select(
            f"When do you want to start the habit {name}?", choices=[
                "Today",
                "Set custom start date"
            ]).ask()

        if start_date_q == "Today":
            start_date = np.datetime64("now", "D")

        elif start_date_q == "Set custom start date":
            while True:     # Loop breaks when start date was entered correctly
                print("Enter custom start date as YYYY-MM-DD")
                date = input()
                form = "%Y-%m-%d"  # String format for comparison
                try:
                    datetime.strptime(date, form)   # Check if string can be converted into datetime
                    start_date = np.datetime64(date, "D")   # If yes, set it as start date
                    break
                except ValueError:
                    print("Incorrect date format!")

        # Check if all values were set
        if (timespan is None) or (periodicity is None) or (start_date is None):
            print("Sorry, problem occurred. Please start again setting up the habit! \n")
            print("Press any key to go back")
            input()
        else:
            # Try to initialize the habit timer
            try:
                h.Habit.list[name].timer.initialize(start_date, timespan, periodicity)
                print("Habit was successfully created!")
                save_all_to_database(save_file)
                break

            except Exception as e:
                print("There was a problem initializing the habit!")
                print(e)
                traceback.print_exc()
                print("Press any key to try again.")
                input()


def restore_all_from_database(save_file: str):
    """
    Restore habit data from database 'filename'
    :param save_file: File name for .db file
    :return:
    """
    # Try to create a database connection
    try:
        database = SQL_functionalities.Database(save_file)
        try:
            database.restore_all()
            database.close_connection()

        except Exception as e:  # If an error occurs during restoring
            print(e)
            traceback.print_exc()
            print("restoring failed")

    except Exception as e:  # If for any reason DB connection cannot be created
        print(e)
        traceback.print_exc()
        print("Database connection failed!")

    print("Habits were successfully restored!")


def show_current_habits():
    """
    Shows currently tracked habits.
    :return:
    """
    # If no habits were created yet
    if not analytics.list_all_habits():
        print("\nThere are no habits yet!\nPress any key to go back.")
        input()
    else:
        for x in analytics.list_all_habits():   # Print all habits
            print(x)
        print("Press any key to go back.")
        input()


def import_habits_from_database():
    """
    Loads data from database. The user can specify a file in the process.
    :return:
    """
    print("You can only load .db files. The files must be located in the same directory as\n"
          "the habit tracker __main__.py\n\n")
    while True:
        print("Please enter the filename as {'filename'.db}")

        file_name = input()

        # Create path to running directory
        path = "./" + file_name

        # Check if file exists
        file_exists = os.path.isfile(path)
        if file_exists:
            restore_all_from_database(file_name)
            break
        else:
            print("File not found!")
            try_again = questionary.select(
                "Do you want to try again??", choices=[
                    "Yes",
                    "No"
                ]).ask()

            if try_again == "Yes":
                pass
            if try_again == "No":
                break


def check_habits(save_file: str):
    """
    Let user select habits that are check able from a list and checks them.

    :param save_file: File name for .db file
    :return:
    """
    while True:     # Breaks either by input or when there are no habits to check
        os.system("cls")    # Clear screen and print header
        print(header)

        # Check if there are habits to check today
        can_check = analytics.can_check_today()
        if not can_check:
            print("There are no habits you can check today.")
            print("Press any key to go back")
            input()
            break

        else:
            can_check.append("Go back")     # Add a go back option to the list
            habit = questionary.select(
                "You can check the following habits today. Which one would you like to check now?",
                choices=can_check).ask()

            if habit == "Go back":
                break
            else:
                can_check.remove("Go back")     # Remove "Go back" to avoid using it as habit list index
                for x in can_check:
                    if habit == x:
                        res = h.Habit.list[x].check_habit()
                        if res == 0:
                            print("Habit was broken!")

                        elif res == 1:
                            print("Habit was checked successfully!")
                save_all_to_database(save_file)


def all_stats_table():
    """
    Prints a table containing all data from all habits.
    :return:
    """
    # Create a stats table and check if empty
    table = analytics.all_values_table()
    if table.empty:
        print("\nThere are no habits yet!\n ")
    else:
        print(table.to_string())        # Print the stats table completely
    print("Press any key to go back.")
    input()


def delete_all_habits(save_file: str):
    """
    Deletes all habits in memory and in database.
    :return:
    """
    h.Habit.list.clear()        # Clear all members from Habit list
    print("All habits have been successfully deleted!")
    save_all_to_database(save_file)     # Save the changes


def longest_streak():
    """
    Prints a descending list of all streaks.
    :return:
    """
    # Print habits sorted by streak
    print(analytics.sort_by_streak())
    print("Press any key to go back.")
    input()


def went_well():
    """
    Prints a descending list of check/fail ratio ind %.
    :return:
    """
    # Print habits sorted by checked/failed ratio in % descending
    print(analytics.sort_by_checked_ratio_positive())
    print("Press any key to go back.")
    input()


def went_poorly():
    """
    Prints an ascending list of check/failed ratio in %.
    :return:
    """
    # Print habits sorted by checked/failed ratio in % ascending
    print(analytics.sort_by_checked_ratio_negative())
    print("Press any key to go back.")
    input()


def show_time_data():
    while True:     # Loop breaks by user input
        os.system("cls")   # Clear screen
        print(header)      # Print header

        # Create a list of habits, check if empty
        can_show = analytics.list_all_habits()
        if not can_show:
            print("There are no habits yet.")
            break

        else:
            can_show.append("Go back")      # Append "Go back" option
            habit = questionary.select(
                "Which time data would you like to see?",
                choices=can_show).ask()

            if habit == "Go back":
                break
            else:
                can_show.remove("Go back")  # Remove "Go back" to avoid using it as habit list index
                for x in can_show:
                    if habit == x:
                        print("Time data for {}:".format(x))    # Insert habit names into string
                        print(h.Habit.list[x].timer.time_data.to_string())    # Print complete time series
                        print("Press any key to go back.")
                        input()


def delete_one_habit(save_file: str):
    """
    Prints a list of all habits from which the habit to delete can be selected.
    :param save_file: File name for .db file
    :return:
    """

    # Create a habit list and check if empty
    menu_list = analytics.list_all_habits()
    if not menu_list:
        print("There are no habits yet.")
        print("Press any key to go back.")
        input()
    else:
        menu_list.append("Go back")     # Append "Go back" option to menu
        del_menu_2 = questionary.select(
            "Which one would you like to delete?", choices=menu_list
        ).ask()

        if menu_list == "Go back":
            pass
        else:
            menu_list.remove("Go back")     # Remove "Go back" to avoid using it as habit list index
            for x in menu_list:
                if del_menu_2 == x:
                    h.Habit.list[x].delete_habit()
                    print("Habit was successfully deleted!")
                    save_all_to_database(save_file)


def same_periodicity():
    """
    Print a table with all (periodicity, timespan) tuples as columns and habits as values.
    :return:
    """
    print(analytics.same_periodicity())
    print("Press any key to go back")
    input()


def display_help():
    """
    Displays a user tutorial for the habit tracker.
    :return:
    """
    os.system("cls")
    print(header)
    print("\n"
          "                           -----------------------------                          \n"
          "                           How to use the habit tracker:                          \n"
          "                           -----------------------------                          \n\n"
          "* Create a new habit:\n"
          "  Just navigate to 'create habit' and follow the process. When you create a habit\n"
          "  with start date today you have to check it today the first time. When you crea-\n"
          "  te a habit on day x you have to check it on day x the first time.\n"
          "  When you set the timespan to days you can check the habit in the next period at\n"
          "  any time during that day. If you set the timespan to weeks you can check the \n"
          "  habit in the next period at any time during that week, and so on.\n"
          "  When you miss to check a habit during the chosen period you break the habit\n\n"
          "* Check a habit:\n"
          "  To check a habit just navigate to 'Check habit'. You can select now which one  \n"
          "  you want to check. It shows only habits that can be checked today\n\n"
          "* Import habits:\n"
          "  Just navigate to 'Import habits'. There you can enter the file name from which\n"
          "  you want to load the habit data from. File names must include the .db suffix.\n"
          "  Only Sqlite files are supported\n\n"
          "* Show currently tracked habits:\n"
          "  Just select 'Show current habits'\n\n"
          "* Get all sorts of useful information about current habits:\n"
          "  Navigate to 'Get habit statistics'. There you can select between different stats\n"
          "  you want to see.\n\n"
          "* Delete habits:\n"
          "  Navigate to 'Delete habits'. You can select between 'delete one' and \n"
          "  'delete all' there.\n\n\n\n"
          "Press any key to go back")
    input()
