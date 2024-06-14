from flask import Flask
from flasgger import Swagger
from user_view import user_blueprint
from animals_zoo import animals_blueprint
from employee_zoo import employee_blueprint

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(animals_blueprint)
app.register_blueprint(employee_blueprint)

@app.route("/")
def home():
    return "This is ZOO API"

if __name__ == "__main__":
    app.run(debug=True)
