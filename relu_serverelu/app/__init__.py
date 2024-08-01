from flask import Flask
from .device.display import display_static_message

def create_app():
    app = Flask(__name__)
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    display_static_message()
    
    return app