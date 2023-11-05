from email.feedparser import FeedParser
from urllib.parse import urljoin
from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
#from feedwerk import atom
from datetime import datetime
#import feedparser
# from feedgen.feed import FeedGenerator

app = Flask(__name__)
FEED_URL = "https://gioele.uber.space/k/fdla2023/feed1.atom"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def get_abs_url(url):
    return urljoin(request.url_root, url)


class Events(db.Model):
    __tablename__ = 'submitted_Events'
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    title = db.Column("title", db.String(100))
    date = db.Column("date", db.DateTime)
    description = db.Column("description", db.String(1000))
    upload = db.Column("upload", db.DateTime)
    atomID = db.Column("atomID", db.String(100))

    def __init__(self, name, title, date, description, upload, atomID):
        self.name = name
        self.title = title
        self.date = date
        self.description = description
        self.upload = upload
        self.atomID = atomID


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    feed = feedparser.parse(FEED_URL)  # obtains feed from the URL

    # makes a list of the AtomIDs of all Events currently in the database
    existentAtomIDs = [event.atomID for event in Events.query.all()]
    isInDb = False

    # Loops over all entries in the feed, checks if they are already in the Database using their AtomID and if not adds them
    for entry in feed.entries:
        isInDb = False

        atomID = entry.get("id")

        for existentID in existentAtomIDs:
            if existentID == atomID:
                isInDb = True
                break

        if isInDb == True:
            continue

        name = entry.get("author")
        title = entry.get("title")
        updated = entry.get("updated")[:-1]
        date = datetime.strptime(updated, '%Y-%m-%dT%H:%M:%S')
        description = entry.get("summary")
        published = entry.get("published")[:-1]
        upload = datetime.strptime(published, '%Y-%m-%dT%H:%M:%S')

        event = Events(name, title, date, description, upload, atomID)
        db.session.add(event)
        db.session.commit()

    # Renders the webpage with the content of the database as text
    return render_template('home.html', values=Events.query.all())


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':

        name = request.form["nm"]
        title = request.form["ttl"]
        date = datetime.strptime(request.form["dt"], '%Y-%m-%dT%H:%M')
        description = request.form["desc"]
        upload = datetime.now()
        atomID = name + title + datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        print(atomID)

        event = Events(name, title, date, description, upload, atomID)
        db.session.add(event)
        db.session.commit()

        return render_template('form.html')

    else:
        return render_template('form.html')


#@app.route('/feeds/')
#def feeds():
   # feed = atom.AtomFeed(title='Latest Events:',
                         #feed_url=request.url, url=request.url_root)

    #numberOfEvents = db.session.query(Events).count()

    #for number in range(1, numberOfEvents):
        #feed.add(db.session.get({"title", number}), db.session.get({"description", number}),
                 #content_type='html',
                 #author=db.session.get({"name", number}),
                 #url=get_abs_url(db.session.get({"title", number})),
                #updated=db.session.get({"upload", number}),
                 #published=db.session.get({"upload", number}))

   # return feed.get_response()


with app.app_context():
    db.create_all()

with app.app_context():
    with open("atom.xml", 'w') as f:
        # Create the .atom file
        f.write('<feed xmlns="http://www.w3.org/2005/Atom">''<title>Events feed</title>''<id>urn:uuid:d3617f5d-cebc-470d-b166-8d6ef98af168</id>''<updated>2023-10-04T16:30:42Z</updated>')
        # feed = atom.AtomFeed(title='Latest Events:',
        #                     feed_url=request.url, url=request.url_root)
        # print(feed.entries)
        for event in Events.query.all():
            atomID = event.atomID
            print(atomID + "1111")
            name = event.name
            title = event.title
            updated = datetime.strftime(
                event.upload, '%Y-%m-%dT%H:%M:%S') + "Z"
            date = datetime.strftime(event.date, '%Y-%m-%dT%H:%M:%S') + "Z"
            description = event.description
            published = datetime.strftime(
                event.upload, '%Y-%m-%dT%H:%M:%S') + "Z"
            a = ("<entry>" + "\n" + "\t" + "<" + atomID + ">" + "\n" + "\t" + "<" + name + ">" + "\n" + "\t" + "<" + title + ">" + "\n" +
                 "\t" + "<" + updated + ">" + "\n" + "\t" + "<" + date + ">" + "\n" + "\t" + "<" + description + ">" + "\n" + "\t" + "<" + published + ">" + "</entry>" + "\n")
            f.write(a)

        # print(feed.entries)
