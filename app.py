from flask import Flask, render_template, redirect, request
import time
import api
import db

app = Flask(__name__)

year = time.localtime()[0]

@app.route('/')
def home():
    return render_template("index.html")

#@app.route('/Search', methods=['GET', 'POST'])
#def search():
 #   if request.method == "GET":
  #      return render_template("search.html")
   # else:
    #    return render_template("search.html") 

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
        return render_template("spec_event.html", event = events)

@app.route('/Teamlist/<page_num>')
def teamlist(page_num=1):
    page = int(page_num)
    teams = db.team_compiler(page)
    d = {}
    d['page'] = page
    d['total'] = 54
    return render_template("team.html", teams = teams, d=d) 

@app.route('/Teams/<team_id>')
def teams(team_id):
    teams = api.team_info(team_id)
    stat = {}
    return render_template("spec_team.html", team = teams, stats=stat)

if __name__ == "__main__":
    app.debug = True
    app.run()
