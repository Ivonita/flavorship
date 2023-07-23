from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
users = []
restaurants = []
POSTGRESQL_URL = "postgres://qtsfupas:XzUVIeUevUrecr_QN-I1sB4OHe-sA0SS@tyke.db.elephantsql.com/qtsfupas"

connection = psycopg2.connect(POSTGRESQL_URL)

try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE users (name TEXT, email TEXT, passwort TEXT, location TEXT);")
            cursor.execute("CREATE TABLE restaurants (name TEXT, email TEXT, passwort TEXT);")
except psycopg2.errors.DuplicateTable:
    pass



@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html")



@app.route("/user_register", methods=["GET", "POST"])
@app.route("/user_register.html", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        print(request.form)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users VALUES (%s, %s, %s, %s);",
                    (
                        request.form.get("name"),
                        request.form.get("email"),
                        request.form.get("passwort"),
                        request.form.get("location"),
                    ),
                )
    return render_template("user_register.html")



@app.route("/users")
@app.route("/users.html")
def display_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
    return render_template("users.html", entries=users)



@app.route("/restaurant_register", methods=["GET", "POST"])
@app.route("/restaurant_register.html", methods=["GET", "POST"])
def restaurant_register():
    if request.method == "POST":
        print(request.form)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO restaurants VALUES (%s, %s, %s)",
                     (
                        request.form.get("name"),
                        request.form.get("email"),
                        request.form.get("passwort"),
                     ),
                )
    return render_template("restaurant_register.html")



@app.route("/restaurants")
@app.route("/restaurants.html")
def display_restaurants():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM restaurants;")
            restaurants = cursor.fetchall()
    return render_template("restaurants.html", entries=restaurants)



@app.route('/restaurants_map')
@app.route('/restaurants_map.html')
def map():
    coordinates = {'latitude': 52.520008, 'longitude': 13.404954}
    return render_template('restaurants_map.html', coordinates=coordinates)





if __name__ == "__main__":
    app.run(debug=True)