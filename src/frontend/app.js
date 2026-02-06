const { createApp, ref, reactive, computed, onMounted } = Vue;

createApp({
  setup() {
    const bridge = ref(null);
    const connectionStatus = ref("Connecting...");

    const state = reactive({
      settings: {
        hints_enabled: true,
        dark_mode: false,
        color_theme: "Default Light",
        min_val: 1,
        max_val: 10,
        sfx_volume: 0.7,
        music_volume: 0.5,
        confetti_on_win: true,
        selected_bg_color: "#f0f0f0",
        current_font: "",
        chart_bar_colors: [],
      },
      game: {
        difficulty: "Easy",
        min_val: 1,
        max_val: 10,
        guesses_made: 0,
        time_trial_mode: false,
        time_remaining: 0,
        previous_guesses: [],
        power_ups: { extra_hint: 0, retry: 0, reveal_digit: 0 },
      },
      leaderboard: {
        Easy: [],
        Medium: [],
        Hard: [],
        "Time Trial": [],
      },
      achievements: {},
      stats: {},
    });

    const ui = reactive({
      view: "game",
      lastGuessMessage: "",
      aiHint: "(Request a hint)",
      aiHintLoading: false,
      leaderboardDifficulty: "Easy",
      notifications: [],
      darkMode: false,
      appStyle: {},
    });

    const forms = reactive({
      guess: null,
      difficulty: "Easy",
      minVal: 1,
      maxVal: 10,
      timeTrial: false,
      importData: "",
    });

    const showImport = ref(false);

    const leaderboardEntries = computed(() => {
      return state.leaderboard[ui.leaderboardDifficulty] || [];
    });

    const syncUiTheme = () => {
      ui.darkMode = Boolean(state.settings.dark_mode);
      ui.appStyle = {
        backgroundColor: state.settings.selected_bg_color || "#f0f0f0",
        color: ui.darkMode ? "#f0f0f0" : "#333333",
        fontFamily: state.settings.current_font || "'Segoe UI', sans-serif",
      };
    };

    const addNotification = (type, message) => {
      ui.notifications.unshift({ type, message });
      if (ui.notifications.length > 6) {
        ui.notifications.pop();
      }
    };

    const updateState = (payload) => {
      if (!payload) return;
      state.settings = { ...state.settings, ...payload.settings };
      state.game = { ...state.game, ...payload.game };
      state.leaderboard = { ...state.leaderboard, ...payload.leaderboard };
      state.achievements = payload.achievements || {};
      state.stats = payload.stats || {};
      syncUiTheme();
      forms.minVal = state.settings.min_val;
      forms.maxVal = state.settings.max_val;
      forms.difficulty = state.game.difficulty;
    };

    const connectBridge = () => {
      if (!window.qt || !window.qt.webChannelTransport) {
        connectionStatus.value = "Browser mode (no Qt bridge)";
        return;
      }

      // QWebChannel -> WebBridge
      new QWebChannel(window.qt.webChannelTransport, (channel) => {
        bridge.value = channel.objects.webBridge;
        connectionStatus.value = "Connected to Qt backend";

        bridge.value.gameStateChanged.connect(updateState);
        bridge.value.timerUpdated.connect((timeRemaining) => {
          state.game.time_remaining = timeRemaining;
        });
        bridge.value.aiHintReady.connect((hint) => {
          ui.aiHint = hint;
          ui.aiHintLoading = false;
        });
        bridge.value.aiHintLoading.connect((isLoading) => {
          ui.aiHintLoading = isLoading;
        });
        bridge.value.notification.connect((type, message) => {
          addNotification(type, message);
        });
        bridge.value.achievementUnlocked.connect((title, description, badge) => {
          addNotification("achievement", `${badge} ${title} - ${description}`);
        });

        bridge.value.get_initial_state((payload) => {
          updateState(payload);
        });
      });
    };

    // QPushButton (Guess) -> submitGuess
    const submitGuess = () => {
      if (!bridge.value) {
        addNotification("warning", "Connect the Qt backend to submit guesses.");
        return;
      }
      bridge.value.submit_guess(forms.guess, (result) => {
        if (result.status === "error") {
          ui.lastGuessMessage = result.message;
          addNotification("warning", result.message);
          return;
        }
        if (result.status === "incorrect") {
          ui.lastGuessMessage = result.message;
          addNotification("info", result.message);
          return;
        }
        ui.lastGuessMessage = "";
        forms.guess = null;
      });
    };

    // QPushButton (New Game) -> startNewGame
    const startNewGame = () => {
      if (!bridge.value) return;
      bridge.value.start_new_game(
        forms.difficulty,
        forms.minVal,
        forms.maxVal,
        forms.timeTrial,
        () => {}
      );
    };

    // QPushButton (Time Trial) -> startTimeTrial
    const startTimeTrial = () => {
      if (!bridge.value) return;
      bridge.value.start_new_game("Time Trial", forms.minVal, forms.maxVal, true, () => {});
    };

    // QPushButton (AI Hint) -> requestAiHint
    const requestAiHint = () => {
      if (!bridge.value) return;
      ui.aiHintLoading = true;
      bridge.value.request_ai_hint();
    };

    // QPushButton (Power-ups) -> usePowerUp
    const usePowerUp = (powerUp) => {
      if (!bridge.value) return;
      bridge.value.use_power_up(powerUp, () => {});
    };

    // QCheckBox/QSlider/QComboBox -> updateSetting
    const updateSetting = (key, value) => {
      if (!bridge.value) return;
      bridge.value.update_setting(key, value, () => {});
    };

    const exportSettings = () => {
      if (!bridge.value) return;
      bridge.value.export_settings((encoded) => {
        navigator.clipboard.writeText(encoded).then(
          () => addNotification("success", "Settings copied to clipboard."),
          () => addNotification("warning", "Unable to copy settings automatically.")
        );
      });
    };

    const importSettings = () => {
      if (!bridge.value) return;
      bridge.value.import_settings(forms.importData, (result) => {
        addNotification(result.success ? "success" : "warning", result.message);
        if (result.success) {
          showImport.value = false;
          forms.importData = "";
        }
      });
    };

    const resetLeaderboard = () => {
      if (!bridge.value) return;
      bridge.value.reset_leaderboard(() => {
        addNotification("info", "Leaderboard reset.");
      });
    };

    const resetAchievements = () => {
      if (!bridge.value) return;
      bridge.value.reset_achievements(() => {
        addNotification("info", "Achievements reset.");
      });
    };

    const resetStatistics = () => {
      if (!bridge.value) return;
      bridge.value.reset_statistics(() => {
        addNotification("info", "Statistics reset.");
      });
    };

    onMounted(() => {
      connectBridge();
    });

    return {
      state,
      ui,
      forms,
      showImport,
      connectionStatus,
      leaderboardEntries,
      submitGuess,
      startNewGame,
      startTimeTrial,
      requestAiHint,
      usePowerUp,
      updateSetting,
      exportSettings,
      importSettings,
      resetLeaderboard,
      resetAchievements,
      resetStatistics,
    };
  },
}).mount("#app");
