from flask import Flask, render_template, redirect, request
import time
import api
import db

app = Flask(__name__)

year = time.localtime()[0]
month = time.localtime()[1]
day = time.localtime()[2]

@app.route('/')
def home():
    stats = []
    if month > 2 or (month == 2 and day == 28):
        stats = db.get_current_stats(year)
    return render_template("index.html", teams=stats)

@app.route('/<link>')
def about(link):
    return redirect("http://www3.usfirst.org/roboticsprograms/frc")

default = "d0000"
@app.route('/Events/<event_id>')
def events(event_id):
    if event_id == default:
        events = api.event_list(year)
        return render_template("events.html", events = events)
    else:
        events = api.event_info(event_id)
        teams = db.get_event_stats(event_id)
        return render_template("spec_event.html", event = events, teams=teams)

@app.route('/Teamlist/<page_num>')
def teamlist(page_num=1):
    page = int(page_num)
    if month < 2:
        year = year - 1
    teams = db.get_teamlist(year, page)
    d = {'page':page, 'total':54}
    return render_template("team.html", teams = teams, d=d) 

@app.route('/Teams/<team_id>')
def teams(team_id):
    teams = api.team_info(team_id)
    stats = db.get_team_overall_stats(team_id)
    event_stats = db.get_team_event_stats(team_id)
    return render_template("spec_team.html", team = teams, stats=stats, events=event_stats)

if __name__ == "__main__":
    app.debug = True
    app.run()
