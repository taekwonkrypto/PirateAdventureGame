import random, math
from files.lists import area_names, area_directions, area_types, secret_area_names
from files.classes import Area

def getDirectionCoordinates(_areas, _current_area, _direction):
    if _direction == 'west':
        return [_areas[_current_area]['coordinates'][0] - 1, _areas[_current_area]['coordinates'][1]]
    elif _direction == 'east':
        return [_areas[_current_area]['coordinates'][0] + 1, _areas[_current_area]['coordinates'][1]]
    elif _direction == 'north':
        return [_areas[_current_area]['coordinates'][0], _areas[_current_area]['coordinates'][1] + 1]
    else:
        return [_areas[_current_area]['coordinates'][0], _areas[_current_area]['coordinates'][1] - 1]

# Generate a random dictionary of rooms with connections and secret doors
def generate_random_map(_num_areas):
    total_secret_areas = 0
    secret_areas = {}
    areas = {}
    unique_area_names = random.sample(area_names, _num_areas)
    for i in range(_num_areas):
        area_name = unique_area_names[i]
        # CREATE ALL OF THE GAME AREAS AND SET THEM TO BASICALLY EMPTY STUFF
        #areas[area_name] = {'area_type': None,
        #                    'connections': {},
        #                    'secret_area_connections': {},
        #                    'coordinates': None,
        #                    'visited': False
        #}
        areas[area_name] = Area()
    # TO CONNECT THE MAP, I AM GOING TO MANUALLY TRAVERSE ALL OF IT, CONNECTING IT AS I GO
    # I TRIED SEVERAL OTHER ITERATIONS (GOOGLE 'PRIMS ALGORITHM' BUT IN THE END, THIS WAS THE MOST DEPENDABLE
    # TO CREATE AN ACTUAL GRID, SO EAST 4X WILL GET YOU BACK TO THE SAME OPEN AREA
    unvisited_areas = list(areas.keys())  # FIRST, CREATE A LIST OF ALL OF THE AREA NAMES (AREAS.KEYS())
    current_area = random.choice(list(areas.keys())) # RANDOMLY PICK A STARTING POINT
    visited_areas = [current_area] # BEGIN A NEW ARRAY OF AREAS VISITED, TO KEEP TRACK
    unvisited_areas.remove(current_area) # REMOVE THE AREA WE ARE IN, BECAUSE WE HAVE VISITED IT.
    coordinates = [0,0] # NEEDED THIS TO MAKE SURE I HANDLE GOING BACK INTO AN AREA PROPERLY
    while unvisited_areas:
        #areas[current_area]['coordinates'] = coordinates
        areas[current_area].update_coordinates(coordinates)
        if areas[current_area]['connections'].keys(): # IF THE CURRENT AREA ALREADY HAS A CONNECTION
            # GET A DIRECTION NOT USED IN CURRENT AREA
            direction = random.choice(list(set(area_directions) - set(areas[current_area]['connections'].keys())))
            coordinates = getDirectionCoordinates(areas, current_area, direction)
            match_found = False # NEED TO SEARCH IF THE NEW SELECTION IS CONNECTED TO ANOTHER ROOM ALREADY
            for area_name, area_info in areas.items():
                #if area_info.get('coordinates') == coordinates:
                if areas[area_name].coordinates == coordinates:
                    match_found = True
                    next_area = area_name
            if not match_found:
                next_area = random.choice(unvisited_areas)
                unvisited_areas.remove(next_area)
            #areas[next_area]['coordinates'] = coordinates
            areas[next_area].update_coordinates(coordinates)
            visited_areas.append(next_area)
            areas[current_area]['connections'][direction] = next_area
            areas[next_area]['connections'][get_opposite_door(direction)] = current_area
            current_area = next_area
        else:
            direction = random.choice(area_directions)
            coordinates = getDirectionCoordinates(areas, current_area, direction)
            next_area = random.choice(unvisited_areas)
            #areas[next_area]['coordinates'] = coordinates
            areas[next_area].update_coordinates(coordinates)
            visited_areas.append(next_area)
            unvisited_areas.remove(next_area)
            areas[current_area]['connections'][direction] = next_area
            areas[next_area]['connections'][get_opposite_door(direction)] = current_area
            current_area = next_area

    # ONCE ALL THE AREAS CREATED, RANDOMLY GIVE THEM AREA TYPES.
    # MIGHT BE WORTH "WEIGHTING" THESE SOME DAY TO GIVE MORE OF ONE OR ANOTHER
    # NEED DATA TO KNOW FOR SURE
    openwater_area_exists = False  # STARTING PLACE WILL BE OPEN WATER SO AT LEAST ONE NEEDS TO EXIST
    for area_name in areas:
        if openwater_area_exists:
            #areas[area_name]['area_type'] = random.choice(area_types)
            areas[area_name].update_area_type(random.choice(area_types))
        else:
            #areas[area_name]['area_type'] = 'Open Water'
            areas[area_name].update_area_type('Open Water')
            openwater_area_exists = True

    # CREATE AND UPDATE SECRET AREAS
    secret_area_counter = 0
    # SINCE WE PICK AN UNUSED CONNECTION, SECRET ROOMS CANNOT HAVE 4 CONNECTIONS ALREADY
    secret_area_options = []
    for area_name, area_item in areas.items():
        if len(area_item['connections']) < 4:
            secret_area_options.append(area_name)
            # SECRET_AREA_OPTIONS NOW HAS ALL AREA NAMES WITH LESS THAN 4 CONNECTIONS
    #areas_to_have_secret_rooms = random.sample(list(areas.keys()), math.ceil(len(areas) * .1)) # 10% SECRET ROOMS
    areas_to_have_secret_rooms = random.sample(secret_area_options, math.ceil(len(areas) * .1))  # 10% SECRET ROOMS
    if not areas_to_have_secret_rooms: #JUST IN CASE NONE ARE RETURNED, GET AT LEAST 1
        areas_to_have_secret_rooms = random.sample(secret_area_options, 1)

    # SIMILAR TO GENERATING UNIQUE NAMES FOR AREAS EALIER
    # GENERATE UNIQUE NAMES FOR SECRET AREAS HERE
    unique_secret_area_names = random.sample(secret_area_names, len(areas_to_have_secret_rooms))

    for area_name in areas_to_have_secret_rooms:
        #print('++++')
        #print(set(area_directions))
        #print('----')
        #print(set(areas[area_name]['connections'].keys()))
        secret_area_direction = random.choice(list(set(area_directions) - set(areas[area_name]['connections'].keys())))
        areas[area_name]['secret_area_connections'][secret_area_direction] = unique_secret_area_names[secret_area_counter]
        secret_area_counter += 1

    for area_name, area_data in areas.items():
        if area_data['secret_area_connections']:
            secret_area_name = area_data['secret_area_connections'][list(area_data['secret_area_connections'])[0]]
            #secret_areas[secret_area_name] = {'area_type': 'Secret Area', 'connections': {}, 'secret_area_connections': None, 'visited': False}
            secret_areas[secret_area_name] = Area('Secret Area')
            secret_areas[secret_area_name]['connections'][get_opposite_door(list(area_data['secret_area_connections'])[0])] = area_name

    areas.update(secret_areas)  #APPEND SECRET ROOMS
    return areas

# Helper function to get the opposite door direction
def get_opposite_door(direction):
    opposites = {'north': 'south', 'south': 'north', 'west': 'east', 'east': 'west'}
    return opposites[direction]


def printMap(areas):
    # Print the generated map
    #for area_name, area_data in random_map.items():
    for area_name, area_data in areas.items():
        connections = area_data['connections']
        secret_area_connections = area_data['secret_area_connections']
        area_type = area_data['area_type']
        print(
            f"{area_name} - connections: {', '.join([f'{area}: {connected_area}' for area, connected_area in connections.items()])}")
        print(f"   Area Type: {area_type}")
        if secret_area_connections:
            print(f"   Secret Area: {secret_area_connections}")

def setStartArea(_random_map):
    open_water_areas = []
    for area_name in _random_map:
        if _random_map[area_name]['area_type'] == 'Open Water':
            open_water_areas.append(area_name)
    return random.choice(open_water_areas)