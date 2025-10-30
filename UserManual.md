# 📘 Guess The Number: Official User Manual

---

Welcome, fellow number-cruncher! You've successfully acquired the ultimate number-guessing experience built with **PySide6**. This manual is your trusty sidekick for mastering the game, from installation to conquering the leaderboards. Get ready to challenge your intuition, track your stats, and unlock glorious achievements! 🧠✨

## 🎮 1. Introduction: What is "Guess The Number"?

**Guess The Number** is a fast-paced, feature-rich number guessing game. Your mission, should you choose to accept it, is to guess a randomly chosen secret number within a predefined range.

The game is not just about making a guess; it's about strategy! We've supercharged the classic formula with:

* Multiple difficulty levels and custom ranges.
* Optional **Time-Trial Mode** for adrenaline junkies.
* A robust **Power-Up** and **Hint System** to aid your quest.
* Detailed **Statistics** and a flashy **Achievement** tracker.
* A persistent **Leaderboard** to track your personal bests.

Good luck, and may the odds (and the numbers) be ever in your favor!

---

## 💻 2. System Requirements

Before you can dive into the guessing frenzy, make sure your system meets the basic requirements.

### Minimum Software Stack:

| Requirement | Version | Notes |
| :--- | :--- | :--- |
| **Python** | 3.10+ | The core language that powers the game. |
| **PySide6** | Latest | The powerful Qt binding for the game's stunning GUI. |
| **Matplotlib** | Latest | Used for generating historical data graphs and fancy stats! |

### 🧩 3. Installation and Setup Instructions

If you received the game as a collection of Python source files, you'll need to install the dependencies. If you have the standalone executable (`.exe`), you can skip this section!

1.  **Install Python:**
    Ensure you have Python installed and correctly configured in your system's PATH.

2.  **Install Dependencies:**
    Open your command line or terminal and run the following command to fetch all required libraries:

    ```bash
    pip install PySide6 matplotlib
    ```

3.  **Verify Setup:**
    Navigate to the game's root directory and run the main file (see next section). If the game window appears, you are all set!

---

## ▶️ 4. How to Run the Game

### Method 1: Running from Python Source

This is the standard method if you have the game's source code (`main.py`).

1.  Open your terminal/command prompt.
2.  Change your directory to the location of the `main.py` file.
3.  Execute the game with the Python interpreter:

    ```bash
    python main.py
    ```

### Method 2: Running the Standalone Executable (`.exe`)

If you have a compiled version of the game (e.g., `GuessTheNumber.exe`), simply double-click the executable file.

> ⚠️ **Note for Windows Users:** Your browser or anti-virus software might flag an unknown `.exe` file. Rest assured, this game is safe! You may need to grant an exception to run it.

---

## 🕹️ 5. Gameplay Guide

The core loop of **Guess The Number** is straightforward, but mastery takes practice!

### Step 1: Start a New Game

* Upon launch, the game will automatically generate a new secret number based on your current **Settings**.
* The range (e.g., "Guess a number between **1** and **100**") will be displayed prominently.

### Step 2: Enter Your Guess

1.  Navigate to the **Game** tab.
2.  Look for the input field (usually labeled **"Your Guess:"**).
3.  Type a whole number within the specified range.

![Gameplay](assets/gameplay.png)

### Step 3: Check and Receive Feedback

1.  Click the **`Guess!`** button.
2.  The game will tell you if your guess is:
    * **TOO HIGH:** The secret number is smaller.
    * **TOO LOW:** The secret number is larger.
    * **CORRECT!** You win!

### Step 4: Win or Continue

* If you are **CORRECT**, your score will be recorded, and you'll be prompted to start a new round. Congratulations!
* If you have remaining guesses, you'll repeat **Step 2** and **Step 3** until you run out of attempts or guess correctly.

---

## ⚙️ 6. Settings Explanation (`settings.json`)

The game's behavior is managed by the **`settings.json`** file. You can change these options directly in the in-game **Settings** menu.

