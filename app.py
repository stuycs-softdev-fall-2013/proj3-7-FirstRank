from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/<link>')
def about(link):
    return redirect("http://www3.usfirst.org/roboticsprograms/frc")


# returns an event page
# a specific event_id will be reserved
# to access a list of all events.

default = "d0000"
@app.route('/Events/<event_id>')
def events(event_id):
    events = []
# events is a list of dictionaries. Each dictionary will store
# all information about a specific event, including links to
# specific teams
    if event_id == default:
# return master-list of all events. table format(?)
        return render_template("events.html", events = events)
# returns specific event page
    return render_template("spec_event.html",
                           event = events[event_id]);

# works the same way as the Events page
# same default value
@app.route('/Teams/<team_id>')
def teams(team_id):
    teams = []
    if team_id == default:
        return render_template("team.html", teams = teams)
    return render_template("spec_team.html",
                           team = teams[team_id])

if __name__ == "__main__":
    app.debug = True
    app.run()
