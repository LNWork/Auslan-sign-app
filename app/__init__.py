from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return 'Index page'

@app.route("/hello")
def hello_world():
    return "<p>Hello World!<p>"
 
@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

