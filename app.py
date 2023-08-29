from flask import Flask, render_template, request, redirect, url_for
from mapgeneration import *
from files.classes import *
from files.helpers import *
from battle import *

app = Flask(__name__)

def initializeGame():
    global game_map, current_area, player
    num_areas = 100
    game_map = generate_random_map(num_areas)
    current_area = setStartArea(game_map)
    player = Player(current_area)

def addHtmlBreaks(_msg):
    return _msg

def areaActionResult(_area_type):
    global game_map, current_area, player

    if _area_type=="Open Water":
        if not game_map[current_area].consumed:
            if player.energy != 100:
                game_map[current_area].update_consumed(True)
                amt = random.randint(5, 20)
                new_energy = min(100,player.energy + amt)
                player.update_energy(new_energy)
                return f'You were awarded {amt} energy and now have {player.energy}.'
            else:
                return f"You already have 100 energy.<br>(come back here when you don't)"
        else:
            return "You have already absorbed the energy this area has to offer."
    elif _area_type=='Treasure':
        if not game_map[current_area].consumed:
            if player.gold != 1000:
                game_map[current_area].update_consumed(True)
                amt = random.randint(45, 95)
                new_gold = min(1000, player.gold + amt)
                player.update_gold(new_gold)
                return f'You were awarded {amt} gold and now have {player.gold}.'
        else:
            return "You've already found all the gold this area has, Legend."
    elif _area_type=='Maelstrom':
        if not game_map[current_area].consumed:
            game_map[current_area].update_consumed(True)
            amt = random.randint(5, 20)
            amt *= -1
            new_energy = max(0, player.energy + amt)
            player.update_energy(new_energy)
            return f'You lost {amt} energy escaping the storm and now have {player.energy}'
        else:
            return 'You already survived the storm in this area.'
    elif _area_type=='Island':
        return "You already found the treasure here, no?"
    elif _area_type=='Battle':
        return "You already battled here, no?"

def percentMapVisitedAndConsumed():
    visited_areas, consumed_areas = 0,0
    global game_map
    for area_name in game_map:
        if game_map[area_name]['visited']:
            visited_areas += 1
        if game_map[area_name]['consumed']:
            consumed_areas += 1
    percent_map_visited = round((visited_areas / len(game_map)) * 100)
    percent_map_consumed = round((consumed_areas / len(game_map)) * 100)

    traverse_dictionary = {
        'visited_areas': visited_areas,
        'percent_map_visited': percent_map_visited,
        'consumed_areas': consumed_areas,
        'percent_map_consumed': percent_map_consumed
    }

    return traverse_dictionary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/battle', methods=['GET', 'POST'])
