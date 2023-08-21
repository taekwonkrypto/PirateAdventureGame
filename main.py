import os
from files.lists import battle_fighters
from mapgeneration import *
from files.classes import *
from files.helpers import *
from termcolor import colored

def checkIfPlayerWon():
    visited_areas = 0
    for area_name in game_map:
        #print(f'** {area_name}')
        if game_map[area_name]['visited']:
            #print(f'You have visited {area_name}')
            visited_areas += 1
    percent_map_visited = round((visited_areas/len(game_map))*100)
    #print(f'You have visited {percent_map_visited}% of the map!')
    if visited_areas == len(game_map):
        print('Oy!  You visited EVERY AREA OF THE MAP!')
        return True
    else:
        return False

def gameStart(current_area, player):
    open_water_first_time = True
    treasure_first_time = True
    maelstrom_first_time = True
    island_first_time = True
    while True:
        os.system('clear')
        area_color = getItemColor(game_map[current_area]['area_type'])
        game_map[current_area]['visited'] = True
        player_won = checkIfPlayerWon()
        if player_won:
            print("Wow!  You won!")
            break

        print("You are in " + colored(current_area,"cyan") + ", a " + colored(game_map[current_area]['area_type'], area_color) + " Area.")

        options = ', '.join(game_map[current_area]['connections'].keys())
        # print('Available directions:', ', '.join(random_map[current_area]['connections'].keys()))
        print('Available directions:', colored(options, "red"))

        if game_map[current_area]['secret_area_connections']:
            print('You sense a hidden path in one direction...')

        direction = input('Enter a direction (above) to move, or "quit" to exit: ').strip().lower()

        if direction == 'quit':
            print('Thanks for playing!')
            break

        if direction in game_map[current_area]['connections']:
            current_area = game_map[current_area]['connections'][direction]
        elif direction in game_map[current_area]['secret_area_connections']:
            print("You've discovered a hidden path!")
            current_area = game_map[current_area]['secret_area_connections'][direction]
        else:
            print('You cannot go that way.')

if __name__ == "__main__":
    # Generate a map with num_areas rooms and connect them
    num_areas = 5
    game_map = generate_random_map(num_areas)
    #player_name = input("Enter a player name:  ")
    printMap(game_map)
    current_area = setStartArea(game_map)
    player = Player(current_area)
    gameStart(current_area, player)