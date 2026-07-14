from features/teams/team_stats import TeamStats

team = TeamStats(
    team_id=2,
    user="root",
    password="",
    database="rawdata_teams"
)
print("="*50)
print("TEAM ID:", team.team_id)
print("="*50)

print("\nGOALS")
print("For:", team.average("goals_for"))
print("Against:", team.average("goals_against"))
print("Total:", team.average_total("goals"))

print("\nSHOTS")
print("For:", team.average("shots_for"))
print("Against:", team.average("shots_against"))
print("Total:", team.average_total("shots"))

print("\nSHOTS ON TARGET")
print("For:", team.average("shots_on_target_for"))
print("Against:", team.average("shots_on_target_against"))
print("Total:", team.average_total("shots_on_target"))

print("\nCORNERS")
print("For:", team.average("corners_for"))
print("Against:", team.average("corners_against"))
print("Total:", team.average_total("corners"))

print("\nOFFSIDES")
print("Average:", team.average("offsides"))

print("\nYELLOW CARDS")
print("Total:", team.average_total("yellow_cards"))

print("\nRED CARDS")
print("Total:", team.average_total("red_cards"))

print("\nXG")
print("For:", team.average("xg"))
print("Against:", team.average("xga"))
print("Total:", team.average_total("xg"))

print("\nGOAL TIMING")
print("First Goal:", team.average("first_goal_minute"))
print("Last Goal:", team.average("last_goal_minute"))

print("\nVARIANCE (MAD)")
print("Goals For:", team.variance("goals_for"))
print("Shots For:", team.variance("shots_for"))
print("Shots Total:", team.variance("shots"))
print("Shots On Target:", team.variance("shots_on_target"))
print("Corners:", team.variance("corners"))

team.close()