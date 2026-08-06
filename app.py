from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_identity", methods=["GET","POST"])
def add_one_identity():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into identity (name) values (:name)",hey)
        user = query_db('select * from identity')

        return render_template("identityform.html", identitys=user, one_user=one_user, the_title="add new identity")


    user = query_db('select * from identity')
    one_user = query_db("select * from identity limit 1", one=True)
    return render_template("identityform.html", identitys=user, one_user=one_user, the_title="add new identity")

@app.route("/add_one_track", methods=["GET","POST"])
def add_one_track():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into track (composer_artist,title) values (:composer_artist,:title)",hey)
        user = query_db('select * from track')

        return render_template("trackform.html", tracks=user, one_user=one_user, the_title="add new track")


    user = query_db('select * from track')
    one_user = query_db("select * from track limit 1", one=True)
    return render_template("trackform.html", tracks=user, one_user=one_user, the_title="add new track")

@app.route("/add_one_socialmedia", methods=["GET","POST"])
def add_one_socialmedia():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into socialmedia (name) values (:name)",hey)
        user = query_db('select * from socialmedia')

        return render_template("socialmediaform.html", socialmedias=user, one_user=one_user, the_title="add new socialmedia")


    user = query_db('select * from socialmedia')
    one_user = query_db("select * from socialmedia limit 1", one=True)
    return render_template("socialmediaform.html", socialmedias=user, one_user=one_user, the_title="add new socialmedia")

@app.route("/add_one_sharemusic", methods=["GET","POST"])
def add_one_sharemusic():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslestrack= query_db("select * from track")

        touslestrack= query_db("select * from track")

        touslesuser= query_db("select * from user")

        one_user = query_db("insert into sharemusic (track_id,track_id,user_id) values (:track_id,:track_id,:user_id)",hey)
        user = query_db('select * from sharemusic')

        return render_template("sharemusicform.html", sharemusics=user, one_user=one_user, the_title="add new sharemusic", touslestrack=touslestrack, touslestrack=touslestrack, touslesuser=touslesuser)


    touslestrack= query_db("select * from track")

    touslestrack= query_db("select * from track")

    touslesuser= query_db("select * from user")

    user = query_db('select * from sharemusic')
    one_user = query_db("select * from sharemusic limit 1", one=True)
    return render_template("sharemusicform.html", sharemusics=user, one_user=one_user, the_title="add new sharemusic", touslestrack=touslestrack, touslestrack=touslestrack, touslesuser=touslesuser)

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        touslesidentity= query_db("select * from identity")

        one_user = query_db("insert into user (username,email,password,country_id,phone,identity_id) values (:username,:email,:password,:country_id,:phone,:identity_id)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','email','password','country_id','phone','identity_id']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry, touslesidentity=touslesidentity)


    touslescountry= query_db("select * from country")

    touslesidentity= query_db("select * from identity")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry, touslesidentity=touslesidentity)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','email','password','country_id','phone','identity_id']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','email','password','country_id','phone','identity_id']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_cli", methods=["GET","POST"])
def add_one_cli():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        one_user = query_db("insert into cli (content,user_id) values (:content,:user_id)",hey)
        user = query_db('select * from cli')

        return render_template("cliform.html", clis=user, one_user=one_user, the_title="add new cli", touslesuser=touslesuser)


    touslesuser= query_db("select * from user")

    user = query_db('select * from cli')
    one_user = query_db("select * from cli limit 1", one=True)
    return render_template("cliform.html", clis=user, one_user=one_user, the_title="add new cli", touslesuser=touslesuser)

