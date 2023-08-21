import random
from files.lists import battle_fighters

class Player:
    def __init__(self,  _location=None,\
                        _player_name="Captain Captain",\
                        _energy=100, \
                        _gold=250,
                        _inventory=[],
                        _winner=False) -> object:

        self.player_name = _player_name
        self.energy = _energy
        self.gold = _gold
        self.location = _location
        self.inventory = _inventory
        self.winner = _winner

    def update_player_name(self, _player_name):
        self.player_name = _player_name
    def update_energy(self, _int):
        self.energy = _int
    #def remove_energy(self, _int):
    #    self.energy -= _int
    def update_gold(self, _int):
        self.gold = _int
    #def remove_gold(self, _int):
    #    self.gold -= _int
    def update_location(self, _location):
        self.location = _location
    def add_to_inventory(self, _item):
        self.inventory.append(_item)
    def update_winner(self, _status):
        self.winner = _status

class Enemy:
    def __init__(self, _enemy_type=None, _energy=100, _master=None):
        self.enemy_type = _enemy_type
        self.energy = _energy
        self.master = _master

    def update_energy(self, _int):
        self.energy = _int
    def update_master(self, _owner):
        self.master = _owner
    def update_enemy_type(self, _enemy_type):
        self.enemy_type = _enemy_type