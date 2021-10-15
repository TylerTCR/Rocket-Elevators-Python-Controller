class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.status = "off"
        self.floor = _floor
        self.direction = _direction
# End Call Button Class

class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status = "off"
        self.floor = _floor
# End Floor Request Button Class

class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = "closed"
# End Door Class

class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.amountOfFloors = _amountOfFloors
        self.status = "idle"
        self.currentFloor = 1
        self.direction = ""
        self.door = Door(_id)
        self.floorRequestList = []
        self.floorRequestButtonList = []

        self.createFloorRequestButtons(self.amountOfFloors)

    def createFloorRequestButtons(self, _amountOfFloors):
        i = 0
        buttonFloor = 1
        buttonId = 1

        while i < _amountOfFloors:
            floorRequestButton = FloorRequestButton(buttonId, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor += 1
            buttonId += 1
            i += 1

    ## Executes when floor request button is pressed
    # - Add the floor request to the list
    # - Move elevator to requested floor
    def requestFloor(self, requestedFloor):
        self.floorRequestList.append(requestedFloor)
        self.move()

    def move(self):
        element = 0

        while len(self.floorRequestList) != 0:
            for element in self.floorRequestList:
                if self.currentFloor < element:
                    self.direction = "up"
                    self.sortFloorList()
                    if self.door.status == "opened":
                        self.door.status = "closed"
                    self.status = "moving"

                    # Move the elevator up until it gets to requested floor
                    while self.currentFloor < element:
                        self.currentFloor += 1
                    
                    self.status = "stopped"
                    self.door.status = "opened"
                    self.door.status = "closed"
                # If the elevator's current floor is higher than the requested floor
                elif self.currentFloor > element:
                    self.direction = "down"
                    self.sortFloorList()
                    if self.door.status == "opened":
                        self.door.status = "closed"
                    self.status = "moving"

                    # Move the elevator down until it gets to requested floor
                    while self.currentFloor > element:
                        self.currentFloor -= 1
                    
                    self.status = "stopped"
                    self.door.status = "opened"
                    self.door.status = "closed"
                # End if
                # Remove the floor since it's been reached
                self.floorRequestList.pop(0)
            # End for loop
        # End outer-while
        self.status = "idle"
    # End move()

    def sortFloorList(self):
        self.floorRequestList.sort() if self.floorRequestList == "up" else self.floorRequestList.sort(reverse=True)
# End Elevator Class

class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id 
        self.status = "online"
        self.numOfFloors = _amountOfFloors
        self.numOfElevators = _amountOfElevators
        self.elevatorList = []
        self.callButtonList = []

        self.fillElevatorList(self.numOfElevators, self.numOfFloors)
        self.fillCallButtonList(self.numOfFloors)
    
    def fillElevatorList(self, numOfElevators, numOfFloors):
        eleId = 1
        i = 0
        while i < numOfElevators:
            elevator = Elevator(eleId, numOfFloors)
            self.elevatorList.append(elevator)
            eleId += 1
            i += 1
    
    def fillCallButtonList(self, numOfFloors):
        buttonId = 1
        floor = 1
        i = 0

        while i < numOfFloors:
            if floor == 1:
                self.callButtonList.append(CallButton(buttonId, floor, "up"))
            elif floor < numOfFloors and floor != 1:
                self.callButtonList.append(CallButton(buttonId, floor, "up"))
                buttonId += 1
                self.callButtonList.append(CallButton(buttonId, floor, "down"))
            else:
                self.callButtonList.append(CallButton(buttonId, floor, "down"))
            buttonId += 1
            floor += 1
            i += 1
    
    ## Executes when a call button is pressed
    # - Find the best elevator
    # - Move that elevator
    # - Open doors
    # Returns the chosen elevator
    def requestElevator(self, requestedFloor, direction):
        chosenElevator = self.findBestElevator(requestedFloor, direction)
        chosenElevator.floorRequestList.append(requestedFloor)
        chosenElevator.move()
        chosenElevator.door.status = "opened"
        return chosenElevator

    # Find the best elevator to use
    def findBestElevator(self, requestedFloor, requestedDirection):
        bestElevator = None
        bestScore = 100
        referenceGap = 10000
        bestElevatorInformation = ""

        # For every element in the column's elevator list
        for elev in self.elevatorList:
            # Elevator is currently at the floor requested, it's stopped, and going in the direction requested
            if requestedFloor == elev.currentFloor and elev.status == "stopped" and requestedDirection == elev.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(1, elev, bestScore, referenceGap, bestElevator, requestedFloor)
            # Elevator is currently higher than the floor requested, it's going down, the user wants to go down
            elif elev.currentFloor > requestedFloor and elev.direction == "down" and requestedDirection == elev.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(2, elev, bestScore, referenceGap, bestElevator, requestedFloor)
            # Elevator is currently lower than the floor requested, it's going up, the user wants to go up
            elif elev.currentFloor < requestedFloor and elev.direction == "up" and requestedDirection == elev.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(2, elev, bestScore, referenceGap, bestElevator, requestedFloor)
            # Elevator is idle
            elif elev.status == "idle":
                bestElevatorInformation = self.checkIfElevatorIsBetter(3, elev, bestScore, referenceGap, bestElevator, requestedFloor)
            # No other elevator currently available
            else:
                bestElevatorInformation = self.checkIfElevatorIsBetter(4, elev, bestScore, referenceGap, bestElevator, requestedFloor)
            
            bestElevator = bestElevatorInformation["bestElevator"]
            bestScore = bestElevatorInformation["bestScore"]
            referenceGap = bestElevatorInformation["referenceGap"]
        # End loop
        
        print("Best Elevtor")
        print(bestElevator)
        return bestElevator
    
    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = abs(newElevator.currentFloor - floor)
        elif bestScore == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if referenceGap > gap:
                bestElevator = newElevator
                referenceGap = gap
        
        return {
            "bestElevator": bestElevator,
            "bestScore": bestScore,
            "referenceGap": referenceGap
        }
# End Column Class