# Web Frontend Backend Runner

## Run the Qt + Vue app

1. Install dependencies (PySide6 with WebEngine support).
2. From the repo root, run:

```bash
python src/backend/main.py
```

This launches a `QWebEngineView` that loads the Vue frontend from `src/frontend/index.html` and connects to the Python backend using Qt WebChannel.

## Browser-only mode

You can open `src/frontend/index.html` directly in a browser for a static preview, but backend features (game logic, save files, AI hints, etc.) require the Qt WebBridge connection.
