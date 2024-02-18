import Managers
import Teams

name = ""

def add_player():
    name = (input("Please enter your full name: "))
    Managers.add_manager(name)
    add_player_to_team(name)

def add_player_to_team(name):
    print(Teams.teams)
    team = (input("Please select team to manager: "))
    Teams.append_team_managers(team, name)
    
