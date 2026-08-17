THEMES = {
    "Ciemny": {"bg": "#0f1520", "panel": "#161f2c", "surface": "#22304a", "accent": "#7b9cff", "text": "#f5f9ff", "muted": "#9caccd"},
    "Jasny": {"bg": "#f4f7fc", "panel": "#ffffff", "surface": "#e6ebf5", "accent": "#4e68dc", "text": "#172033", "muted": "#6b7a92"},
}


def stylesheet(theme="Ciemny"):
    c = THEMES.get(theme, THEMES["Ciemny"])
    return f'''
        QMainWindow, QWidget {{ background: {c["bg"]}; color: {c["text"]}; font-family: "Segoe UI", "Calibri", sans-serif; font-size: 14px; }}
        QLabel[role="muted"] {{ color: {c["muted"]}; }}
        QFrame[card="true"] {{ background: {c["panel"]}; border: 1px solid {c["surface"]}; border-radius: 16px; }}
        QFrame[panel="true"] {{ background: {c["surface"]}; border-radius: 14px; }}
        QPushButton {{ background: {c["surface"]}; color: {c["text"]}; border: none; border-radius: 12px; padding: 11px 18px; font-weight: 600; }}
        QPushButton:hover {{ background: {c["accent"]}; color: white; }}
        QPushButton:disabled {{ background: #566074; color: #d5d9e2; }}
        QPushButton[primary="true"] {{ background: {c["accent"]}; color: white; padding: 13px 20px; font-size: 15px; }}
        QPushButton[small="true"] {{ padding: 8px 12px; font-size: 13px; }}
        QLineEdit, QComboBox, QSpinBox, QListWidget, QTextEdit {{ background: {c["surface"]}; border: 1px solid {c["surface"]}; border-radius: 12px; padding: 8px; selection-background-color: {c["accent"]}; selection-color: white; }}
        QSlider::groove:horizontal {{ height: 8px; background: {c["panel"]}; border-radius: 4px; }}
        QSlider::handle:horizontal {{ width: 18px; background: {c["accent"]}; border-radius: 9px; margin: -5px 0; }}
        QProgressBar {{ border: none; border-radius: 10px; background: {c["surface"]}; min-height: 14px; }}
        QProgressBar::chunk {{ background: {c["accent"]}; border-radius: 10px; }}
        QListWidget {{ padding: 6px; }}
        QComboBox {{ min-height: 36px; }}
    '''