def battle():
    global enemy, battle_active
    if not enemy.enemy_type:
        enemy = spawnEnemy(player)
    message = f"Oh snap! a {enemy.enemy_type} has spawned with {enemy.energy} energy!"
    notes, attack_options = '', ''
    choice_made, displayed_results = False, False

    if request.method == 'POST':
        if choice_made:
            displayed_results = True
        else:
            print('else entered...')
            if battle_active:
                print('battle active entered...')
                message = "FIGHT!"
                battle_input = request.form.get('user_input_battle')
                print(f'battle input is {battle_input}')
                if battle_input == '1':
                    print('one')
                    enemy_damage = pirate_sword()
                    enemy_energy = enemy.energy - enemy_damage
                    enemy.update_energy(max(0, enemy_energy))
                    notes = f"You dealt {enemy_damage} damage to the {enemy.enemy_type}!"
                    if outOfEnergy(enemy):
                        notes = f'You defeated the {enemy.enemy_type}!<br>Which fully restored your energy!<br>' \
                                f'Also a {enemy.enemy_type} has been added to your fighters!'
                        player.update_energy(100)
                        player.add_to_fighters(enemy.enemy_type)
                        battle_active = False
                    player_damage = enemy_attack(enemy.enemy_type)
                    print(f'player_damage returned {player_damage}')
                    pirate_energy = player.energy - player_damage
                    player.update_energy(max(0, pirate_energy))
                    notes = f"You dealt {enemy_damage} damage to the {enemy.enemy_type} and took {player_damage} damage!"
                    if outOfEnergy(player):
                        notes = f'You were defeated by the {enemy.enemy_type}!'
                        player.update_alive(False)
                        battle_active = False
                        #redirect to END GAME screen?
                    if canPlayerSummon(player):
                        attack_options = "1:sword | 2:cannon | 3:summon"
                    else:
                        attack_options = "1:sword | 2:cannon"
                elif battle_input == '2':
                    print('two')
                    enemy_damage = pirate_cannon()
                    enemy_energy = enemy.energy - enemy_damage
                    enemy.update_energy(max(0, enemy_energy))
                    notes = f"You dealt {enemy_damage} damage to the {enemy.enemy_type}!"
                    if outOfEnergy(enemy):
                        notes = f'You defeated the {enemy.enemy_type}!<br>Which fully restored your energy!<br>' \
                                f'Also a {enemy.enemy_type} has been added to your fighters!'
                        player.update_energy(100)
                        player.add_to_fighters(enemy.enemy_type)
                        battle_active = False
                    player_damage = enemy_attack(enemy.enemy_type)
                    print(f'player_damage returned {player_damage}')
                    pirate_energy = player.energy - player_damage
                    player.update_energy(max(0, pirate_energy))
                    notes = f"You dealt {enemy_damage} damage to the {enemy.enemy_type} and took {player_damage} damage!"
                    if outOfEnergy(player):
                        notes = f'You were defeated by the {enemy.enemy_type}!'
                        player.update_alive(False)
                        battle_active = False
                        # redirect to END GAME screen?
                    if canPlayerSummon(player):
                        attack_options = "1:sword | 2:cannon | 3:summon"
                    else:
                        attack_options = "1:sword | 2:cannon"
                elif battle_input == '3' and canPlayerSummon(player):
                    notes = "you entered 3!"
                    chosen_fighter = enemySummonOptionAutoSelect(player)
                    message = f'a {chosen_fighter} has been summoned!'
                    print(f'a {chosen_fighter} has been summoned!')
                    enemy_damage = pirateSummonFighter(chosen_fighter)
                    gold_cost = getFighterCost(chosen_fighter)
                    updated_gold = player.gold - gold_cost
                    player.update_gold(updated_gold)
                    print(f'{chosen_fighter} has done {enemy_damage} damage and cost {gold_cost}')
                    enemy_energy = enemy.energy - enemy_damage
                    enemy.update_energy(max(0, enemy_energy))
                    notes = f"You dealt {enemy_damage} damage to the {enemy.enemy_type}!"
                    if outOfEnergy(enemy):
                        notes = f'You defeated the {enemy.enemy_type}!<br>Which fully restored your energy!<br>' \
                                f'Also a {enemy.enemy_type} has been added to your fighters!'
                        player.update_energy(100)
                        player.add_to_fighters(enemy.enemy_type)
                        battle_active = False
                    player_damage = enemy_attack(enemy.enemy_type)
                    print(f'player_damage returned {player_damage}')
                    pirate_energy = player.energy - player_damage
                    player.update_energy(max(0, pirate_energy))
                    notes = f"You dealt {enemy_damage} damage to the {enemy.enemy_type} and took {player_damage} damage!"
                    if outOfEnergy(player):
                        notes = f'You were defeated by the {enemy.enemy_type}!'
                        player.update_alive(False)
                        battle_active = False
                        # redirect to END GAME screen?
                    if canPlayerSummon(player):
                        attack_options = "1:sword | 2:cannon | 3:summon"
                    else:
                        attack_options = "1:sword | 2:cannon"
                else:
                    notes = f'Sorry {battle_input} is not accepted.'
                    print("Sorry. That's not an acceptable entry.")
            else:
                print('Battle is not active...')
                battle_input = request.form.get('battle_explore_choice')
                if battle_input == 'yes':
                    battle_active = True
                    game_map[current_area].update_consumed(True)
                    message = "Choose your attack:"
                    if canPlayerSummon(player):
                        attack_options = "1:sword | 2:cannon | 3:summon"
                    else:
                        attack_options = "1:sword | 2:cannon"
                elif battle_input == 'no':
                    message = "(probably) smart, Chicken."
                else:
                    notes = 'Sorry that input is not valid (BATTLE function)'
                choice_made = True
        #if 'battle_explore_choice' in request.form:
        #    print('battle_explore_choice')
        #    battle_input = request.form.get('battle_explore_choice')
        #elif 'user_input_battle' in request.form:
        #    print('entered user_input_battle')
        #    battle_input = request.form.get('user_input_battle')
        #if choice_made:
        #    displayed_results = True
        #else:

    if choice_made and displayed_results:
        return redirect('/play')  # Redirect to the main page after processing
    else:
        print(f'Battle active is: {battle_active}')
        return render_template('battle.html',
                               player=player,
                               area_type=game_map[current_area]['area_type'],
                               message=message,
                               notes=notes,
                               choice_made=choice_made,
                               enemy=enemy,
                               battle_active=battle_active,
                               attack_options=attack_options)

