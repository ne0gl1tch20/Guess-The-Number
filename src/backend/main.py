import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

from webbridge import WebBridge, game_module


def main():
    """Run the Qt backend with a QWebEngineView hosting the Vue frontend."""
    app = QApplication(sys.argv)

    root_dir = Path(__file__).resolve().parents[2]
    frontend_path = root_dir / "src" / "frontend" / "index.html"
    icon_path = root_dir / "src" / "data" / "icon.ico"

    window = QMainWindow()
    window.setWindowTitle("Supercharged Number Guessing Game")
    window.setMinimumSize(1024, 720)
    if icon_path.exists():
        window.setWindowIcon(QIcon(str(icon_path)))

    view = QWebEngineView()
    window.setCentralWidget(view)

    sound_service = game_module.SoundManager(window)
    settings_service = game_module.SettingsService(sound_service)
    leaderboard_service = game_module.LeaderboardService()
    stats_service = game_module.StatisticsService()
    achievement_service = game_module.AchievementService(sound_service)
    game_service = game_module.GameService(
        settings_service,
        leaderboard_service,
        achievement_service,
        stats_service,
        sound_service,
    )

    stats_service.refresh_daily_streak()
    achievement_service.start_daily_streak_timer()

    bridge = WebBridge(
        settings_service,
        leaderboard_service,
        achievement_service,
        stats_service,
        sound_service,
        game_service,
    )

    channel = QWebChannel()
    channel.registerObject("webBridge", bridge)
    view.page().setWebChannel(channel)

    view.load(QUrl.fromLocalFile(str(frontend_path)))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
