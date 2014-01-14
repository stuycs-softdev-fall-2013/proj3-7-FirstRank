from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/About')
def about():
    return render_template("about.html")

@app.route('/Events')
def events():
    d = []
    a = {}
    a['title'] = 'titleasddfkagjlkdsajfl;kadjsflk;adjskl;f'
    a['info'] = 'ifskafjklsanfo'
    b = {}
    b['title'] = 'titlsadklfslakdjfklsadje'
    b['info'] = 'infsakfhlsdao'
    d.append(a)
    d.append(b)
    return render_template("events.html", events = d)

#individual stat page
@app.route('/Teams')
def teams():
    return render_template("teams.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
