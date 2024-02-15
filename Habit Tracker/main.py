import io_functions as io
import questionary
import os

# PROGRAM STARTS AND INTRO MESSAGE INTRODUCES THE APP.
test_mode = io.start_up()

# Change the save file in test mode to test.db so test data does not overwrite the current save data
if test_mode:
    save_file = "data/test_save.db"
else:
    save_file = "data/habits.db"


# Application header
header = "\n" \
         "***********************************************************************************\n" \
         "*                                   HABIT TRACKER                                 *\n" \
         "***********************************************************************************"
# Main menu
# Comments in the main menu were left out for improving visibility. The choices can be read as comments
# Questionary.select presents a list of choices which can be selected by the user using arrow keys
# The selected choice is then assigned to the variable
# if statements then checks the variable content
while True:
    os.system("cls")
    print(header)
    menu = questionary.select(
        "What do you want to do?", choices=[
            "Create new habit",
            "Check habits",
            "Import habits",
            "Show current habits",
            "Get habit statistics",
            "Delete habits",
            "Help",
            "Exit the program"
        ]).ask()

    if menu == "Create new habit":
        io.create_new_habit(save_file)

    if menu == "Check habits":
        io.check_habits(save_file)

    if menu == "Import habits":
        io.import_habits_from_database()

    if menu == "Delete habits":
        while True:
            os.system('cls')
            print(header)
            del_menu = questionary.select(
                "Habit statistics", choices=[
                    "Delete one habit",
                    "Delete all habits",
                    "Go back"
                ]).ask()

            if del_menu == "Delete one habit":
                io.delete_one_habit(save_file)

            elif del_menu == "Delete all habits":
                io.delete_all_habits(save_file)

            elif del_menu == "Go back":
                break

    if menu == "Show current habits":
        io.show_current_habits()

    if menu == "Get habit statistics":
        while True:
            os.system('cls')
            print(header)
            stat_menu = questionary.select(
                "Habit statistics", choices=[
                    "Longest streak",
                    "Same periodicity",
                    "Went well",
                    "Went poorly",
                    "Show time data",
                    "All stats table",
                    "Go back"
                ]).ask()

            if stat_menu == "Longest streak":
                io.longest_streak()
            elif stat_menu == "Same periodicity":
                io.same_periodicity()
            elif stat_menu == "Went well":
                io.went_well()
            elif stat_menu == "Went poorly":
                io.went_poorly()
            elif stat_menu == "Show time data":
                io.show_time_data()
            elif stat_menu == "All stats table":
                io.all_stats_table()
            elif stat_menu == "Go back":
                break

    if menu == "Help":
        io.display_help()

    if menu == "Exit the program":
        sure = questionary.select(
            "Are your sure?", choices=[
                "No",
                "Yes"
            ]).ask()

        if sure == "No":
            pass
        elif sure == "Yes":
            break
