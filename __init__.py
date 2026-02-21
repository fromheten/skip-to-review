from aqt import mw, gui_hooks
from aqt.qt import (
    QAction, QCheckBox, QComboBox, QDialog,
    QDialogButtonBox, QHBoxLayout, QLabel, QVBoxLayout, Qt,
)
from aqt.utils import showWarning


def go_to_study() -> None:
    config = mw.addonManager.getConfig(__name__)
    if not config or not config.get("enabled", True):
        return

    deck_name = config.get("deck_name", "")
    if not deck_name:
        return

    deck = mw.col.decks.by_name(deck_name)
    if not deck:
        showWarning(f"Skip to Review: deck '{deck_name}' not found.\n\nCheck the plugin settings.")
        return

    mw.col.decks.select(deck["id"])
    mw.moveToState("review")


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Skip to Review")
        self.setMinimumWidth(380)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        self.enabled_cb = QCheckBox("Automatically skip to review on startup")
        layout.addWidget(self.enabled_cb)

        deck_row = QHBoxLayout()
        deck_row.addWidget(QLabel("Deck:"))
        self.deck_combo = QComboBox()
        self.deck_combo.setMinimumWidth(220)
        deck_row.addWidget(self.deck_combo)
        layout.addLayout(deck_row)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)
        self._load()

    def _load(self) -> None:
        deck_names = sorted(d["name"] for d in mw.col.decks.all())
        self.deck_combo.addItems(deck_names)

        config = mw.addonManager.getConfig(__name__) or {}
        self.enabled_cb.setChecked(config.get("enabled", True))

        current = config.get("deck_name", "")
        idx = self.deck_combo.findText(current)
        if idx >= 0:
            self.deck_combo.setCurrentIndex(idx)

    def save(self) -> None:
        mw.addonManager.writeConfig(__name__, {
            "enabled": self.enabled_cb.isChecked(),
            "deck_name": self.deck_combo.currentText(),
        })
        self.accept()


def open_settings() -> None:
    SettingsDialog(mw).exec()


action = QAction("Skip to Review Settings…", mw)
action.triggered.connect(open_settings)
mw.form.menuTools.addAction(action)

gui_hooks.profile_did_open.append(go_to_study)
