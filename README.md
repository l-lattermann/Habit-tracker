# Habit tracker
A university project for the course "Object-Oriented and Functional Programming with Python".
Built in Python 3.12

## What is it?
Habit tracker is a basic program with a command line interface where you can keep track of habits you want to implement
in your life.
You can create new habits, set time ranges in which you want to check off those habits. The application keeps track of all those habits
and calculates a variety of statistics about those habits like streaks, and a time series when the habit was
broken or checked.

# Installation
Make sure to install [Python 3.7](https://www.python.org/downloads/) or later.

Install requirements.txt to get all the python modules needed for running this application.
````shell
pip install -r requirements.txt
````

# Usage
To start the program just run the main.py and the start menu will lead you through the application.
```shell
python main.py
```
### 1. Select start mode
* Load from save data
* Load test data

### 2 Main menu
* Create new habit
* Check habits
* Load habits
* Import habits
* Show current habits
* Get habit statistics
  * Longest streak
  * Went well
  * Went poorly
  * Show time data
  * All stats table
  * Go back
* Delete habits
  * Delete one habit 
  * Delete all habits
* Exit the program 



# Testing
There is a Pytest test suit included in this project. 

Run:
```shell
python project_test.py
```
to start the test.