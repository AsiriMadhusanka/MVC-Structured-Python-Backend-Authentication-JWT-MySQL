from flask import Flask
from src.routes.authRoutes import auth_routes
from src.routes.userRoutes import user_routes
import os
from dotenv import load_dotenv


load_dotenv() # load environment variables from .env file

app = Flask(__name__)

app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)

if __name__ == '__main__':
 port = os.getenv('APP_PORT')
 if port is None:
  port = 3000 # default port if APP_PORT is not set
 app.run(debug=True, host='0.0.0.0', port=int(port))






