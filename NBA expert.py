import clips

DEFTEMPLATE_STRING = """
(deftemplate player
  (slot name (type STRING))
  (slot ppg (type FLOAT))
  (slot apg (type FLOAT))
  (slot rpg (type FLOAT))
  (slot team_rank (type INTEGER))
  (slot past_mvp (type INTEGER))
  (slot points (type INTEGER)))
"""

DEFRULE_STRING = """
(defrule calculate-points
  ?player <- (player (name ?name) (ppg ?ppg) (apg ?apg) (rpg ?rpg) (team_rank ?team_rank) (past_mvp ?past_mvp) (points ?points))
  =>
  (bind ?new_points 0)

  ; PPG scoring
  (if (>= ?ppg 33.9) then (bind ?new_points (+ ?new_points 10)))
  (if (and (>= ?ppg 30.4) (< ?ppg 33.9)) then (bind ?new_points (+ ?new_points 9)))
  (if (and (>= ?ppg 26.9) (< ?ppg 30.4)) then (bind ?new_points (+ ?new_points 8)))
  (if (and (>= ?ppg 26.6) (< ?ppg 26.9)) then (bind ?new_points (+ ?new_points 7)))

  ; APG scoring
  (if (>= ?apg 9.8) then (bind ?new_points (+ ?new_points 10)))
  (if (and (>= ?apg 9.0) (< ?apg 9.8)) then (bind ?new_points (+ ?new_points 9)))
  (if (and (>= ?apg 6.5) (< ?apg 9.0)) then (bind ?new_points (+ ?new_points 8)))
  (if (and (>= ?apg 6.2) (< ?apg 6.5)) then (bind ?new_points (+ ?new_points 7)))
  (if (and (>= ?apg 4.9) (< ?apg 6.2)) then (bind ?new_points (+ ?new_points 6)))

  ; RPG scoring
  (if (>= ?rpg 12.4) then (bind ?new_points (+ ?new_points 10)))
  (if (and (>= ?rpg 11.5) (< ?rpg 12.4)) then (bind ?new_points (+ ?new_points 9)))
  (if (and (>= ?rpg 9.2) (< ?rpg 11.5)) then (bind ?new_points (+ ?new_points 8)))
  (if (and (>= ?rpg 8.1) (< ?rpg 9.2)) then (bind ?new_points (+ ?new_points 7)))
  (if (and (>= ?rpg 5.6) (< ?rpg 8.1)) then (bind ?new_points (+ ?new_points 6)))

  ; Team ranking scoring
  (bind ?new_points (+ ?new_points (- 11 ?team_rank)))

  ; Past MVP scoring
  (bind ?new_points (+ ?new_points ?past_mvp))

  ; Modify points in fact
  (modify ?player (points ?new_points))
  (printout t "Player: " ?name " Points: " ?new_points crlf))
"""

environment = clips.Environment()

# define constructs
environment.build(DEFTEMPLATE_STRING)
environment.build(DEFRULE_STRING)

# retrieve the fact template
template = environment.find_template('player')

# assert new facts for each player
players = [
    {"name": "Nikola Jokic", "ppg": 26.6, "apg": 9, "rpg": 12.4, "team_rank": 3, "past_mvp": 2},
    {"name": "Shai Gilgeous Alexander", "ppg": 30.4, "apg": 6.2, "rpg": 5.6, "team_rank": 2, "past_mvp": 0},
    {"name": "Luka Doncic", "ppg": 33.9, "apg": 9.8, "rpg": 9.2, "team_rank": 6, "past_mvp": 0},
    {"name": "Giannis Antetokounmpo", "ppg": 30.4, "apg": 6.5, "rpg": 11.5, "team_rank": 8, "past_mvp": 2},
    {"name": "Jayson Tatum", "ppg": 26.9, "apg": 4.9, "rpg": 8.1, "team_rank": 1, "past_mvp": 0},
]

for player in players:
    template.assert_fact(name=player["name"],
                         ppg=float(player["ppg"]),
                         apg=float(player["apg"]),
                         rpg=float(player["rpg"]),
                         team_rank=int(player["team_rank"]),
                         past_mvp=int(player["past_mvp"]),
                         points=0)


# execute the activations in the agenda
environment.run()

# Retrieve and print the player with the highest points
facts = environment.facts()
mvp = None
max_points = -1

for fact in facts:
    if fact.template.name == 'player':
        if fact['points'] > max_points:
            max_points = fact['points']
            mvp = fact['name']

print(f"The MVP is: {mvp} with {max_points} points")
