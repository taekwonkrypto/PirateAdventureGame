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

@app.route('/explore', methods=['GET', 'POST'])
def explore_island():
    message = 'Always a chance of finding gold.<br>Of course, you can get raided while you are searching.'
    notes = ''
    explore_choice = request.form.get('explore_choice')
    choice_made = False
    displayed_results = False

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

@app.route('/play', methods=['GET', 'POST'])
def play():
    global player, game_map, current_area
    traverse_dictionary = percentMapVisitedAndConsumed()
    direction_options = ', '.join(game_map[current_area]['connections'].keys())
    game_map[current_area].update_visited(True)
    message = 'Enter a direction in the input field below to go that way.'
    notes = ''


    if request.method == 'POST':
        if 'user_input' in request.form:
            print('entered user_input')
            user_input = request.form['user_input']
        elif 'island_button_continue' in request.form:
            print('entered island_button_continue')
            user_input = 'button_click'
        if user_input in game_map[current_area]['connections']:
            current_area = game_map[current_area]['connections'][user_input]
            player.update_location(current_area)
            direction_options = ', '.join(game_map[current_area]['connections'].keys())
            message = f'You went {user_input}.'
            notes = areaActionResult(game_map[current_area]['area_type'])
            if game_map[current_area]['area_type'].lower() == 'island' and not game_map[current_area]['consumed']:
                #print('entered island consume')
                return redirect('/explore')
        elif user_input in game_map[current_area]['secret_area_connections']:
            current_area = game_map[current_area]['secret_area_connections'][user_input]
            player.update_location(current_area)
            direction_options = ', '.join(game_map[current_area]['connections'].keys())
            message = f'You went {user_input}.'
            notes = areaActionResult(game_map[current_area]['area_type'])
        elif user_input == 'quit':
            #redirect to a thanks for playing page.
            message = "quit not supported yet.<br>(just close your browser)"
        elif user_input == 'button_click':
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
    global game_map, current_area, player
    initializeGame()
    app.run(debug=True)

if __name__ == '__main__':
    startHere()