from flask import redirect, render_template, url_for, current_app
from dotenv import load_dotenv
from api import create_app, db

# Load environment variables from .env file
# load_dotenv()

app = create_app()

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
