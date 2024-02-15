import random
import SQL_functionalities
import numpy as np
import pandas as pd
import analytics
import class_habit


smoking = class_habit.Habit("smoking")
drinking = class_habit.Habit("drinking")
reading = class_habit.Habit("reading")
running = class_habit.Habit("running")
sleeping = class_habit.Habit("sleeping")

smoking.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="days", periodicity=1)
drinking.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="days", periodicity=2)
reading.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="weeks", periodicity=1)
running.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="weeks", periodicity=2)
sleeping.timer.initialize(start_date=np.datetime64("2023-11-06"), timespan="months", periodicity=1)

smoking.timer.time_data = pd.Series(index=pd.date_range("2023-11-06", "2023-12-03", freq="1D"), data=str)
drinking.timer.time_data = pd.Series(index=pd.date_range("2023-11-06", "2023-12-03", freq="2D"), data=str)
reading.timer.time_data = pd.Series(index=pd.date_range("2023-11-06", "2023-12-03", freq="1W"), data=str)
running.timer.time_data = pd.Series(index=pd.date_range("2023-11-06", "2023-12-03", freq="2W"), data=str)
sleeping.timer.time_data = pd.Series(index=pd.date_range("2023-11-06", "2023-12-03", freq="1M"), data=str)

smoking.timer.last_checked = np.datetime64("2023-12-03")
drinking.timer.last_checked = np.datetime64("2023-12-03")
reading.timer.last_checked = np.datetime64("2023-12-03")
running.timer.last_checked = np.datetime64("2023-12-03")
sleeping.timer.last_checked = np.datetime64("2023-12-03")

for x in smoking.timer.time_data.index:
    smoking.timer.time_data[x] = random.choice(["checked", "failed", "checked","checked"])
for x in drinking.timer.time_data.index:
    drinking.timer.time_data[x] = random.choice(["checked", "failed", "checked","checked"])
for x in reading.timer.time_data.index:
    reading.timer.time_data[x] = random.choice(["checked", "failed", "checked","checked"])
for x in running.timer.time_data.index:
    running.timer.time_data[x] = random.choice(["checked", "failed", "checked","checked"])
for x in sleeping.timer.time_data.index:
    sleeping.timer.time_data[x] = random.choice(["checked", "failed", "checked","checked"])


for x in smoking.timer.time_data:
    if x == "checked":
        smoking.counter += 1
        if smoking.counter > smoking.streak:
            smoking.streak = smoking.counter
    elif x == "failed":
        smoking.counter = 0
for x in drinking.timer.time_data:
    if x == "checked":
        drinking.counter += 1
        if drinking.counter > drinking.streak:
            drinking.streak = drinking.counter
    elif x == "failed":
        drinking.counter = 0
for x in reading .timer.time_data:
    if x == "checked":
        reading.counter += 1
        if reading.counter > reading.streak:
            reading.streak = reading.counter
    elif x == "failed":
        reading.counter = 0
for x in running.timer.time_data:
    if x == "checked":
        running.counter += 1
        if running.counter > running.streak:
            running.streak = running.counter
    elif x == "failed":
        running.counter = 0
for x in sleeping.timer.time_data:
    if x == "checked":
        sleeping.counter += 1
        if sleeping.counter > sleeping.streak:
            sleeping.streak = sleeping.counter
    elif x == "failed":
        sleeping.counter = 0

smoking.timer.last_checked = np.datetime64("2023-12-03")
drinking.timer.last_checked = np.datetime64("2023-12-03")
reading.timer.last_checked = np.datetime64("2023-12-03")
running.timer.last_checked = np.datetime64("2023-12-03")
sleeping.timer.last_checked = np.datetime64("2023-12-03")


print(analytics.all_values_table().to_string())

db = SQL_functionalities.Database("test_data.db")
db.save_all()
db.close_connection()
