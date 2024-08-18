import random
import time

pass_text = [' gives the ball to ' , ' passes it to ' , ' sharply gives it to ' , ' puts it in the path of ']
defend_text = [' performs a great tackle ' , ' comes up with a meaty tackle ']
shoot_text = [ 'hits the ball ' , ' curls it towards the goal ' , ' shoots ']
goal = ' have scored a beauty!'
no_goal = " have missed it!"

def match_day_teams(team, squad, opposition_manager, opposition_team, oppostion_squad):
    team_name = team
    match_team = squad
    opp_manager = opposition_manager
    opp_team_name = opposition_team
    opp_squad = oppostion_squad
    print(f"Your {team_name} team is: {match_team}\n")
    print(f"Your opposition are: {opp_team_name}, Managed by {opp_manager}\n")
    print(f"{opp_team_name}'s team are: {opp_squad}\n")

def match_start(opp_first_eleven, my_first_eleven, opp_team_name, my_team_name):
    my_team_score = 0
    opp_team_score = 0
    opp_team_first_eleven = opp_first_eleven
    my_team_first_eleven = my_first_eleven
    opp_name = opp_team_name
    my_team = my_team_name
    match_time = 0
    print("The Ref blows his whistle and we are under way!")
    while match_time < 10:
        goal_or_not = random.randint(0,1)
        whose_ball = random.randint(0,1)
        if whose_ball == 0:
            time.sleep(2)
            print("the ball is taken and {} {} {} {} ".format(random.choice(opp_team_first_eleven),random.choice(pass_text),random.choice(opp_team_first_eleven),random.choice(shoot_text)))
            time.sleep(2)
            if goal_or_not == 1 :
                print("{} score!".format(opp_name))
                opp_team_score += 1
                time.sleep(2)
                print(" it's {} {} ".format(str(my_team_score) , str(opp_team_score)))
                match_time += 1
            else :
                time.sleep(2)
                print("{} {} {} {}".format(random.choice(my_team_first_eleven),random.choice(pass_text),random.choice(my_team_first_eleven),random.choice(shoot_text)))
                time.sleep(2)
                print("{} {}!".format(opp_name,no_goal))
                match_time += 1
        else :
            if goal_or_not == 1 :
                    time.sleep(2)
                    print("{} {} {} {}".format(random.choice(my_team_first_eleven),random.choice(pass_text),random.choice(my_team_first_eleven),random.choice(shoot_text)))
                    time.sleep(2)
                    print("{} {}!".format(my_team,goal) )
                    my_team_score += 1
                    time.sleep(2)
                    print(" it's {} {} ".format(str(my_team_score) , str(opp_team_score)))
                    match_time += 1
            else :
                    time.sleep(2)
                    print("{} {} {} {}".format(random.choice(my_team_first_eleven),random.choice(pass_text),random.choice(my_team_first_eleven),random.choice(shoot_text)))
                    time.sleep(2)
                    print("{} {}!".format(my_team,no_goal))
                    time.sleep(2)
                    match_time += 1

    if my_team_score > opp_team_score :
        print("{} {} {} win!".format(my_team_score,opp_team_score,my_team))
    elif my_team_score < opp_team_score :
        print("{} {} {} win!".format(my_team_score,opp_team_score,opp_name))
    else :
        print("{} {} It's a tie".format(my_team_score,opp_team_score))            


