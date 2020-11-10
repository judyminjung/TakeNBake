# Brittany Rollins
# Fall 2020
# sect 31854
# Assignment 9


from flask import Flask, redirect, render_template, request, session, url_for
import os
import sqlite3 as sl

app = Flask(__name__)
db = "favouriteFoods.db"


@app.route("/")
def home():
    if not session.get("logged_in"):
       return render_template("login2.html")
    else:
        if session["username"] == "admin":
            return render_template("admin.html", username=session["username"], result=db_get_user_list())
        else:
            return render_template("acc_page.html", username=session["username"], fav_food=db_get_food(session["username"]))
    pass


@app.route("/client")
def client():
    pass


@app.route("/action/createuser", methods=["POST", "GET"])
def create_user():
    if request.method == "POST":
        if request.form["username"] is not '' and request.form["password"] is not '':
            if db_check_creds(request.form["username"], request.form["password"]) == 0:
                db_create_user(request.form["username"], request.form["password"])
                session["username"] = request.form["username"]
                return render_template("acc_page.html", username=session["username"])
        return render_template("new_user.html", err="That account already exists")


@app.route("/action/updateitem", methods=["POST", "GET"])
def update_item():
    db_set_food(session.get("username"), request.form["item"])
    print(session["username"])
    user = session["username"]
    print(request.form["item"])
    it = db_get_food(session["username"])
    path = 'images/' + it + '.png'
    print(path)
    return render_template("acc_page.html", username=user, item=path, mess="Favorite Item")




@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "password":
            session["username"] = request.form["username"]
            session["logged_in"] = True
            res = db_get_user_list()
            return render_template("admin.html", username=request.form["username"], result=res)
        else:
            exists = db_check_creds(request.form["username"], request.form["password"])
            if exists:
                session["username"] = request.form["username"]
                session["logged_in"] = True
                print("logged in")
                fav = db_get_food(session["username"])
                # return render_template("user2.html", username=request.form["username"], fav_food=fav)
                return render_template("acc_page.html", username=request.form["username"], fav_food=fav)
        return render_template("login2.html", err="no account with those credentials could be found")
    pass


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        session["logged_in"] = False
        print("logged out")
        return render_template("login2.html")
    pass



@app.route("/action/removeuser", methods=["POST", "GET"])
def remove_user():
    if request.method == "POST":
        db_remove_user(request.form["username"])
        session["logged_in"] = False
        return render_template("login2.html")
    pass



# links to other pages on website
@app.route("/createacc", methods=["POST", "GET"])
def new_user():
    return render_template("new_user.html")

@app.route("/acc_page", methods=["POST", "GET"])
def acc_page():
    if session.get("logged_in"):
        if db_get_food(session["username"]) != None:
            it = db_get_food(session["username"])
            path = 'images/' + it + '.png'
            print(path)
            message = "Favorite Item"
        else:
            path = ""
            message = ""
        return render_template("acc_page.html", username=session["username"], mess=message, item=path)
    else:
        return render_template("login2.html", username="Login")

@app.route("/menu", methods=["POST", "GET"])
def menu():
    if session.get("logged_in"):
        return render_template("menu.html", username=session["username"])
    else:
        return render_template("menu.html", username="Login")

@app.route("/plans", methods=["POST", "GET"])
def plans():
    if session.get("logged_in"):
        return render_template("plans.html", username=session["username"])
    else:
        return render_template("plans.html", username="Login")

@app.route("/homepage", methods=["POST", "GET"])
def home2():
    if session.get("logged_in"):
        return render_template("index.html", username=session["username"])
    else:
        return render_template("index.html", username="Login")


@app.route("/shop", methods=["POST", "GET"])
def shop():
    if session.get("logged_in"):
        return render_template("shop.html", username=session["username"])
    else:
        return render_template("shop.html", username="Login")







# add new user to cred and userfoods data base
def db_create_user(un, pw):
    conn = sl.connect(db, check_same_thread=False)  # connect to database
    curs = conn.cursor()
    creat_user = "INSERT INTO credentials (username, password) VALUES (?, ?)"
    create_user2 = "INSERT INTO userfoods (username, food) VALUES (?, ?)"
    curs.execute(creat_user, (un, pw))
    curs.execute(create_user2, (un, None))
    conn.commit()
    conn.close()




# gets fav food of user from returned tuple
def db_get_food(un):
    conn = sl.connect(db, check_same_thread=False)  # connect to database
    curs = conn.cursor()
    get_food_stmt = "SELECT food FROM userfoods WHERE username=?"
    curs.execute(get_food_stmt, (un,))
    food = curs.fetchall()
    conn.close()
    return food[0][0]


# update a user's fave food
def db_set_food(un, ff):
    conn = sl.connect(db, check_same_thread=False)  # connect to database
    curs = conn.cursor()
    enter_food = "UPDATE userfoods SET food=? WHERE username=?"
    curs.execute(enter_food, (ff, un))
    conn.commit()
    conn.close()


# gets tuple from select statement and if it is empty, then no user w/those credentials exists
def db_check_creds(un, pw):
    conn = sl.connect(db, check_same_thread=False)  # connect to database
    curs = conn.cursor()
    login_user = "SELECT 1 FROM credentials WHERE username=? AND password=?"
    curs.execute(login_user, (un, pw))
    real_user = curs.fetchall()
    conn.close()
    if not real_user:
        return 0
    else:
        return real_user[0][0]


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
