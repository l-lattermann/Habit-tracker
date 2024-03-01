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
Clone the directory from GitHub using the Git Bash.
Therefor navigate to directory you want to clone the project at and enter:
````cmd
git clone https://github.com/l-lattermann/Habit-tracker.git
````
### Virtual environment venv
It is recommended to install into a virtual environment to avoid package conflicts in your Python installation.
### Create a venv
In the Habit-tracker-project folder run:
#### Windows:
````cmd
.venv\Scripts\activate
````
#### MacOS:
````cmd
source .venv/bin/activate
````
### Activate venv
In the Habit-tracker-project folder run:
#### Windows:
````cmd
py -m venv .venv
````
#### MacOS:
````cmd
python3 -m venv .venv
````

### Install the project into the venv
To install the project from the project root directory run:
#### Windows:
````cmd
py -m pip install .
````

#### MacOS:
````cmd
python3 -m pip install .
````
# Usage
To start the program just run habit_tracker and the start menu will lead you through the application.

#### Windows
```cmd
py haibit_tracker
```
#### MacOS
```cmd
python3 haibit_tracker
```
### 1. Select start mode
* Load from save data
* Load test data

### 2 Main menu
* Create new habit
* Check habits
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
There is a Pytest test suit included in this project. It will open a coverage report in your browser automatically

Run:
```shell
pytest
```
to start the test.