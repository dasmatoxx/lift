from modules import *


def get_desired_floor(floors_amount, current_floor):

    floors = [i for i in range(1, floors_amount)]
    possible_floors = list(filter(lambda x: x != current_floor, floors))
    desired_floor = randint(possible_floors[0], possible_floors[-1])
    return desired_floor


def passed_passengers(passengers, elevator):

    passed = []
    for passenger in passengers:
        if passenger.desired_floor <= elevator.position:
            passed.append(passenger)

    return passed


def come_inside_elevator(passed, passengers, elevator):

    elev_passengers = elevator.get_passengers()
    if elev_passengers is None:
        elev_passengers = []

    for passenger in passengers:
        if elevator.get_direction():

            # if elevator goes up
            if passenger.desired_floor <= elevator.max_floor and len(elev_passengers) < 5:
                if passenger not in elev_passengers and passenger not in passed:
                    elev_passengers.append(passenger)

            elif passenger.desired_floor > elevator.max_floor and len(elev_passengers) < 5:
                elevator.max_floor = passenger.desired_floor
                if passenger not in elev_passengers and passenger not in passed:
                    elev_passengers.append(passenger)

        else:
            # else elevator goes down
            if passenger.desired_floor >= elevator.max_floor and len(elev_passengers) < 5:
                if passenger not in elev_passengers and passenger.desired_floor > elevator.position:
                    elev_passengers.append(passenger)

            elif passenger.desired_floor < elevator.max_floor and len(elev_passengers) < 5:
                elevator.max_floor = passenger.desired_floor
                if passenger not in elev_passengers and passenger.desired_floor > elevator.position:
                    elev_passengers.append(passenger)

    elevator.set_passengers(elev_passengers)


def exit_from_elevator(desired_floor, elevator):

    elev_passengers = elevator.get_passengers()
    res = filter(lambda x: x.desired_floor != desired_floor, elev_passengers)
    elevator.set_passengers(list(res))


def empty_elevator(elevator, passengers):
    if len(elevator.get_passengers()) == 0 and len(passengers) == 0:
        elevator.set_direction(False)


def create_objects():

    building = Building()
    floors_amount = building.floors_amount
    building.floors = [Floor(floor_number=i, floor_amount=floors_amount) for i in range(1, floors_amount)]
    elevator = Elevator()
    for floor in building.floors:
        amount_passengers = floor.get_amount_passengers()

        for passenger in range(amount_passengers):

            desired_floor = get_desired_floor(floors_amount, floor.floor_number)
            floor.passengers.append(Passenger(current_floor=floor.floor_number, desired_floor=desired_floor))

    result = {'building': building, 'elevator': elevator}
    return result


def start_elevator(elevator, floors):

    step = 1
    for floor in floors:
        # checks if elevator on which floor
        if floor.floor_number == elevator.position:
            # passengers from this floor comes inside elevator if they go on same direction
            passed = passed_passengers(floor.passengers, elevator)
            come_inside_elevator(passed, floor.passengers, elevator)
            res = f'\n****** \n\nElevator goes to:{elevator.max_floor}, elevator on floor:{elevator.position}\n'
            i = 1

            for passenger in elevator.get_passengers():
                if passenger.desired_floor == elevator.position:
                    exit_from_elevator(passenger.desired_floor, elevator)

            for passenger in elevator.get_passengers():

                res += f'Passenger:' \
                    f' desired floor: {passenger.desired_floor}, \t'
                i += 1

            print(res)
            step += 1
            empty_elevator(elevator, floor.passengers)
            elevator.go()


def main():
    context = create_objects()
    building = context.get('building')
    elevator = context.get('elevator')
    floors = building.floors

    if elevator.max_floor is None:
        elevator.max_floor = 2

    start_elevator(elevator, floors)


if __name__ == "__main__":
    main()