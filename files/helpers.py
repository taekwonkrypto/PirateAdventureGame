from termcolor import colored
import random

def getItemColor(_input):
    if _input == 'Open Water' or _input == "Shark":
        return "blue"
    elif _input == 'Treasure':
        return "green"
    elif _input == 'Maelstrom' or _input == "Kaiju":
        return "red"
    elif _input == 'Battle':
        return "magenta"
    elif _input == 'Island':
        return "yellow"
    elif _input == "Kraken":
        return "light_red"
    elif _input == "Kong":
        return "light_cyan"
    elif _input == "Alien":
        return "light_green"
    else:
        return "white"

def goldDecision(_player, _new_gold):
    #print(f'Current player gold: {_player.gold}')
    updated_gold = _player.gold + _new_gold
    if _new_gold > 0:
        if updated_gold >= 1000:
            return 1000
        else:
            return updated_gold
    else:
        if updated_gold <= 0:
            return 0
        else:
            return updated_gold
def energyDecision(_player, _new_energy):
    updated_energy = _player.energy + _new_energy
    if _new_energy > 0:
        if updated_energy >= 100:
            return 100
        else:
            return updated_energy
    else:
        if updated_energy <= 0:
            return 0
        else:
            return updated_energy

def playerEnergy(_option, _player):
    if _option == 'award':
        if _player.energy == 100:
            print(f'You already have full health so get going, {_player.player_name}! ')
        if _player.energy < 100:
            energy_gain = random.randint(5, 20)
            new_energy = energyDecision(_player, energy_gain)
            _player.update_energy(new_energy)
            print('Your new energy amount is ' + colored(_player.energy, "light_yellow"))
    elif _option == 'strip':
        if _player.energy == 0:
            print('You have no energy.  You should be dead.')
        if _player.energy >= 0:
            energy_lost = random.randint(5, 20)
            energy_lost *= -1
            new_energy = energyDecision(_player, energy_lost)
            _player.update_energy(new_energy)
            print('Your new energy amount is ' + colored(_player.energy, "light_yellow"))
    else:
        print(f'{_option} is not a recognized option in playerGold function.')

def playerGold(_option, _player):
    if _option == 'award':
        if _player.gold == 750:
            print(f'But you ship is at capacity, {_player.player_name}! ')
        if _player.gold < 750:
            gold_gain = random.randint(10, 50)
            new_gold = goldDecision(_player, gold_gain)
            _player.update_gold(new_gold)
            print('Your new gold amount is ' + colored(_player.gold,"light_yellow"))
    elif _option == 'strip':
        if _player.gold == 0:
            print('You are already out of gold, so no fear of losing that, at least.')
        if _player.gold >= 0:
            gold_lost = random.randint(10, 50)
            gold_lost *= -1
            new_gold = goldDecision(_player, gold_lost)
            _player.update_gold(new_gold)
            print('Your new gold amount is ' + colored(_player.gold,"light_yellow"))
    else:
        print(f'{_option} is not a recognized option in playerGold function.')

def playerStatus(_player, _game_map):
    print('********** PLAYER STATS ***********')
    print(f'*** Gold: {_player.gold}')
    print(f'*** Energy: {_player.energy}')
    if _player.inventory:
        print(f'*** Inventory: {_player.energy}')
        for item in _player.inventory:
            print(f'*** - {item}')
    visited_areas = 0
    for area_name in _game_map:
        if _game_map[area_name]['visited']:
            visited_areas += 1
    percent_map_visited = round((visited_areas/len(_game_map))*100)
    print(f'*** Areas Visited: {visited_areas} ({percent_map_visited}% of the map)')
    print('*********************************')

def playerOutOfEnergy(_player):
    if _player.energy <= 0:
        return True
    else:
        return False

def playerOutOfGold(_player):
    if _player.gold <= 0:
        return True
    else:
        return False