| Key | Description | Type | Default Value | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `min_range` | The smallest number that can be chosen. | Integer | `1` | Affects game difficulty. |
| `max_range` | The largest number that can be chosen. | Integer | `100` | A wider range is much harder! |
| `max_guesses` | Maximum attempts per game. Set to `0` for unlimited (not recommended for leaderboard). | Integer | `10` | The core difficulty constraint. |
| `time_trial_mode` | Enables a countdown timer for guessing. | Boolean | `false` | A challenging mode for speed runners. |
| `sound_effects` | Toggle in-game sounds (clicks, win chimes, etc.). | Boolean | `true` | Enjoy the satisfying *clink* of a correct guess! |
| `theme` | UI color scheme. Common values: `dark`, `light`, `system`. | String | `dark` | Customize your look. |

---

## 🧠 7. Power-ups and Hints System

To keep the game fresh, you earn special tools for guessing streaks and achievements. Use them wisely!

| Tool/Power-Up | Effect | How to Earn |
| :--- | :--- | :--- |
| **🔍 Single Hint** | Reveals if the number is **Even** or **Odd**. | Earned after 3 consecutive wins. |
| **💡 Digit Reveal** | Reveals one of the digits of the secret number (randomly chosen). | Earned after guessing a number on your very first try. |

All available power-ups are managed in a dedicated panel, usually in the **Game** tab. Click the icon to activate!

---

## 📊 8. Statistics and Achievements

### Personal Statistics

Your journey is tracked meticulously in the **Statistics** tab. Here's what we record:

* **Total Games Played:** Your dedication is noted!
* **Total Wins/Losses:** Check your win rate.
* **Best Score (Lowest Guesses):** The record you are trying to beat.
* **Average Guesses per Win:** A measure of your efficiency.
* **Most Common Guess:** The number you've guessed the most (maybe it's a lucky number?).


### Achievements

A comprehensive list of challenges to complete! Unlocked achievements grant you badges and sometimes power-up rewards.

| Badge | Title | Requirement |
| :--- | :--- | :--- |
| ⭐ | **First Win!** | Win your very first game. |
| 🟢 | **Easy Mode Master** | Win **5 games** on Easy difficulty. |
| 🟠 | **Medium Challenger** | Win **5 games** on Medium difficulty. |
| 🔴 | **Hardcore Guesser** | Win **3 games** on Hard difficulty. |
| 🔥 | **Guessing Streak (3)** | Win **3 games in a row**. |
| 🔥🔥 | **Guessing Streak (5)** | Win **5 games in a row**. |
| ⏱️ | **Quick Thinker** | Win a **Time Trial** game. |
| ⚡ | **Power User** | Use a **power-up** for the first time. |
| 🤖 | **AI Apprentice** | Use an **AI hint** for the first time. |
| 👑 | **Ultimate Guesser** | Win a **Hard** game in **5 guesses or less**. |
| 🔥 | **Daily Streak (3)** | Win games **3 consecutive days**! |
| 🔥🔥 | **Daily Streak (7)** | Win games **7 consecutive days**! |
| 🔥🔥🔥 | **Daily Streak (30)** | Win games **30 consecutive days**! |

---

## 🧰 9. Recovery Tool Guide (`recovery.py`)

The **Guess The Number** game stores important data like your stats and achievements locally. If a power outage or a system crash corrupts these files, the main game might fail to start. This is where **`recovery.py`** saves the day!

### How to Use the Recovery Tool:

1.  Make sure the main game (**`main.py`** or **`.exe`**) is *not* running.
2.  Open your terminal/command prompt.
3.  Navigate to the directory containing **`recovery.py`**.
4.  Run the script:

    ```bash
    python recovery.py
    ```

5.  The tool will automatically:
    * **Scan** all save files for errors (invalid JSON, missing keys, etc.).
    * If no errors are found, it will safely exit.
    * If errors **are** found, it will present a dialog with the option to **Reset All Save Data**.

> 🚨 **WARNING:** Selecting **Reset All Save Data** will wipe your statistics, achievements, and leaderboard scores, restoring the files to their factory defaults. Only use this if the main game won't launch!

---

## 📂 10. Save Files Structure and Locations

Your game data is stored in five separate **`.json`** files. They are typically located in your operating system's standard application data directory:

