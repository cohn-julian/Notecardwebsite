"""
todo:
        add title/instructions to bottom of page
"""
from flask import Flask, render_template, request, redirect, url_for
from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import *

db = SqliteExtDatabase("cards.db")

class Set(Model):
    name = CharField()

    class Meta:
        database = db

class Card(Model):
    term = CharField()
    text = TextField()
    set = ForeignKeyField(Set, related_name='cards')

    class Meta:
        database = db

app = Flask(__name__)

@app.before_request
def before_request():
    db.connect()
    db.create_tables([Card, Set], safe=True)

@app.teardown_request
def teardown_request(exception):
    db.close()

@app.route("/")
def view_sets():
    return render_template("sets.html", sets=Set.select().order_by(Set.name))

@app.route("/<s>/")
def cards(s):
    try:
        set = Set.get(id=s)
        return render_template("cards.html", cards=set.cards.order_by(Card.term));
    except:
        return "error"

@app.route("/add_set")
def add_set():
    return render_template("new_set.html")

@app.route("/create_set/", methods=['POST'])
def create_set():
    Set.create(
        name=request.form['set_name']
    )
    return redirect("/")

@app.route("/add")
def add_Card():
    return render_template("new_card.html", set = Set.select().order_by(Set.name))

@app.route("/create/", methods=['POST'])
def create_Card():
    Card.create(
        term = request.form['term'],
        text = request.form['text'],
        set = Set.get(name=request.form['set_chooser'])
    )
    return redirect("/{}".format(Set.get(name=request.form['set_chooser']).id))

@app.route("/delete/<card>")
def delete_card(card):
    try:
        c = Card.get(id=card)
        location = c.set.id
        c.delete_instance()
        return redirect("/{}".format(location))
    except:
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, )
