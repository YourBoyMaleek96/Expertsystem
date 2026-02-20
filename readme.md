# 🏀 NBA MVP Expert System

## Project Overview

This project is an **Expert System** built using **CLIPS** and **Python** with a **Tkinter GUI** to predict NBA Most Valuable Player (MVP) rankings based on player statistics.  

It demonstrates the use of **rule-based reasoning** to make decisions, mimicking how a human expert might weigh different factors when evaluating player performance.

**Technologies Used:**

- Python 3.12 – main programming language  
- CLIPS – rule-based expert system engine  
- Tkinter – GUI framework  
- Pillow – image handling in the GUI  

---

## Project Description

The system evaluates NBA players using the following inputs:

| Input         | Description                                   |
|---------------|-----------------------------------------------|
| PPG           | Points per Game                                |
| APG           | Assists per Game                               |
| RPG           | Rebounds per Game                              |
| Team Rank     | Current team ranking in the NBA season        |
| Past MVP      | Number of previous MVP awards                  |

The program calculates a **point score** for each player based on a set of rules, and ranks them accordingly. The GUI displays the players’ images, names, total points, and allows the user to view detailed stats for each player.

---

## Rule System

The expert system uses **CLIPS rules** to assign points based on player performance:

### 1. PPG (Points Per Game) Rules

| PPG Range          | Points |
|-------------------|--------|
| ≥ 33.9            | 10     |
| 30.4 – 33.8       | 9      |
| 26.9 – 30.3       | 8      |
| 26.6 – 26.8       | 7      |

### 2. APG (Assists Per Game) Rules

| APG Range          | Points |
|-------------------|--------|
| ≥ 9.8             | 10     |
| 9.0 – 9.7         | 9      |
| 6.5 – 8.9         | 8      |
| 6.2 – 6.4         | 7      |
| 4.9 – 6.1         | 6      |

### 3. RPG (Rebounds Per Game) Rules

| RPG Range          | Points |
|-------------------|--------|
| ≥ 12.4            | 10     |
| 11.5 – 12.3       | 9      |
| 9.2 – 11.4        | 8      |
| 8.1 – 9.1         | 7      |
| 5.6 – 8.0         | 6      |

### 4. Team Rank Contribution

- Formula: `11 - Team Rank`  
- Rewards players on higher-ranked teams

### 5. Past MVP Awards

- Each previous MVP adds **1 point** to the player’s total

---

## How It Works

1. Player facts are created in **CLIPS**.  
2. The **rules engine** evaluates each player’s stats.  
3. Each rule assigns points based on performance thresholds.  
4. Total points are calculated and updated for each player.  
5. The **GUI** ranks players by points and displays images, names, and stats.

---

## Discussion

- Demonstrates how **rule-based AI** can model expert decision-making.  
- The scoring system is **interpretable**, unlike neural networks — you can trace exactly why a player scored a certain number of points.  
- Limitations: Rules are simplified; advanced metrics like PER, defensive impact, or injuries are not included.  
- Future Improvements:  
  - Integrate advanced statistics (PER, Win Shares, etc.)  
  - Allow user-defined rules dynamically  
  - Incorporate historical data for trend analysis  

---

## Usage Instructions

1. Ensure **Python 3.12** is installed.  
2. Install dependencies:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install pillow clips