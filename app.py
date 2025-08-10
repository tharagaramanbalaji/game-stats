from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import DB_CONFIG


app = Flask(__name__)

# MySQL Connection
mydb = mysql.connector.connect(**DB_CONFIG)
mycursor = mydb.cursor(buffered=True)

def stand_unranked():
    try:
        mycursor.execute("""

            
            CREATE TRIGGER stand_unranked_trigger
            BEFORE INSERT ON gameinfo
            FOR EACH ROW
            BEGIN
                IF NEW.stand IS NULL OR NEW.stand = 'null' THEN
                    SET NEW.stand = 'unranked';
                END IF;
            END;
            
            //

        """)
        mydb.commit()

    except mysql.connector.Error as error:
        print("Error creating trigger:", error)


stand_unranked()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
        mycursor.execute("SELECT * FROM gameinfo ORDER BY wins DESC LIMIT 3")
        rows = mycursor.fetchall()
        return render_template('dashboard.html', rows=rows)


@app.route('/add_record', methods=['GET','POST'])
def add_record():
    playerid = request.form.get('playerid')
    username = request.form.get('username')
    rank = request.form.get('rank')
    wins = request.form.get('wins')
    winrate = request.form.get('winrate')
    killrate = request.form.get('killrate')
    clanid = request.form.get('clanid')
    sql = "INSERT INTO gameinfo (playerid,username,stand,wins,winrate,killrate,clanid) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val = (playerid,username,rank,wins,winrate,killrate,clanid)
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for('view_records'))


@app.route('/remove_record/<int:playerid>')
def remove_record(playerid):
    sql = "DELETE FROM gameinfo WHERE playerid = %s"
    val = (playerid,)
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for('view_records'))


@app.route('/view_records')
def view_records():
    mycursor.execute("SELECT * FROM gameinfo order by wins desc")
    records = mycursor.fetchall()
    return render_template('records.html', records=records)






if __name__ == '__main__':
    app.run(debug=True)

