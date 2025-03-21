# app.py
from flask import Flask
from database.setup import initialize_db
from routes.user_controller import user_routes
from routes.image_controller import image_routes
from routes.admin_controller import admin_routes
from flask_jwt_extended import JWTManager
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': os.getenv('MONGODB_URI')
}
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

# Khởi tạo JWT
jwt = JWTManager(app)

# Khởi tạo cơ sở dữ liệu
initialize_db(app)

# Đăng ký blueprints
app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(image_routes, url_prefix='/api/images')
app.register_blueprint(admin_routes, url_prefix='/api/admin')

if __name__ == '__main__':
    app.run(debug=True)
