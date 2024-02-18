import Managers

teams = [
    'Arsenal',
    'Aston Villa',
    'Bournemouth',
    'Brentford',
    'Brighton',
    'Burnley',
    'Chelsea',
    'Crystal Palace',
    'Everton',
    'Fulham',
    'Liverpool',
    'Luton Town',
    'Manchester City',
    'Manchester United',
    'Newcastle United',
    'Nottingham Forest',
    'Sheffield United',
    'Tottenham Hotspur',
    'West Ham United',
    'Wolverhampton Wanderers'
]


def add_managers_to_team():
        team_managers = {teams[i]: Managers.managers[i] for i in range(len(teams))}
        return team_managers

team_manager_dictionary = add_managers_to_team()

def append_team_managers(team, manager):
        team_manager_dictionary.update({team:manager})
        print(team_manager_dictionary)
        return team_manager_dictionary
