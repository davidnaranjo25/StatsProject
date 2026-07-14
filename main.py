import pymysql
from features.teams.team_stats import TeamStats

# Database Connection Details
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "rawdata_teams"
}

def get_available_teams():
    """Queries the database to fetch active team names and IDs."""
    teams_list = {}
    try:
        connection = pymysql.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            # Assumes your teams table is named 'teams' with 'id' and 'name' columns
            cursor.execute("SELECT id, name FROM teams ORDER BY id ASC")
            for row in cursor.fetchall():
                teams_list[row["id"]] = row["name"]
    except Exception as e:
        print(f"⚠️ Error fetching team list: {e}")
    finally:
        if 'connection' in locals():
            connection.close()
    return teams_list

# =====================================================================
# TEAM SELECTION MENU
# =====================================================================
print("=" * 50)
print("             AVAILABLE TEAMS MENU             ")
print("=" * 50)

available_teams = get_available_teams()

if not available_teams:
    print("❌ No teams found in the database. Exiting program.")
    exit()

# Display options to the user
for team_id, team_name in available_teams.items():
    print(f" [{team_id}] {team_name}")
print("=" * 50)

# Input Validation Loop
selected_id = None
while True:
    user_input = input("Please enter the ID of the team you want to analyze: ").strip()
    
    # 1. Check if input is a valid integer
    if not user_input.isdigit():
        print("❌ Invalid input! Please enter a numeric ID (integer only).\n")
        continue
    
    selected_id = int(user_input)
    
    # 2. Check if the ID exists in the database
    if selected_id not in available_teams:
        print(f"❌ Team ID [{selected_id}] does not exist in the database. Try again.\n")
        continue
    
    break  # Input is valid, break out of the loop

# =====================================================================
# FETCH AND PRESENT STATS
# =====================================================================
team = TeamStats(
    team_id=selected_id,
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    database=DB_CONFIG["database"]
)

print("\n" + "="*50)
print(f"ANALYSIS FOR: {available_teams[selected_id].upper()} (ID: {team.team_id})")
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