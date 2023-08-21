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