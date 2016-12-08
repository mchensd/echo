from flask import Flask, request, render_template
import os
import json
import time, datetime, goslate

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('init.html')

@app.route('/entry', methods=['GET'])
def entry():
    entry=request.args.get('echo')
    t = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    ip = request.remote_addr
    f = open('entry.txt', 'r')
    j_data = json.load(f)
    f.close()
    j_data["amount_of_entries"] += 1

    if str(entry) == '':
        echo=None

        j_data["no_entries"]["entries"] += 1
        cur_entry = j_data["no_entries"]["entries"]
        j_data["no_entries"]["entry{}".format(cur_entry)]={"ip_address": str(ip), "timestamp":t}

    else:
        echo=str(entry)

        j_data["with_entries"]["entries"] += 1
        cur_entry = j_data["with_entries"]["entries"]
        j_data["with_entries"]["entry{}".format(cur_entry)]={"content":echo, "ip_address":str(ip), "timestamp":t}

    f=open('entry.txt','w')
    json.dump(j_data, f, indent=4, sort_keys=True)
    f.close()

    return render_template("return.html", echo=echo)

@app.route('/sure', methods=['GET'])
def sure():
    return render_template("sure.html")

@app.route('/clear', methods=['GET'])
def clear():
    f = open('entry.txt', 'r')
    j_data = json.load(f)
    f.close()
    data={"amount_of_entries":0, "no_entries":{"entries":0}, "with_entries":{"entries":0}}
    f = open('entry.txt', 'w')
    json.dump(data, f, indent=4, sort_keys=True)
    return render_template("clear.html")

@app.route('/table', methods=['GET'])
def table():
    # if str(request.remote_addr) == "10.51.173.231":  # does not work, this is just a local ip address
    f = open('entry.txt', 'r')
    j_data = json.load(f)
    f.close()
    e = j_data['with_entries']
    del e['entries']
    entries = []
    for i in e:
        entries.append(e[i])
    return render_template("table.html", entries=entries)
    # else:
        # return render_template("no_access.html")

@app.route('/table_admin')
def table_admin():
    f = open('entry.txt', 'r')
    j_data = json.load(f)
    f.close()
    e = j_data['with_entries']
    del e['entries']
    entries = []
    for i in e:
        entries.append(e[i])
    return render_template("table.html", entries=entries)

@app.route('/translate', methods=['GET'])
def translate():
    #gs = goslate.Goslate()  # translator
    name = request.args.get('name')
    return render_template("translate.html", name=name)
    #phrase = request.args.get('phrase')
    #translated = gs.translate(phrase, 'es')
    #, translated=translated, phrase=phrase)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
