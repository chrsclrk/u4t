from flask import Flask, render_template, request, escape, session
from flask import copy_current_request_context
import mysql.connector
# https://pypi.python.org/pypi/DBcm/1.7.1
# from u4tView001_DBcm import UseDatabase, SQLError, CredentialsError
from u4t003_DBcm import *
# https://docs.python.org/3/library/base64.html?highlight=base64#module-base64
import base64
import sys

app = Flask(__name__)
app.config['dbconfig'] = {'host': 'chrsclrk.mysql.pythonanywhere-services.com',
            'user': 'chrsclrk',
            'password': 'lain82.dodos',
            'database': 'chrsclrk$u4t', }   
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

@app.route('/')
def hello() -> str:
    return """Hello world from /Users/chrsclrk/Google Drive/computer_infrastructure/viewTopics/etudes/webapp"""


@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to UPLIFT :University Personnel Learning Ideas For Thriving!')


# Relying on previous defining dict: "dbconfig" and class: "UseDatabase".
@app.route('/manyRows', methods=['GET', 'POST'])
def allContent_page() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """SELECT mlb, title, dscrpt, png
                   FROM u4t"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    bento = []  #TODO convert to list comprehension
    for row in contents:
        bento.append((row[0],
                      row[1],
                      row[2],
                      str(base64.standard_b64encode(row[3]), 'utf-8'), ))
    titles = ('MLB', 'Topic', 'Image', 'Explanation',)
    print('MySqL: mlb: {} len(png): {}'.format(contents[0][0], len(contents[0][2])), file=sys.stderr)
    print('bento: mlb: {} len(png): {}'.format(bento[0][0], len(bento[0][2])), file=sys.stderr)
    return render_template('manyRows.html',
                            the_data=bento, )
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=64000)
