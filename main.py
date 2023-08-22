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
        area_color = getItemColor(game_map[current_area]['area_type'])
        game_map[current_area].updated_visited(True)
        player_won = checkIfPlayerWon()
        if player_won:
            print("Wow!  You won!")
            break

        print("\n+++ You are in " + colored(current_area,"cyan") + ", a " + colored(game_map[current_area]['area_type'], area_color) + " Area.")

        if game_map[current_area]['area_type'] == 'Open Water':
            if open_water_first_time:
                print('> Open Water is so relaxing. ')
                print('> No enemies in site you and your crew can finally recharge.')
                print('> Your energy might go up when in these areas.')
                open_water_first_time = False
            playerEnergy('award', player)
        elif game_map[current_area]['area_type'] == 'Treasure':
            if treasure_first_time:
                print('> You found a Treasure area!')
                print('> Your gold might go up when in these areas.')
                treasure_first_time = False
            playerGold('award', player)
        elif game_map[current_area]['area_type'] == 'Maelstrom':
            if maelstrom_first_time:
                print('> Oh no! You have encountered a Maelstrom!')
                print("> Not good.  It's going to take energy to escape and some gold always goes overboard...")
                maelstrom_first_time = False
            playerGold('strip', player)
            playerEnergy('strip', player)
            if playerOutOfEnergy(player):
                print(f'You breathed your last breath, {player.player_name}.')
                print('You died.  rip.')
                break
            if playerOutOfGold(player):
                print(f'You ran out of gold to pay your pirates, {player.player_name}')
                print('Mutiny insued and you died')
                print('rip')
                break

        options = ', '.join(game_map[current_area]['connections'].keys())
        print('Available directions:', colored(options, "red"))

        if game_map[current_area]['secret_area_connections']:
            print('You sense a hidden path in one direction...')

        direction = input('Enter a direction (above) to move, "quit" to exit, or "status" to view your progress: ').strip().lower()

        if direction == 'quit':
            print('Thanks for playing!')
            break

        if direction in game_map[current_area]['connections']:
            current_area = game_map[current_area]['connections'][direction]
        elif direction in game_map[current_area]['secret_area_connections']:
            print("You've discovered a hidden path!")
            current_area = game_map[current_area]['secret_area_connections'][direction]
        elif direction == 'status':
            playerStatus(player, game_map)
        else:
            print("\n*** You cannot go " + colored(direction, "red") + "\n")

if __name__ == "__main__":
    # Generate a map with num_areas rooms and connect them
    num_areas = 50
    game_map = generate_random_map(num_areas)
    #player_name = input("Enter a player name:  ")
    #printMap(game_map)
    current_area = setStartArea(game_map)
    player = Player(current_area)
    gameStart(current_area, player)