import Teams
import Player
import PlayerTeams
import Match
import os


Teams.add_managers_to_team()
team = Player.add_player()
os.system('cls')
squad = PlayerTeams.get_match_day_team(team)
opp_team_manager = Teams.get_opposition_manager()
opp_team_key = opp_team_manager
opp_team = opp_team_key[0]
opp_squad = PlayerTeams.get_match_day_team(opp_team)
Match.match_day_teams(team, squad, opp_team_manager, opp_team, opp_squad)
Match.match_start(opp_squad, squad, opp_team, team)
