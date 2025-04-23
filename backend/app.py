from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging
import argparse

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
app = Flask(__name__)
CORS(app)

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', 'rootpassword')}@{os.getenv('DB_HOST', 'localhost')}/{os.getenv('DB_NAME', 'mydb')}"
)
db = SQLAlchemy(app)

# 環境変数の値を確認
app.logger.setLevel(logging.DEBUG)
app.logger.debug("DB_HOST: %s", os.getenv("DB_HOST"))
app.logger.debug("DB_URI: %s", app.config['SQLALCHEMY_DATABASE_URI'])

logging.basicConfig(
        filename=os.path.join(log_dir, 'app.log'),
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# DBモデル
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))

with app.app_context():
    try:
        db.create_all()
        print("Umaku Ittayo!")
    except Exception as e:
        print(f"Error Detayo!{str(e)}")
        app.logger.error(f"Error in db.create_all: {str(e)}")

@app.route('/submit', methods=['POST'])
def submit():
    try:
        if not request.is_json:
            return jsonify({"status": "error", "message": "Invalid JSON format"}), 415
        data = request.json
        name = data.get('name')
        email = data.get('email')

        if not name or not email:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"status": "success", "data": {"name": name, "email": email}})

    except Exception as e:
        # エラーログの記録
        app.logger.error(f"Error in /submit: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        result = [{"name": u.name, "email": u.email} for u in users]
        return jsonify(result)
    except Exception as e:
        # エラーログの記録
        app.logger.error(f"Error in /users: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    
    app.run(debug=True, host='0.0.0.0', port=args.port)
