"""Project on Fleet information Query system
Author : Aasari Prashanth
Data Scientist.
"""
import sqlite3


# setup spacy corpus
import spacy
from spacy.pipeline import EntityRuler

def init():
    nlp = spacy.load("en_core_web_sm")
    ruler1 = EntityRuler(nlp)
    pattern1 = [{"label": "FLEET", "pattern": "Fleets"}, {"label": "FLEET", "pattern": "Fleet"},
                {"label": "FLEET", "pattern": "Trucks"}, {"label": "FLEET", "pattern": "Truck"},
                {"label": "FLEET", "pattern": "Rails"}, {"label": "FLEET", "pattern": "Rail"},
                {"label": "FLEET", "pattern": "Ships"}, {"label": "FLEET", "pattern": "Ship"},
                {"label": "FLEET", "pattern": "Cargos"}, {"label": "FLEET", "pattern": "Cargo"}]

    # add the rules to NLP engine
    ruler1.add_patterns(pattern1)
    nlp.add_pipe(ruler1, before='ner')
    return nlp

from flask import Flask, render_template, request

app = Flask(__name__)
@app.route('/')
def home():

    return render_template('index.html')

def convert_text_sql(text):
    nlp = init()
    text = text.title()
    doc = nlp(text)
    query = u''
    LIST_FLEETS = ['truck', 'trucks', 'rail', 'rails', 'ship', 'ships', 'cargo', 'cargos']

    # extracting the named entities in the text
    for ent in doc.ents:
        exp = ent.text
        print(ent.text, ent.label_)
        exp = exp.lower()
        if exp in LIST_FLEETS:
            query = 'select * from FLEET where fleet_type = ' + '\'' + exp.title() + '\''
            return query
        else:
            query = 'select * from FLEET'
            return query
    return query

@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        text = convert_text_sql(request.form['Query'])
        sqltext = text
        column_names = []
        if len(sqltext) > 0:
            mysql_conn = sqlite3.connect('./newfleet.db')
            my_cursor = mysql_conn.cursor()
            print(sqltext)
            # sqltext = "select fleet_id, operator_name, fleet_type, capacity, status from fleet"
            my_cursor.execute(sqltext)
            # get the column names
            for c in my_cursor.description:
                column_names.append(c[0])
            # get the data
            rows = my_cursor.fetchall()
        print(column_names)
        for r in rows:
            print(r)
        row = len(rows)

    return render_template("results.html", column_names=column_names, rows=rows, row=row)


if __name__ == "__main__":
    app.run(debug=True)




