from files.classes import Enemy, battle_fighters
from files.helpers import getItemColor, checkYorN, outOfEnergy
from termcolor import colored
import random

def enemy_attack(_enemy_type):
    if (_enemy_type == 'Kraken' or _enemy_type == 'Shark'):
        if random.random() < 0.5:  # 60% chance of hitting with a regular attack
            return random.randint(10, 25)  # Regular attack damage
        else:
            return 0
    elif (_enemy_type == 'Kaiju' or _enemy_type == 'Kong'):
        if random.random() < 0.6:  # 60% chance of hitting with a regular attack
            return random.randint(15, 35)  # Regular attack damage
        else:
            return 0
    elif _enemy_type == 'Alien':
        if random.random() < 0.7:  # 60% chance of hitting with a regular attack
            return random.randint(20, 45)  # Regular attack damage
        else:
            return 0
    else:
        if random.random() < 0.6:  # 60% chance of hitting with a regular attack
            return random.randint(10, 15)  # Regular attack damage
        else:
            return 0

def pirate_sword():
    if random.random() < 0.6:  # 60% chance of hitting with a sword
        return random.randint(15, 35)  # Sword damage
    else:
        return 0

def pirate_cannon():
    if random.random() < 0.4:  # 40% chance of hitting with a cannon
        return random.randint(25, 55)  # Cannon damage
    else:
        return 0

def canPlayerSummon(_player):
    for item in _player.fighters:
        if (item == 'Kraken' or item == 'Shark') and _player.gold >= 100:
            return True
        elif (item == 'Kaiju' or item == 'Kong') and _player.gold >= 200:
            return True
        elif item == 'Alien' and _player.gold >= 300:
            return True
        else:
            return False

def spawnEnemy(_player):
    #enemy = Enemy()
    if not _player.fighters:
        fighter_options = ["Shark", "Kraken"]
        enemy_type = random.choice(fighter_options)
        if enemy_type == "Shark":
            enemy = Enemy(enemy_type, 100)
            return enemy
        else:
            enemy = Enemy(enemy_type, 100)
            return enemy
    elif len(_player.fighters) == 1:
        if "Shark" in _player.fighters:
            enemy = Enemy("Kraken", 100)
            return enemy
        else:
            enemy = Enemy("Shark", 100)
            return enemy
    elif len(_player.fighters) == 2:
        fighter_options = ["Kaiju", "Kong"]
        enemy_type = random.choice(fighter_options)
        if enemy_type == "Kaiju":
            enemy = Enemy(enemy_type, 200)
            return enemy
        else:
            enemy = Enemy(enemy_type, 200)
            return enemy
    elif len(_player.fighters) == 3:
        if "Kaiju" in _player.fighters:
            enemy = Enemy("Kong", 200)
            return enemy
        else:
            enemy = Enemy("Kaiju", 200)
            return enemy
    elif len(_player.fighters) == 4:
        enemy = Enemy("Alien", 300)
        return enemy
    else:
        print("This 'else' clause in spawnEnemy should not be executed.")

def enemySummonOption(_player):
    #print('Entered enemySummonOption...')
    options = []
    for item in _player.fighters:
        if (item == 'Kraken' or item == 'Shark') and _player.gold >= 100:
            #print(f'Added {item} to options')
            options.append(item)
        elif (item == 'Kaiju' or item == 'Kong') and _player.gold >= 200:
            #print(f'Added {item} to options')
            options.append(item)
        elif item == 'Alien' and _player.gold >= 300:
            #print(f'Added {item} to options')
            options.append(item)
        else:
            print('Nothing to add.  Not good if you entered this ELSE clause in enemySummonOption')
            return options
    #print(f'You summon options are: {options}')
    return options

def validFighterSelection(_fighter_options):
    counter = 1
    counter_options = []
    display_fighter_options = []  # USED FOR INPUT LOOP LATER
    print("Available Fighters: ")
    for fighter in _fighter_options:
        counter_options.append(counter)
        display_fighter_options.append(f'{counter}. {fighter}')
        print(f'{counter}. {fighter}')
        counter += 1
    selected = input("Which fighter would you like to attack with (enter the number)? ")
    while not selected.strip().isdigit() or int(selected) not in counter_options:
        #print('That was not a valid option.')
        #print(f'{selected} was entered.')
        #print('Counter options are:')
        #print(counter_options)
        #print(not selected.strip().isdigit())
        #print(selected not in counter_options)
        for item in display_fighter_options:
            print(item)
        selected = input("Which fighter would you like to attack with (enter the number)? ")
    return _fighter_options[int(selected)-1]


