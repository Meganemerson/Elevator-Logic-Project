from enum import Enum
from collections import deque

class Direction(Enum):
    up = 1
    still = 0
    down = -1

outside_up = deque() #outside of elevator wanting to go up
outside_down = deque() #outside of elevator wanting to go down
inside = deque() #inside of elevator request

def Outside_Request(floor, direct):
    if direct == Direction.up:
        outside_up.append(floor)
    elif direct == Direction.down:
        outside_down.append(floor)
    print(f"Added outside request: floor {floor}, direction {direct.name}")

def Inside_Request(floor):
    inside.append(floor)
    print(f"Added inside request: floor {floor}")

def All_Requests():
    return sorted(list(outside_up) + list(outside_down) + list(inside))
def Next_Direction(floor, direct):
    curr_requests = All_Requests()
    print(f"Current pending requests: {curr_requests}")
    if not curr_requests:
        return None

    higher = []
    for i in curr_requests:
        if i > floor:
            higher.append(i)

    lower = []
    for i in curr_requests:
        if i > floor:
            lower.append(i)

    if direct == Direction.still:
        nearest = None
        nearest_dist = float('inf')

        for i in curr_requests:
            dist = abs(i - floor)
            if dist < nearest_dist:
                nearest = i
                nearest_dist = dist

        return nearest

    #Going upward, fulfills closest upward request first
    if direct == Direction.up:
        if higher:
            return min(higher)
        if lower:
            return max(lower) #called if no upward requests

    # Going downward, fulfills closest downward request first
    if direct == Direction.down:
        if lower:
            return max(lower)
        if higher:
            return min(higher) #called if no downward requests

    return None

def Stops(floor):
    if floor in inside:
        inside.remove(floor)
        print(f"Stop: floor {floor}")

    if floor in outside_up:
        outside_up.remove(floor)
        print(f"Stop: floor {floor}")

    if floor in outside_down:
        outside_down.remove(floor)
        print(f"Stop: floor {floor}")

def main(start_floor, start_direction):
    curr_floor = start_floor
    curr_direction = start_direction

    while All_Requests():
        next_floor = Next_Direction(curr_floor, curr_direction)
        if next_floor is None:
            break

        #update direction for next floor
        if next_floor == curr_floor:
            curr_direction = Direction.still

        elif next_floor > curr_floor:
            curr_direction = Direction.up

        else:
            curr_direction = Direction.down

        curr_floor = next_floor
        Stops(curr_floor)

    print(f"All Requests Fulfilled.")
    return curr_floor, curr_direction

#Test to run

# Outside_Request(1, Direction.up)
# Outside_Request(5, Direction.down)
# Inside_Request(9)
# Inside_Request(2)

#curr_floor, curr_direction = main(1, Direction.still)
