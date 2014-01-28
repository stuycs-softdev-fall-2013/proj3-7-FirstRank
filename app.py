from flask import Flask, render_template, redirect, request
import time
import api

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

@app.route('/Teams/<team_id>')
#@app.route('Teams/<page_num>')
def teams(team_id):
    if team_id == default:
        teams = db.team_compiler()
        return render_template("team.html", teams = teams)
    else:
        teams = api.team_info(team_id)
        return render_template("spec_team.html", team = teams)

if __name__ == "__main__":
    app.debug = True
    app.run()
