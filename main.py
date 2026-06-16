import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QStackedWidget
from auth.login import LoginScreen
from auth.signup import SignupScreen
from gui.dashboard import DashboardScreen

class MainController(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skeleton-Based Fall Detection System")
        self.resize(1000, 700)
        
        # Initialize Screens
        self.login_screen = LoginScreen()
        self.signup_screen = SignupScreen()
        self.dashboard_screen = DashboardScreen()
        
        # Add to Stack
        self.addWidget(self.login_screen)
        self.addWidget(self.signup_screen)
        self.addWidget(self.dashboard_screen)
        
        # Connections
        self.login_screen.login_successful.connect(self.show_dashboard)
        self.login_screen.go_to_signup.connect(self.show_signup)
        
        self.signup_screen.go_to_login.connect(self.show_login)
        
        self.dashboard_screen.logout_requested.connect(self.show_login)
        
        # Start at login
        self.setCurrentWidget(self.login_screen)
        
    def show_login(self):
        self.setCurrentWidget(self.login_screen)
        
    def show_signup(self):
        self.setCurrentWidget(self.signup_screen)
        
    def show_dashboard(self, username):
        self.dashboard_screen.update_username(username)
        self.setCurrentWidget(self.dashboard_screen)

def main():
    # Ensure necessary folders exist
    os.makedirs('ml', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Check if model exists, if not, try to generate it
    if not os.path.exists('ml/model.pkl'):
        print("Model not found. Attempting to generate synthetic model...")
        try:
            from ml.generate_model import generate_synthetic_model
            generate_synthetic_model()
        except ImportError as e:
            print(f"Could not generate model automatically: {e}")
            print("Please ensure dependencies are installed correctly.")

    app = QApplication(sys.argv)
    
    # Apply global stylesheet
    from utils.styles import GLOBAL_QSS
    app.setStyleSheet(GLOBAL_QSS)
    
    controller = MainController()
    controller.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
