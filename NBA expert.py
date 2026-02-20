# ===============================
# IMPORTS
# ===============================

# Tkinter for GUI
import tkinter as tk
from tkinter import ttk

# Pillow (PIL) for loading and resizing player images
from PIL import Image, ImageTk

# CLIPS Python binding for rule-based expert system
import clips


# ==========================================================
# CLIPS EXPERT SYSTEM DEFINITIONS
# ==========================================================

# ----------------------------------------------------------
# DEFTEMPLATE
# Defines the structure of a "player" fact in working memory.
# This acts like a class definition for facts.
#
# Each player will have:
# - name        : Player name (STRING)
# - ppg         : Points per game (FLOAT)
# - apg         : Assists per game (FLOAT)
# - rpg         : Rebounds per game (FLOAT)
# - team_rank   : Team standing in conference (INTEGER)
# - past_mvp    : Number of MVP awards won (INTEGER)
# - points      : Computed MVP score from rule engine (INTEGER)
# ----------------------------------------------------------

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


# ----------------------------------------------------------
# DEFRULE
# This rule calculates a weighted MVP score.
#
# When a player fact with points = 0 is found,
# the rule fires and computes a new MVP score.
#
# The rule uses:
# - Statistical thresholds (PPG, APG, RPG)
# - Team success factor
# - Historical MVP bias
#
# Then it modifies the fact in working memory.
# ----------------------------------------------------------

DEFRULE_STRING = """
(defrule calculate-points
  ?player <- (player (name ?name) (ppg ?ppg) (apg ?apg) (rpg ?rpg) (team_rank ?team_rank) (past_mvp ?past_mvp) (points 0))
  =>
  (bind ?new_points 0)

  ; -----------------------
  ; PPG scoring
  ; -----------------------
  ; Elite scoring gets higher weights
  (if (>= ?ppg 33.9) then (bind ?new_points (+ ?new_points 10)))
  (if (and (>= ?ppg 30.4) (< ?ppg 33.9)) then (bind ?new_points (+ ?new_points 9)))
  (if (and (>= ?ppg 26.9) (< ?ppg 30.4)) then (bind ?new_points (+ ?new_points 8)))
  (if (and (>= ?ppg 26.6) (< ?ppg 26.9)) then (bind ?new_points (+ ?new_points 7)))

  ; -----------------------
  ; APG scoring
  ; -----------------------
  (if (>= ?apg 9.8) then (bind ?new_points (+ ?new_points 10)))
  (if (and (>= ?apg 9.0) (< ?apg 9.8)) then (bind ?new_points (+ ?new_points 9)))
  (if (and (>= ?apg 6.5) (< ?apg 9.0)) then (bind ?new_points (+ ?new_points 8)))
  (if (and (>= ?apg 6.2) (< ?apg 6.5)) then (bind ?new_points (+ ?new_points 7)))
  (if (and (>= ?apg 4.9) (< ?apg 6.2)) then (bind ?new_points (+ ?new_points 6)))

  ; -----------------------
  ; RPG scoring
  ; -----------------------
  (if (>= ?rpg 12.4) then (bind ?new_points (+ ?new_points 10)))
  (if (and (>= ?rpg 11.5) (< ?rpg 12.4)) then (bind ?new_points (+ ?new_points 9)))
  (if (and (>= ?rpg 9.2) (< ?rpg 11.5)) then (bind ?new_points (+ ?new_points 8)))
  (if (and (>= ?rpg 8.1) (< ?rpg 9.2)) then (bind ?new_points (+ ?new_points 7)))
  (if (and (>= ?rpg 5.6) (< ?rpg 8.1)) then (bind ?new_points (+ ?new_points 6)))

  ; -----------------------
  ; Team ranking scoring
  ; Higher ranked teams contribute more.
  ; Example: Rank 1 gets +10, Rank 10 gets +1
  ; -----------------------
  (bind ?new_points (+ ?new_points (- 11 ?team_rank)))

  ; -----------------------
  ; Past MVP bonus
  ; Adds historical credibility factor
  ; -----------------------
  (bind ?new_points (+ ?new_points ?past_mvp))

  ; Update fact in working memory
  (modify ?player (points ?new_points))

  ; Debug output to console
  (printout t "Player: " ?name " Points: " ?new_points crlf))
"""


# ==========================================================
# INITIALIZE CLIPS ENVIRONMENT
# ==========================================================

