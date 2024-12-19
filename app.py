from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
import os
from src.utils.database import Database
from src.data_processing.data_cleaner import DataCleaner
from src.data_processing.feature_engineering import FeatureEngineer
from src.visualization.dashboard import Dashboard
from src.models.user import User, get_user_by_id, get_user_by_username

app = Flask(__name__, 
            template_folder='web_app/templates',
            static_folder='web_app/static')

# Set up Flask-Login with a strong secret key
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@app.route('/')
@login_required
def index():
    """Main dashboard page"""
    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', 
                         current_time=current_time,
                         username=current_user.username)  # Use username instead of id

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = get_user_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/refresh')
@login_required
def refresh():
    """Refresh dashboard data"""
    try:
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        return {
            'status': 'success',
            'timestamp': current_time,
            'username': current_user.username
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs("web_app/templates", exist_ok=True)
    os.makedirs("web_app/static/plots", exist_ok=True)
    
    app.run(debug=True)