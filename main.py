from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS xss (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                injection TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/', methods=['GET'])
@app.route('/<_>', methods=['GET'])
def home(_=None):
    try:
        xss = sqlite3.connect("database.db")
        cursor = xss.cursor() 
        cursor.execute('SELECT * FROM xss') 
        data = cursor.fetchall()
        xss.commit()
    except sqlite3.Error as e:
        print(f"\033[91mAn error occurred:\033[00m {e} ")
        init_db()
    finally:
        if xss:
            xss.close()
    return render_template('index.html', data=data)


@app.route('/inject', methods=['GET', 'POST'])
def Post_injection():
    if request.method == 'POST': 
        injection = request.form['injection'] 
        try:
            xss = sqlite3.connect("database.db")
            cursor = xss.cursor()
            cursor.execute("INSERT INTO xss (injection) VALUES (?)", (injection, ) )
            xss.commit()
        except sqlite3.Error as e:
            print(f"\033[91mAn error occurred:\033[00m {e} ")
            init_db()
        finally:
            if xss:
                xss.close()
        return redirect("/", code=302)
    else:
        return render_template('inject.html')


if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=80)
