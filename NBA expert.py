import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import clips

# Define the CLIPS environment and rules
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
  ?player <- (player (name ?name) (ppg ?ppg) (apg ?apg) (rpg ?rpg) (team_rank ?team_rank) (past_mvp ?past_mvp) (points 0))
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

# Initialize the CLIPS environment
environment = clips.Environment()

# Define constructs
environment.build(DEFTEMPLATE_STRING)
environment.build(DEFRULE_STRING)

# Retrieve the fact template
template = environment.find_template('player')

# Sample player data with images
players = [
    {"name": "Nikola Jokic", "ppg": 26.6, "apg": 9, "rpg": 12.4, "team_rank": 3, "past_mvp": 2, "image": "Nikola Jokic.jpg"},
    {"name": "Shai Gilgeous Alexander", "ppg": 30.4, "apg": 6.2, "rpg": 5.6, "team_rank": 2, "past_mvp": 0, "image": "Shai Alexander.jpg"},
    {"name": "Luka Doncic", "ppg": 33.9, "apg": 9.8, "rpg": 9.2, "team_rank": 6, "past_mvp": 0, "image": "Luka Donic.jpg"},
    {"name": "Giannis Antetokounmpo", "ppg": 30.4, "apg": 6.5, "rpg": 11.5, "team_rank": 8, "past_mvp": 2, "image": "Giannis Antetokounmpo.jpg"},
    {"name": "Jayson Tatum", "ppg": 26.9, "apg": 4.9, "rpg": 8.1, "team_rank": 1, "past_mvp": 0, "image": "Jayson Tatum.jpg"},
]

# Assert new facts for each player
for player in players:
    template.assert_fact(name=player["name"],
                         ppg=float(player["ppg"]),
                         apg=float(player["apg"]),
                         rpg=float(player["rpg"]),
                         team_rank=int(player["team_rank"]),
                         past_mvp=int(player["past_mvp"]),
                         points=0)

# Execute the activations in the agenda
environment.run()

# Retrieve and sort players by points
facts = [fact for fact in environment.facts() if fact.template.name == 'player']
sorted_facts = sorted(facts, key=lambda x: x['points'], reverse=True)

class PlayerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NBA MVP Player Rankings")
        self.geometry("600x800")
        self.player_data = {player["name"]: player for player in players}  # Store player data with images
        self.create_widgets()

    def create_widgets(self):
        for i, fact in enumerate(sorted_facts):
            frame = ttk.Frame(self)
            frame.pack(fill=tk.BOTH, expand=True, pady=10)

            # Load and display the player's image
            player = self.player_data[fact['name']]
            img = Image.open(player['image'])
            img = img.resize((100, 100), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to the image
            img_label.grid(row=0, column=0, rowspan=2)

            # Display the player's name and points
            name_label = tk.Label(frame, text=f"{i + 1}. {fact['name']}", font=("Arial", 16))
            name_label.grid(row=0, column=1, sticky=tk.W)
            points_label = tk.Label(frame, text=f"Points: {fact['points']}", font=("Arial", 12))
            points_label.grid(row=1, column=1, sticky=tk.W)

            # Add the "View Stats" button
            stats_button = ttk.Button(frame, text="View Stats", command=lambda fact=fact: self.show_stats(fact))
            stats_button.grid(row=0, column=2, rowspan=2, padx=10)

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

if __name__ == "__main__":
    app = PlayerGUI()
    app.mainloop()
