from flask import Flask, render_template, request
import mongoengine as db
import datetime
import os

#import __passwd__
class __passwd__: passwd = os.environ["PASSWD"]

dbname = "test1"
user = "test1"

c = db.connect(host=("mongodb://{user}:{passwd}@ds033390.mongolab.com:33390/{dbname}"
                     .format(user=user, passwd=__passwd__.passwd, dbname=dbname)))

class Message(db.Document):
    timestamp = db.DateTimeField(default=datetime.datetime.now)
    content = db.StringField(required=True)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def do_search():
    if request.method == 'POST':
        term = request.form.get('term')
        if term: Message(content=term).save()

    return render_template('results.html',
                           items=[(p.timestamp, p.content)
                                  for p in Message.objects.order_by("-timestamp")])

if os.environ["LOCAL"] == "yes":
    app.run(host='0.0.0.0', port=8080, debug=True)
