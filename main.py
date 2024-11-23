from flask import render_template
from api import create_app, db

app = create_app()

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=80)
