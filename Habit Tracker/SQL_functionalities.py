import sqlite3
import traceback
import pandas as pd
import numpy as np
import class_habit as h


# Create the database class
class Database:

    def __init__(self, file_name: str = "Habits.db"):
        self.con = sqlite3.connect(file_name)       # Create a sql connection to 'file_name.db'
        self.cur = self.con.cursor()        # Create a cursor for the connection above

    def close_connection(self):
        """
        Close the database connection.
        :return:
        """
        self.cur.close()        # Close the cursor
        self.con.close()        # Close the connection

    def save_all(self):
        """
        Save all habits to database.
        :return:
        """
        # Delete existing table to replace it
        drop_habit_tables = """DROP TABLE IF EXISTS habits"""

        # Crete a new table (replace)
        create_habit_table = """CREATE TABLE IF NOT EXISTS habits (     
                                name PRIMARY KEY,
                                counter,
                                streak,
                                start_date,
                                timespan,
                                last_checked,
                                periodicity
                                )"""

        self.con.execute(drop_habit_tables)     # Execute delete
        self.con.execute(create_habit_table)    # Execute create

        # Insert values in habit table
        insert_habit_data = """INSERT INTO habits (
                                name,
                                counter,
                                streak,
                                start_date,
                                timespan,
                                last_checked,
                                periodicity)
                                
                                VALUES
                                
                                (?,?,?,?,?,?,?)
        """

        # Get all habit values and pass them to sql query
        for x in h.Habit.list:
            if h.Habit.list[x].timer.last_checked is None:      # last_checked can be none in some cases.
                last_checked = None                             # Check if its none before converting it into timestamp
            else:
                last_checked = pd.Timestamp.isoformat(pd.Timestamp(h.Habit.list[x].timer.last_checked))

            # Execute sql query with habit values
            self.con.execute(insert_habit_data, (
                h.Habit.list[x].name,
                h.Habit.list[x].counter,
                h.Habit.list[x].streak,
                pd.Timestamp.isoformat(pd.Timestamp(h.Habit.list[x].timer.start_date)),
                h.Habit.list[x].timer.timespan,
                last_checked,       # Last checked was set above
                h.Habit.list[x].timer.periodicity
            ))
            self.con.commit()

        # Save time_data series
        # Delete existing table to replace it
        drop_time_data_tables = """DROP TABLE IF EXISTS {}_time_data"""

        # Create new table
        create_time_data_table = """CREATE TABLE IF NOT EXISTS {}_time_data(
                                        dates PRIMARY KEY,
                                        value 
                                )"""

        # Insert values into table
        insert_time_data = """INSERT INTO {}_time_data 
                                (dates, value) 
                                VALUES
                                (?,?)
                            """

        # For every habit in habit list drop and create a table for time_data
        for x in h.Habit.list:
            self.cur.execute((drop_time_data_tables.format(x)))
            self.cur.execute((create_time_data_table.format(x)))

            # Get the time_data index and value by position
            for y in range(len(h.Habit.list[x].timer.time_data)):
                values = h.Habit.list[x].timer.time_data.iloc[y]
                dates = pd.Timestamp.isoformat(pd.Timestamp(h.Habit.list[x].timer.time_data.index[y]))

                # Insert time_data into database
                try:
                    self.cur.execute((insert_time_data.format(x)), (dates, values))
                except Exception as e:
                    print("Encountered an error while saving the data")
                    print(e)
                    traceback.print_exc()       # Trace back every possible exception
                    return
                self.con.commit()       # Commit changes to database
        print("Changes were saved correctly!")
        print("Press any key to go back.")
        input()

    def restore_all(self):
        """
        Restore all habits from database.
        :return:
        """
        name_list = []      # List for all habit names
        get_all_habit_names = """SELECT name FROM habits """        # Query to get all habit names from database

        # Fetch all habit names and save them in a list
        try:
            self.cur.execute(get_all_habit_names)
            temp_list = self.cur.fetchall()     # Temporary list for habit names
        except sqlite3.OperationalError:        # Catch Sql errors
            # Check if habit table is in database
            self.cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='habits'""")
            if self.cur.fetchone() is None:
                print("Database seems empty")
                print("Press any key to go back.")
                input()
            return

        # Sql query return values as tuple like (value,.)
        # Convert temp_list tuples into single values and save them in name_list
        for x in range(len(temp_list)):
            name_list.append(temp_list[x][0])

        # Setup habit dictionary with names as keys
        for x in name_list:
            h.Habit.list[x] = None

        # Create the habits from the Database and fill in values
        for x in name_list:
            h.Habit.list[x] = h.Habit(x)

            # Get the time data back
            try:
                time_data_index = [time_data_index[0] for time_data_index in
                                   self.cur.execute("""SELECT dates FROM {}_time_data""".format(x))]

                time_data_value = [time_data_value[0] for time_data_value in
                                   self.cur.execute("""SELECT value FROM {}_time_data""".format(x))]

                h.Habit.list[x].timer.time_data = pd.Series(time_data_value, index=time_data_index)

            # If time_data doesn't exist
            except sqlite3.OperationalError:
                traceback.print_exc()

            # Get all other values back
            try:
                self.cur.execute("""SELECT counter FROM habits WHERE name = '{}'""".format(x))
                h.Habit.list[x].counter = self.cur.fetchone()[0]        # [0] index because value is a tuple

                self.cur.execute("""SELECT streak FROM habits WHERE name = '{}'""".format(x))
                h.Habit.list[x].streak = self.cur.fetchone()[0]     # [0] index because value is a tuple

                self.cur.execute("""SELECT start_date FROM habits WHERE name = '{}'""".format(x))
                start_date = np.datetime64(self.cur.fetchone()[0], "D")     # [0] index because value is a tuple

                self.cur.execute("""SELECT timespan FROM habits WHERE name = '{}'""".format(x))
                timespan = self.cur.fetchone()[0]       # [0] index because value is a tuple

                self.cur.execute("""SELECT last_checked FROM habits WHERE name = '{}'""".format(x))
                last_checked = np.datetime64(self.cur.fetchone()[0], "D")    # [0] index because value is a tuple

                if pd.isnull(last_checked):     # If last_checked was saved as None trying to convert it to datetime64
                    last_checked = None         # yields NaT. This will lead to problems later on, so convert it

                self.cur.execute("""SELECT periodicity FROM habits WHERE name = '{}'""".format(x))
                periodicity = self.cur.fetchone()[0]        # # [0] index because value is a tuple

                # Pass all previously gathered data to timer.initialize function
                h.Habit.list[x].timer.initialize(start_date, timespan, periodicity, last_checked)

            # Catch all exception and trace back
            except Exception as e:
                print("Encountered an error while restoring the data.")
                print(e)
                traceback.print_exc()
                return

        print("Data was restored correctly.")
        print("Press any key to go continue.")
        input()
