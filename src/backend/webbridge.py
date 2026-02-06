import importlib.util
import random
from pathlib import Path

from PySide6.QtCore import QObject, Signal, Slot

ROOT_DIR = Path(__file__).resolve().parents[2]
GAME_MODULE_PATH = ROOT_DIR / "src" / "scripts" / "main.py"

spec = importlib.util.spec_from_file_location("guess_the_number_game", GAME_MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load game module from {GAME_MODULE_PATH}")

game_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game_module)


class WebBridge(QObject):
    """Qt WebChannel bridge exposing backend services to the Vue frontend."""

    gameStateChanged = Signal(dict)
    timerUpdated = Signal(int)
    aiHintReady = Signal(str)
    aiHintLoading = Signal(bool)
    notification = Signal(str, str)
    achievementUnlocked = Signal(str, str, str)

    def __init__(self, settings_service, leaderboard_service, achievement_service, statistics_service, sound_manager, game_service):
        super().__init__()
        self.settings_service = settings_service
        self.leaderboard_service = leaderboard_service
        self.achievement_service = achievement_service
        self.statistics_service = statistics_service
        self.sound_manager = sound_manager
        self.game_service = game_service

        self.game_service.game_state_changed.connect(self._emit_game_state)
        self.game_service.timer_update.connect(self.timerUpdated.emit)
        self.game_service.ai_hint_ready.connect(self.aiHintReady.emit)
        self.game_service.ai_hint_loading.connect(self.aiHintLoading.emit)
        self.game_service.game_over.connect(self._handle_game_over)
        self.achievement_service.achievement_unlocked.connect(self.achievementUnlocked.emit)

        if self.game_service.target_number == 0:
            self.game_service.start_new_game(
                self.game_service.difficulty,
                self.settings_service.get_setting("min_val"),
                self.settings_service.get_setting("max_val"),
            )

    def _build_state(self):
        return {
            "settings": self.settings_service.settings,
            "game": {
                "difficulty": self.game_service.difficulty,
                "min_val": self.game_service.min_val,
                "max_val": self.game_service.max_val,
                "guesses_made": self.game_service.guesses_made,
                "time_trial_mode": self.game_service.time_trial_mode,
                "time_remaining": self.game_service.time_remaining,
                "previous_guesses": self.game_service.previous_guesses,
                "power_ups": self.game_service.power_ups,
            },
            "leaderboard": {
                "Easy": self.leaderboard_service.get_all_scores("Easy"),
                "Medium": self.leaderboard_service.get_all_scores("Medium"),
                "Hard": self.leaderboard_service.get_all_scores("Hard"),
                "Time Trial": self.leaderboard_service.get_all_scores("Time Trial"),
            },
            "achievements": self.achievement_service.get_all_achievements(),
            "stats": self.statistics_service.get_stats(),
        }

    def _emit_game_state(self):
        self.gameStateChanged.emit(self._build_state())

    def _check_and_unlock_achievements(self, stats):
        achievements = self.game_service.achievements.get_all_achievements()
        conditions = {
            "First Win!": stats.get("total_wins", 0) >= 1,
            "Easy Mode Master": stats.get("wins_easy", 0) >= 5,
            "Medium Challenger": stats.get("wins_medium", 0) >= 5,
            "Hardcore Guesser": stats.get("wins_hard", 0) >= 3,
            "Guessing Streak (3)": stats.get("current_streak", 0) >= 3,
            "Guessing Streak (5)": stats.get("current_streak", 0) >= 5,
            "Quick Thinker": stats.get("time_trial_wins", 0) >= 1,
            "Power User": stats.get("powerups_used", 0) >= 1,
            "AI Apprentice": stats.get("ai_hints_used", 0) >= 1,
            "Ultimate Guesser": stats.get("hard_five_guess_wins", 0) >= 1,
        }

        for key, condition_met in conditions.items():
            if key in achievements and not achievements[key]["unlocked"] and condition_met:
                achievements[key]["unlocked"] = True
                self.game_service.achievements.save_achievements()
                if self.game_service.sound_manager:
                    self.game_service.sound_manager.play_sfx("achievement_unlock")
                self.game_service.achievements.achievement_unlocked.emit(
                    key,
                    achievements[key]["description"],
                    achievements[key]["badge"],
                )

    def _handle_game_over(self, won, guesses, time_taken):
        stats = self.game_service.stats.get_stats()

        if won:
            message = random.choice(game_module.WIN_MESSAGES) + f"\nYou guessed it in {guesses} tries!"
            if self.game_service.time_trial_mode:
                message += f" Time: {time_taken:.2f}s."
            self.notification.emit("success", message)

            stats["total_wins"] = stats.get("total_wins", 0) + 1
            stats[f"wins_{self.game_service.difficulty.lower()}"] = stats.get(
                f"wins_{self.game_service.difficulty.lower()}",
                0,
            ) + 1
            stats["current_streak"] = stats.get("current_streak", 0) + 1
            stats["max_streak"] = max(stats.get("max_streak", 0), stats["current_streak"])
            if self.game_service.difficulty == "Hard" and guesses <= 5:
                stats["hard_five_guess_wins"] = stats.get("hard_five_guess_wins", 0) + 1

            self.game_service.stats.set_stats(stats)
            self.game_service.stats.save_stats()

            self._check_and_unlock_achievements(stats)

            self.statistics_service.increment("total_wins")
            self.statistics_service.update_streak(True)
            self.statistics_service.update_daily_streak(True)

            reward_powerup = random.choice(["extra_hint", "retry", "reveal_digit"])
            self.game_service.add_power_up(reward_powerup)
            self.notification.emit(
                "reward",
                f"You won a {reward_powerup.replace('_', ' ').title()} power-up!",
            )
            daily_streak = self.statistics_service.get_stats().get("daily_streak", 0)
            self.notification.emit("info", f"Your current daily streak: {daily_streak} 🔥")
        else:
            message = random.choice(game_module.LOSE_MESSAGES) + f"\nThe number was {self.game_service.target_number}."
            self.notification.emit("warning", message)

            stats["total_losses"] = stats.get("total_losses", 0) + 1
            stats["current_streak"] = 0
            self.game_service.stats.set_stats(stats)
            self.game_service.stats.save_stats()

            self._check_and_unlock_achievements(stats)
            self.statistics_service.increment("total_losses")
            self.statistics_service.update_streak(False)

        self.game_service.clear_saved_game_state()
        self.game_service.start_new_game(self.game_service.difficulty)
        self._emit_game_state()

    @Slot(result=dict)
    def get_initial_state(self):
        return self._build_state()

    @Slot(str, int, int, bool, result=dict)
    def start_new_game(self, difficulty, min_val, max_val, time_trial):
        self.game_service.start_new_game(difficulty, min_val, max_val, time_trial)
        self._emit_game_state()
        return {"status": "ok"}

    @Slot(int, result=dict)
    def submit_guess(self, guess):
        try:
            guess = int(guess)
        except (TypeError, ValueError):
            self.sound_manager.play_sfx("incorrect_guess")
            return {"status": "error", "message": "Please enter a valid number! ⚠️"}

        if not (self.game_service.min_val <= guess <= self.game_service.max_val):
            return {
                "status": "error",
                "message": f"Please enter a number between {self.game_service.min_val} and {self.game_service.max_val}!",
            }

        result = self.game_service.check_guess(guess)
        if result == "correct":
            return {"status": "correct"}

        msg = random.choice(game_module.INCORRECT_MESSAGES)
        if self.settings_service.get_setting("hints_enabled"):
            msg += " 🔺 Too low!" if result == "too_low" else " 🔻 Too high!"
        return {"status": "incorrect", "message": msg}

    @Slot()
    def request_ai_hint(self):
        self.game_service.request_ai_hint()

    @Slot(str, result=dict)
    def use_power_up(self, power_up_type):
        success = self.game_service.use_power_up(power_up_type)
        self._emit_game_state()
        return {"status": "ok" if success else "error"}

    @Slot(str, result=list)
    def get_leaderboard(self, difficulty):
        return self.leaderboard_service.get_all_scores(difficulty)

    @Slot(result=dict)
    def get_achievements(self):
        return self.achievement_service.get_all_achievements()

    @Slot(result=dict)
    def get_stats(self):
        return self.statistics_service.get_stats()

    @Slot(result=bool)
    def reset_leaderboard(self):
        self.leaderboard_service.reset_leaderboard()
        self._emit_game_state()
        return True

    @Slot(result=bool)
    def reset_achievements(self):
        self.achievement_service.reset_achievements()
        self._emit_game_state()
        return True

    @Slot(result=bool)
    def reset_statistics(self):
        self.statistics_service.reset_stats()
        self._emit_game_state()
        return True

    @Slot(str, object, result=bool)
    def update_setting(self, key, value):
        self.settings_service.set_setting(key, value)
        self._emit_game_state()
        return True

    @Slot(result=str)
    def export_settings(self):
        return self.settings_service.export_settings()

    @Slot(str, result=dict)
    def import_settings(self, encoded_str):
        success, message = self.settings_service.import_settings(encoded_str)
        if success:
            self._emit_game_state()
        return {"success": success, "message": message}
