# Rocket-Elevators-Python-Controller
This is Tyler's Rocket Elevators' Residential Controller coded in Python.

A brief run-down on how the controller works; First, the user calls the elevator and will pick the best elevator to send. Once picked, it will come to the user and allow them to get in and choose the floor they want to go to. When a floor is chosen, it will add the floor they picked to a floor request list for that specific elevator. Finally, the elevator will take them to that floor.

### Running the tests

To test this controller with scenarios, simply run the following command:

`python -m pytest`

To get more details about the test, simply add `-v` at the end like so:

`python -m pytest -v`