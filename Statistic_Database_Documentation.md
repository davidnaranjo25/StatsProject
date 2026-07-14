# World Cup Predictive Engine - Database Documentation

## Philosophy

The database is the single source of truth. Raw match statistics are
stored and all model metrics are derived from them.

## Tables

### Teams

  Column          Type          Description
  --------------- ------------- -------------------
  id              INTEGER PK    Team identifier
  name            TEXT UNIQUE   Team name
  coach           TEXT          Coach
  formation       TEXT          Typical formation
  style           TEXT          High level style

### Matches

Stores one match.

Columns: - id (PK) - match_date - stage - home_team_id - away_team_id -
home_score - away_score - stadium

### TeamMatchStats

One row = one team in one match.

Core metrics: - goals - goals_against - shots - shots_on_target -
shots_inside_box - shots_outside_box - possession - passes -
accurate_passes - corners - offsides - yellow_cards - red_cards - xg -
xga - first_goal_minute - last_goal_minute - clean_sheet -
penalty_scored - penalty_conceded

### PlayerMatchStats

Stores player statistics for every match.

### TournamentTrends

Tournament-wide dynamic adjustments.

Metrics: - average_goals - average_corners - average_cards -
average_shots - average_shots_on_target - late_goals - early_goals -
penalties - own_goals - red_cards

### TeamStyle

Static tactical profile (0-100): - high_press - counter_attack -
crosses - long_ball - build_up - direct_play - wing_play - set_pieces

### ModelMetrics

Stores derived statistics: - mean - weighted_mean - trimmed_mean -
std_dev - coeff_variation - confidence

### PredictionHistory

Stores every prediction produced by the engine.

Columns: - market - predicted_probability - bookmaker_probability -
confidence - result - success - reason

## Design Rules

1.  Never overwrite raw match data.
2.  All predictive metrics are recalculated.
3.  Tournament trends never replace team data; they only adjust
    probabilities.
4.  Keep last-5 arrays available in application memory after querying
    SQL.
