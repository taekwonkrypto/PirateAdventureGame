import os
from files.lists import battle_fighters
from mapgeneration import *
from files.classes import *
from files.helpers import *
from termcolor import colored
from battle import *

def checkIfPlayerWon():
    visited_areas = 0
    consumed_areas = 0
    for area_name in game_map:
        if game_map[area_name]['visited']:
            visited_areas += 1
        if game_map[area_name]['consumed']:
            consumed_areas += 1
    if visited_areas == len(game_map) and consumed_areas == len(game_map):
        print('Oy!  You visited and consumed EVERY AREA OF THE MAP!')
        print('This is the best you can possibly do!')
        return True
    elif visited_areas == len(game_map) and consumed_areas < len(game_map):
        print('Oy!  You visited, but did not consume every area of the map!')
        print('This is ok, but you could have done better.')
        return True
    elif len(player.fighters) == len(battle_fighters):
        print('Congratulations!  You have captured ALL FIGHTERS and now RULE THE OPEN SEA')
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
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("+++ You are in " + colored(current_area,"cyan") + ", a " + colored(game_map[current_area]['area_type'], area_color) + " Area.")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        if game_map[current_area]['area_type'] == 'Open Water':
            if open_water_first_time:
                print('><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><')
                print('> Open Water is so relaxing.                                   <')
                print('> No enemies in site you and your crew can finally recharge.   <')
                print('> Your energy might go up when in these areas.                 <')
                print('><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><')
                open_water_first_time = False
            #print('Visited Status: ' +str(game_map[current_area]['visited']))
            if game_map[current_area]['consumed']:
                print('][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][')
                print("] You've already absorbed the energy from this relaxing place. [")
                print("]   No energy is awarded.                                      [")
                print('][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][')
            else:
                if player.energy != 100:
                    game_map[current_area].update_consumed(True)
                playerEnergy('award', player)
            #playerEnergy('award', player)
        elif game_map[current_area]['area_type'] == 'Treasure':
            if treasure_first_time:
                print('><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><')
                print('> You found a Treasure area!                                   <')
                print('> Your gold might go up when in these areas.                   <')
                print('><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><')
                treasure_first_time = False
            if game_map[current_area]['consumed']:
                print('][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][')
                print("] You already found the gold in this area.                     [")
                print("]    No gold is awarded.                                       [")
                print('][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][')
            else:
                playerGold('award', player)
                game_map[current_area].update_consumed(True)
        elif game_map[current_area]['area_type'] == 'Maelstrom':
            if maelstrom_first_time:
                print('><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><')
                print('> Oh no! You have encountered a Maelstrom!                     <')
                print("> You'll burn energy to escape and gold always goes overboard. <")
                print('><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><')
                maelstrom_first_time = False
            if game_map[current_area]['consumed']:
                print('][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][')
                print("] The storm has passed in this area.                           [")
                print("]    Good news is you don't lose anything.                     [")
                print('][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][')
            else:
                playerGold('strip', player)
                playerEnergy('strip', player)
                game_map[current_area].update_consumed(True)
                if outOfEnergy(player):
                    print(f'You breathed your last breath, {player.player_name}.')
                    print('You died.  rip.')
                    break
                if playerOutOfGold(player):
                    print(f'You ran out of gold to pay your pirates, {player.player_name}')
                    print('Mutiny insued and you died')
                    print('rip')
                    break
        elif game_map[current_area]['area_type'] == 'Island':
            if island_first_time:
                print('> Sweet! Land!')
                print("> There's always a chance you'll find gold on an island!")
                print("> But leaving the ship is risky as you might get raided while you're gone.")
                island_first_time = False
            if game_map[current_area]['consumed']:
                print("> You've already searched this island")
                print(">    Nothing to see here.")
            else:
                decision = checkYorN(input("Do you want to search the island for treasure (y/n)? "))
                if decision == 'y':
                    print("Good luck!")
                    find_gold = random.choice([True, False])
                    if find_gold:
                        print('Nice!  You found ' + colored("gold!","yellow"))
                        playerGold('award', player)
                    else:
                        print('Rekt.  While you searched for gold, you were ' + colored("raided","red"))
                        playerGold('strip', player)
                    game_map[current_area].update_consumed(True)
                    print(f'\n***You are still in {current_area}')
                else:
                    print("Guess we'll never know what was out there...")
                    print(f'\n***You are still in {current_area}')
        elif game_map[current_area]['area_type'] == 'Battle':
            if game_map[current_area]['consumed']:
                print('You already battled in this area!')
            else:
                playerBattle(player, game_map, current_area)
                #game map consumed is handled in playerBattle, not here.
        elif game_map[current_area]['area_type'] == 'Secret Area':
            print('Oooo...a secret area!  Nice.')
            print('Maybe something worth finding will be here one day.')
            game_map[current_area].update_consumed(True)
            game_map[current_area].update_visited(True)
        if outOfEnergy(player):
            print(f'gg.')
            break
        game_map[current_area].update_visited(True)

        options = ', '.join(game_map[current_area]['connections'].keys())
        print('Available directions:', colored(options, "red"))

        if game_map[current_area]['secret_area_connections']:
            print('You sense a ' + colored("hidden path","yellow") + ' in one direction...')

        direction = input('Enter a direction (above) to move, "quit" to exit, or "status" to view your progress: ').strip().lower()

        if direction == 'quit':
            print('Thanks for playing!')
            break

        if direction in game_map[current_area]['connections']:
            current_area = game_map[current_area]['connections'][direction]
        elif direction in game_map[current_area]['secret_area_connections']:
            print("You've discovered a " + colored("hidden path","yellow") + "!")
            current_area = game_map[current_area]['secret_area_connections'][direction]
        elif direction == 'status':
            playerStatus(player, game_map)
        else:
            print("\n*** You cannot go " + colored(direction, "red") + "\n")

        player_won = checkIfPlayerWon()
        if player_won:
            print("gg.")
            break

if __name__ == "__main__":
    # Generate a map with num_areas rooms and connect them
    num_areas = 100
    game_map = generate_random_map(num_areas)
    #player_name = input("Enter a player name:  ")
    #printMap(game_map)
    current_area = setStartArea(game_map)
    player = Player(current_area)
    gameStart(current_area, player)