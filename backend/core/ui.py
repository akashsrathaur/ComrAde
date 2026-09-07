import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QRadialGradient, QPen, QBrush

class UltronUI(QWidget):
    def __init__(self):
        super().__init__()
        # Set frameless, transparent, and always-on-top window flags (Removed Tool flag for macOS visibility)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.resize(300, 300)
        
        # Position in the exact center of the screen so it's impossible to miss!
        screen = QApplication.primaryScreen().geometry()
        self.move((screen.width() - 300) // 2, (screen.height() - 300) // 2)
        
        self.state = "SLEEPING"
        self.pulse_radius = 50
        self.pulse_growing = True
        
        # Animation timer (30 FPS)
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)
        
        # Layout for status text underneath the orb
        layout = QVBoxLayout()
        self.status_label = QLabel("Sleeping...")
        self.status_label.setStyleSheet("color: #ff3333; font-family: 'Courier New'; font-size: 16px; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        
        # Always show UI
        self.show()

    def update_state(self, new_state: str, message: str = ""):
        self.state = new_state
        self.show() # Ensure it's never hidden
        self.raise_()
        self.activateWindow()
        
        if new_state == "SLEEPING":
            self.status_label.setText("Sleeping...")
        else:
            self.status_label.setText(message)
            
    def animate(self):
        if self.state == "SLEEPING":
            return
            
        # Different pulsing speeds based on state
        speed = 1.5 if self.state == "LISTENING" else (4 if self.state == "SPEAKING" else 2)
        
        if self.pulse_growing:
            self.pulse_radius += speed
            if self.pulse_radius > 110:
                self.pulse_growing = False
        else:
            self.pulse_radius -= speed
            if self.pulse_radius < 50:
                self.pulse_growing = True
                
        self.update() # Triggers paintEvent

    def paintEvent(self, event):
        if self.state == "SLEEPING":
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center_x = self.width() / 2
        center_y = self.height() / 2
        
        # Ultron Colors: Menacing Red
        core_color = QColor(255, 0, 0, 255)
        if self.state == "THINKING":
            core_color = QColor(255, 80, 0, 255) # Orange-red for thinking
        elif self.state == "SPEAKING":
            core_color = QColor(255, 0, 100, 255) # Bright red/pink
            
        # 1. Draw the glowing aura (gradient)
        gradient = QRadialGradient(QPointF(center_x, center_y), self.pulse_radius)
        gradient.setColorAt(0, core_color)
        gradient.setColorAt(0.6, QColor(100, 0, 0, 150))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(center_x, center_y), self.pulse_radius, self.pulse_radius)
        
        # 2. Draw outer silver mechanical rings
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(QColor(192, 192, 192, 200)) # Silver
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawEllipse(QPointF(center_x, center_y), self.pulse_radius + 5, self.pulse_radius + 5)
        
        # 3. Draw inner bright core
        painter.setBrush(QColor(255, 200, 200, 255))
        painter.drawEllipse(QPointF(center_x, center_y), 15, 15)
