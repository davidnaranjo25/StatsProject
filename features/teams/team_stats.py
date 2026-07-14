# team_stats.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

class TeamStats:

    def __init__(
        self,
        team_id,
        host="localhost",
        port=3306,
        database="rawdata_teams",
        user="root",
        password=""
    ):
        self.team_id = team_id

        engine = create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
            pool_recycle=3600
        )

        Session = sessionmaker(bind=engine)
        self.session = Session()

        Base = automap_base()
        Base.prepare(autoload_with=engine)

        self.TeamMatchStats = Base.classes.teammatchstats

        # UNA SOLA CONSULTA
        self.rows = (
            self.session.query(self.TeamMatchStats)
            .filter(self.TeamMatchStats.team_id == team_id)
            .all()
        )

        self.cache = {}

    # ===================================
    # Helpers
    # ===================================
    def values(self, field):
        return [
            getattr(row, field)
            for row in self.rows
            if getattr(row, field) is not None
        ]

    def average(self, field):
        if field in self.cache:
            return self.cache[field]

        # Computed totals (goals_total, shots_total, etc.)
        if field.endswith("_total"):
            base = field.replace("_total", "")
            value = self.average_total(base)
            self.cache[field] = value
            return value

        values = self.values(field)

        if not values:
            avg = 0.0
        else:
            avg = round(sum(values) / len(values), 2)

        self.cache[field] = avg
        return avg
	
    def average_total(self, stat):
        values = self.values_total(stat)

        if not values:
            return 0.0

        return round(sum(values) / len(values), 2)
	
    def values_total(self, stat):
        totals = []

        for row in self.rows:
            stat_for = getattr(row, f"{stat}_for", None)
            stat_against = getattr(row, f"{stat}_against", None)

            if stat_for is None:
                stat_for = 0

            if stat_against is None:
                stat_against = 0

            totals.append(stat_for + stat_against)

        return totals
    
    def variance(self, stat, debug=False):
        if hasattr(self.TeamMatchStats, f"{stat}_for"):
            values = self.values(f"{stat}_for")
            average = self.average(f"{stat}_for")
            average_total = self.average_total(stat)
        else:
            values = self.values(stat)
            average = self.average(stat)
            average_total = average

        if not values or average_total == 0:
            return 0.0

        differences = [
            abs(v - average)
            for v in values
        ]

        mean_difference = sum(differences) / len(differences)

        variance = round(
            (mean_difference / average_total) * 100,
            2
        )

        if debug:
            print("\n==============================")
            print(f"DEBUG VARIANCE : {stat}")
            print("==============================")

            print("Match values:")
            print(values)

            print("\nAverage:")
            print(average)

            print("\nAverage Total:")
            print(average_total)

            print("\nDifferences:")
            print([round(v, 2) for v in differences])

            print("\nMean Difference:")
            print(round(mean_difference, 2))

            print("\nVariance:")
            print(f"{variance}%")

        return variance

    def classify(stat,value):

    match stat:

        case "corners":

            if value<=6:
                return "LOW"

            elif value<=10:
                return "MEDIUM"

            return "HIGH"

        case "shots":

            if value<12:
                return "LOW"

            elif value<20:
                return "MEDIUM"

            return "HIGH"

        case "shots_on_target":

            if value<=5:
                return "LOW"

            elif value<=10:
                return "MEDIUM"

            return "HIGH"

        case "cards":

            if value<=1:
                return "LOW"

            elif value<=3:
                return "MEDIUM"

            return "HIGH"

        case "goal_margin":

            if value<1:
                return "LOW"

            elif value<2:
                return "MEDIUM"

            return "HIGH"


    def matches(self):

        return len(self.rows)

    # ===================================
    # Estadísticas resumidas
    # ===================================
def summary(self):

    return {

        "matches": self.matches(),

        # ---------------- Goals ----------------

        "goals_for": self.average("goals_for"),
        "goals_against": self.average("goals_against"),
        "goals_total": self.average("goals_total"),

        # ---------------- Shots ----------------

        "shots_for": self.average("shots_for"),
        "shots_against": self.average("shots_against"),
        "shots_total": self.average("shots_total"),

        # -------- Shots On Target --------

        "shots_on_target_for":
            self.average("shots_on_target_for"),

        "shots_on_target_against":
            self.average("shots_on_target_against"),

        "shots_on_target_total":
            self.average("shots_on_target_total"),

        # ---------------- Corners ----------------

        "corners_for":
            self.average("corners_for"),

        "corners_against":
            self.average("corners_against"),

        "corners_total":
            self.average("corners_total"),

        # ---------------- Offsides ----------------

        "offsides":
            self.average("offsides"),

        # ---------------- Cards ----------------

        "yellow_cards":
            self.average("yellow_cards"),

        "red_cards":
            self.average("red_cards"),

        # ---------------- xG ----------------

        "xg":
            self.average("xg"),

        "xga":
            self.average("xga"),

        # ---------------- Goal Timing ----------------

        "first_goal_minute":
            self.average("first_goal_minute"),

        "last_goal_minute":
            self.average("last_goal_minute")
    }



    def close(self):
        self.session.close()