# Create the inference engine environment
environment = clips.Environment()

# Load template and rule into engine
environment.build(DEFTEMPLATE_STRING)
environment.build(DEFRULE_STRING)

# Get reference to player template
template = environment.find_template('player')


# ==========================================================
# SAMPLE PLAYER DATA (Knowledge Base Input)
# ==========================================================

# This acts as the "facts" inserted into working memory
players = [
    {"name": "Nikola Jokic", "ppg": 26.6, "apg": 9, "rpg": 12.4, "team_rank": 3, "past_mvp": 2, "image": "Nikola Jokic.jpg"},
    {"name": "Shai Gilgeous Alexander", "ppg": 30.4, "apg": 6.2, "rpg": 5.6, "team_rank": 2, "past_mvp": 0, "image": "Shai Alexander.jpg"},
    {"name": "Luka Doncic", "ppg": 33.9, "apg": 9.8, "rpg": 9.2, "team_rank": 6, "past_mvp": 0, "image": "Luka Donic.jpg"},
    {"name": "Giannis Antetokounmpo", "ppg": 30.4, "apg": 6.5, "rpg": 11.5, "team_rank": 8, "past_mvp": 2, "image": "Giannis Antetokounmpo.jpg"},
    {"name": "Jayson Tatum", "ppg": 26.9, "apg": 4.9, "rpg": 8.1, "team_rank": 1, "past_mvp": 0, "image": "Jayson Tatum.jpg"},
]

# Insert each player as a fact into working memory
for player in players:
    template.assert_fact(
        name=player["name"],
        ppg=float(player["ppg"]),
        apg=float(player["apg"]),
        rpg=float(player["rpg"]),
        team_rank=int(player["team_rank"]),
        past_mvp=int(player["past_mvp"]),
        points=0  # initialize before rule fires
    )

# Run forward-chaining inference engine
environment.run()


# ==========================================================
# SORT RESULTS
# ==========================================================

# Extract player facts after rule execution
facts = [fact for fact in environment.facts() if fact.template.name == 'player']

# Sort by calculated MVP points descending
sorted_facts = sorted(facts, key=lambda x: x['points'], reverse=True)


# ==========================================================
# GUI IMPLEMENTATION
# ==========================================================

class PlayerGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("NBA MVP Player Rankings")
        self.geometry("600x800")

        # Dictionary for mapping player names to images
        self.player_data = {player["name"]: player for player in players}

        self.create_widgets()

    def create_widgets(self):

        # Loop through sorted results
        for i, fact in enumerate(sorted_facts):

            frame = ttk.Frame(self)
            frame.pack(fill=tk.BOTH, expand=True, pady=10)

            # Load and resize image
            player = self.player_data[fact['name']]
            img = Image.open(player['image'])
            img = img.resize((100, 100), Image.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)

            img_label = tk.Label(frame, image=img_tk)
            img_label.image = img_tk  # Prevent garbage collection
            img_label.grid(row=0, column=0, rowspan=2)

            # Player ranking and name
            name_label = tk.Label(
                frame,
                text=f"{i + 1}. {fact['name']}",
                font=("Arial", 16)
            )
            name_label.grid(row=0, column=1, sticky=tk.W)

            # MVP score
            points_label = tk.Label(
                frame,
                text=f"Points: {fact['points']}",
                font=("Arial", 12)
            )
            points_label.grid(row=1, column=1, sticky=tk.W)

            # View Stats Button
            stats_button = ttk.Button(
                frame,
                text="View Stats",
                command=lambda fact=fact: self.show_stats(fact)
            )
            stats_button.grid(row=0, column=2, rowspan=2, padx=10)

    # Opens detailed stats window
    def show_stats(self, fact):

        stats_window = tk.Toplevel(self)
        stats_window.title(f"Stats for {fact['name']}")

        stats = f"""
        Name: {fact['name']}
        PPG: {fact['ppg']}
        APG: {fact['apg']}
        RPG: {fact['rpg']}
        Team Rank: {fact['team_rank']}
        Past MVPs: {fact['past_mvp']}
        Points: {fact['points']}
        """

        stats_label = tk.Label(stats_window, text=stats, font=("Arial", 12))
        stats_label.pack()


# ==========================================================
# APPLICATION ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    app = PlayerGUI()
    app.mainloop()