| Operating System | Default Save Location (Example) |
| :--- | :--- |
| **Windows** | `C:\Users\<YourUser>\Documents\.GuessTheNumber\saves` |
| **macOS** | `~/Documents/.GuessTheNumber/saves` |
| **Linux** | `~/Documents/.GuessTheNumber/saves` |

### Save File Breakdown:

| File Name | Content | Managed By |
| :--- | :--- | :--- |
| `leaderboard.json` | Top scores (time/guesses) for various settings. | Leaderboard System |
| `settings.json` | Your current configuration (ranges, sound, theme, etc.). | Settings Menu |
| `game_state.json` | The current, uncompleted game's data (number, guesses left). | Core Game Engine |
| `achievements.json` | A list of all unlocked achievements and their status. | Achievement Tracker |
| `statistics.json` | Cumulative stats (Total Games, Win Rate, Averages). | Stats Tracker |

---

## ❗ 11. Error Codes Reference

Below is a complete list of possible error codes used by the **Recovery Tool (`recovery.py`)**.  
Each one describes what went wrong and how to fix it.

| Code | Description | Suggested Solution |
| :--- | :--- | :--- |
| **E-001** | `BlankGameStateError`: The game state file is empty or missing. | Launch **`recovery.py`** to auto-generate new save files. |
| **E-002** | `InvalidJSONError`: Save file cannot be read or is not valid JSON. | Use the Recovery Tool to repair or reset the affected file. |
| **E-004** | `TargetNumberCorrupt`: Target number is `0` or invalid. | Let Recovery reset your **`game_state.json`** file. |
| **E-005** | `OutOfRangeTarget`: Target number is outside the defined range. | Reconfigure min/max values in **Settings** or reset data. |
| **E-006** | `NegativeGuessesError`: The guesses count is negative. | Run **`recovery.py`** and allow file correction. |
| **E-007** | `InvalidPreviousGuesses`: Previous guesses contain non-integer or out-of-range values. | Delete **`game_state.json`** or fix using the Recovery Tool. |
| **E-008** | `PowerUpValueError`: One or more power-ups have invalid or negative values. | Reset power-up data through recovery. |
| **E-009** | `InvalidSFXVolume`: SFX volume value not between 0–1. | Open settings and correct manually or let Recovery fix it. |
| **E-010** | `InvalidMusicVolume`: Music volume value not between 0–1. | Reopen the game settings and adjust sliders. |
| **E-011** | `NegativeStatisticError`: One or more statistical counters are invalid or negative. | Run the Recovery Tool to fix corrupted statistics. |
| **E-012** | `InvalidLeaderboardEntry`: A leaderboard entry is missing required keys. | Use **Recovery** to rebuild leaderboard data. |
| **E-013** | `InvalidLeaderboardScore`: A leaderboard entry has an invalid or negative score. | Reset leaderboard via the recovery app. |
| **E-205** | `GuessOutOfRangeException`: A player’s guess is outside the configured min/max range. | Check **Settings** and ensure guesses match the range. |
| **E-300** | `DependencyError`: Missing `PySide6` or `Matplotlib`. | Reinstall using: `pip install PySide6 matplotlib` |


---

## 🪪 12. Credits and Version Info

Thank you for playing **Guess The Number**!

* **Version:** 0.3.0-prerelease
* **Developer:** G0ld Ne0
* **GUI Framework:** PySide6
* **Data Visualization:** Matplotlib
* **Special Thanks:** to the devs who make the game possible

---

## 💡 13. Extra Tips and Notes for Players

* **Binary Search is Your Friend:** The fastest way to guess a number in a range is to always guess the middle number. This method (called a binary search) guarantees the win in the minimum number of moves!
* **Leaderboard Strategy:** To get the best score, you need the **lowest number of guesses** in the **fastest time**. Practice your binary search!
* **Backup Your Saves:** If you are paranoid about losing your amazing stats, periodically make a copy of the **`GuessTheNumber`** folder mentioned in Section 10!
* **Report Bugs:** Found an issue? Report it to **respitory** so we can make the game even better!
