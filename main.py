from flask import redirect, render_template, url_for, current_app
from dotenv import load_dotenv
from api import create_app, db
import os

# Load environment variables from .env file
# load_dotenv()

# Use "development" as fallback
app = create_app(os.getenv("FLASK_ENV", "development")) 
print("SQLALCHEMY_DATABASE_URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))
# default routes, not related to endpoints (TODO maybe should move to routes.py)
@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def api_landing():
    return redirect(url_for("app.home")) 

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, host='0.0.0.0', port=80)