def getFighterDamage(_fighter):
    if (_fighter == 'Kraken' or _fighter == 'Shark'):
        return random.randint(50, 85)
    elif (_fighter == 'Kaiju' or _fighter == 'Kong'):
        return random.randint(85, 125)
    elif _creature == 'Alien':
        return random.randint(125, 200)

def getFighterCost(_fighter):
    if (_fighter == 'Kraken' or _fighter == 'Shark'):
        return 150
    elif (_fighter == 'Kaiju' or _fighter == 'Kong'):
        return 250
    elif _creature == 'Alien':
        return 400

def pirate_summon(_player):
    enemy_summon_options = enemySummonOption(_player)
    selected_fighter = validFighterSelection(enemy_summon_options)
    print('You have chosen to attack with your ' + colored(selected_fighter, getItemColor(selected_fighter)))
    damage = getFighterDamage(selected_fighter)
    cost = getFighterCost(selected_fighter)
    #print(f'This will deal ' + colored(damage,"red") + ' and cost ' + colored(cost,"yellow") + ' gold.')
    print('This summon cost ' + colored(cost,"yellow") + ' gold.')
    updated_player_gold = _player.gold - cost
    _player.update_gold(updated_player_gold)
    return damage

def playerBattle(_player, _game_map, _current_area):
    print('You entered player battle!')
    #os.system('clear')
    enemy = spawnEnemy(_player)
    enemy_color = getItemColor(enemy.enemy_type)
    print('Oh snap! A ' + colored(enemy.enemy_type,enemy_color) + ' appears with ' + colored(enemy.energy,"yellow") + ' energy!')
    print(f'Your current energy level is {_player.energy} so keep that in mind...')
    decision = checkYorN(input("Do you want to fight it (y/n)? "))
    if decision == 'n':
        print("Probably ok to skip this one (chicken).")
    elif decision == 'y':
        _game_map[_current_area].update_consumed(True)
    print("let's do it!")
    while _player.energy > 0 and enemy.energy > 0:
        print("Pirate's turn (enter number from options):")
        #if _player.inventory and _player.gold > 100:
        if canPlayerSummon(_player):
            attack_choice = input("1:sword | 2:cannon | 3:summon > ")
        else:
            attack_choice = input("1:sword | 2:cannon> ")
        if attack_choice == '1':
            damage = pirate_sword()
        elif attack_choice == '2':
            damage = pirate_cannon()
        elif attack_choice == '3':
            damage = pirate_summon(_player)
            print(f'Dealing ' + colored(damage, "red") + ' damage. ')
            print('Your updated gold amount is: ' + colored(_player.gold,"yellow"))
        else:
            print("Invalid choice. Pirate's turn skipped.")
            damage = 0

        enemy_energy = enemy.energy - damage
        enemy.update_energy(enemy_energy)
        print(colored(enemy.enemy_type, enemy_color) + " took " + colored(damage,"red") +
              " damage and now has " + colored(enemy.energy, "yellow"))

        if outOfEnergy(enemy):
            print(f'{enemy.enemy_type} has been defeated')
            print('Killing ' + colored(enemy.enemy_type, enemy_color) + 's always makes you feel better.')
            _player.update_energy(100)
            print('Your energy has been fully restored to ' + colored(_player.energy, "green"))
            _player.add_to_fighters(enemy.enemy_type)
            print('Even more, a ' + enemy.enemy_type + ' has been added to your inventory!')
            print('Your fighters:')
            for item in _player.fighters:
                print(item)
            break

        damage = enemy_attack(enemy.enemy_type)
        pirate_energy = _player.energy - damage
        _player.update_energy(pirate_energy)
        print("You took " + colored(damage, "red") +
              " damage and now have " + colored(_player.energy, "green"))

        if outOfEnergy(_player):
            print(f'Sadly, the {enemy.enemy_type} has defeated you.')
            break