@app.route('/explore', methods=['GET', 'POST'])
def explore_island():
    message = 'Always a chance of finding gold.<br>Of course, you can get raided while you are searching.'
    notes = ''
    #explore_choice = request.form.get('explore_choice')
    choice_made = False
    displayed_results = False

    if request.method == 'POST':
        explore_choice = request.form.get('explore_choice')
        if choice_made:
            displayed_results = True
        else:
            if explore_choice == 'yes':
                find_gold = random.choice([True, False])
                if find_gold:
                    gold_before = player.gold
                    playerGold('award', player)
                    gold_after = player.gold
                    gold_awarded = gold_after - gold_before
                    notes = f'Nice!  You found {gold_awarded} gold!'
                else:
                    gold_before = player.gold
                    playerGold('strip', player)
                    gold_after = player.gold
                    gold_stripped = gold_after - gold_before
                    notes = f'Rekt!  You were raided for {gold_stripped} gold while you searched the island.'
                game_map[current_area].update_consumed(True)
            elif explore_choice == 'no':
                message = "Guess we'll never know what was out there..."
            else:
                notes = 'Sorry that input is not valid.'
            choice_made = True

    if choice_made and displayed_results:
        return redirect('/play')  # Redirect to the main page after processing
    else:
        return render_template('island.html',
                               player=player,
                               area_type=game_map[current_area]['area_type'],
                               message=message,
                               notes=notes,
                               choice_made=choice_made)


'''  

    if explore_choice == 'yes':
    #if displayed_results and not choice_made:
        if explore_choice == 'yes':
            find_gold = random.choice([True, False])
            if find_gold:
                gold_before = player.gold
                playerGold('award', player)
                gold_after = player.gold
                gold_awarded = gold_after - gold_before
                notes = f'Nice!  You found {gold_awarded} gold!'
            else:
                gold_before = player.gold
                playerGold('strip', player)
                gold_after = player.gold
                gold_stripped = gold_after - gold_before
                notes = f'Rekt!  You were raided for {gold_stripped} gold while you searched the island.'
            game_map[current_area].update_consumed(True)
        elif explore_choice == 'no':
            message = "Guess we'll never know what was out there..."
        else:
            notes = 'Sorry that input is not valid.'
        choice_made = True
    elif explore_choice == 'no':
    #else:
        choice_made = True
        displayed_results = True

    if choice_made and displayed_results:
        return redirect('/play')  # Redirect to the main page after processing
    else:
        return render_template('island.html',
                           player=player,
                           area_type=game_map[current_area]['area_type'],
                           message=message,
                           notes=notes,
                           choice_made=choice_made)
'''

@app.route('/play', methods=['GET', 'POST'])
def play():
    global player, game_map, current_area, enemy, battle_active
    traverse_dictionary = percentMapVisitedAndConsumed()
    direction_options = ', '.join(game_map[current_area]['connections'].keys())
    game_map[current_area].update_visited(True)
    message = 'Enter a direction in the input field below to go that way.'
    notes = ''
    battle_active = False

    if request.method == 'POST':
        if 'user_input' in request.form:
            print('entered user_input')
            user_input = request.form['user_input']
        elif 'island_button_continue' in request.form:
            print('entered island_button_continue')
            user_input = 'button_click'
        elif 'battle_button_continue' in request.form:
            print('entered battle_button_continue')
            user_input = 'button_click'
        if user_input.lower() in game_map[current_area]['connections']:
            current_area = game_map[current_area]['connections'][user_input.lower()]
            player.update_location(current_area)
            direction_options = ', '.join(game_map[current_area]['connections'].keys())
            message = f'You went {user_input.lower()}.'
            notes = areaActionResult(game_map[current_area]['area_type'])
            if game_map[current_area]['area_type'].lower() == 'island' and not game_map[current_area]['consumed']:
                #print('entered island consume')
                return redirect('/explore')
            elif game_map[current_area]['area_type'].lower() == 'battle' and not game_map[current_area]['consumed']:
                print('entered battle not consumed section')
                enemy = Enemy()
                return redirect('/battle')
        elif user_input.lower() in game_map[current_area]['secret_area_connections']:
            current_area = game_map[current_area]['secret_area_connections'][user_input.lower()]
            player.update_location(current_area)
            direction_options = ', '.join(game_map[current_area]['connections'].keys())
            message = f'You went {user_input.lower()}.'
            notes = areaActionResult(game_map[current_area]['area_type'])
        elif user_input.lower() == 'quit':
            #redirect to a thanks for playing page.
            message = "quit not supported yet.<br>(just close your browser)"
        elif user_input.lower() == 'button_click':
            message = "Ok so which way are we going now?"
        else:
            message = f'You cannot go {user_input}.'

    return render_template('game.html', player=player,
                           area_type=game_map[current_area]['area_type'],
                           direction_options=direction_options,
                           message=message,
                           notes=notes,
                           coordinates=game_map[current_area]['coordinates'],
                           traverse_dictionary=traverse_dictionary,
                           area_consumed=game_map[current_area]['consumed'])

def startHere():
    global game_map, current_area, player, enemy, battle_active
    battle_active = False
    initializeGame()
    app.run(debug=True)

if __name__ == '__main__':
    startHere()