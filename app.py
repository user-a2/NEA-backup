from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3 as sql
import json
app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def home():
    conn = sql.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS parcels (''delivery_type TEXT, customer_email TEXT, customer_phone TEXT, customer_address TEXT, '
                 'customer_postcode TEXT, delivery_postcode TEXT, delivery_cost TEXT, delivery_status TEXT)')
    print("Table created successfully")
    conn.close()
    return render_template('home.html')

@app.route("/track/<id>")
def get_parcel(id):
   #take the id parameter and query the db with it
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from parcels where parcel_id ="+id)
   
   rows = cur.fetchall(); 
   #return render_template("list.html",rows = rows)
   results = []
   for row in rows:
      results.append(dict(row))

   json_result = json.dumps(results)
   return json_result

@app.route("/directions/<id>")
def get_directions(id):
    # GET THE DIRECTION DATA FROM DATABASE
    # FOR THE EXAMPLE, I WILL JUST USE DUMMY DATA
    directions = [{"field1": "field1 data"}, {"field1": "field2 data"}]

    """
    Any data you want to pass to the template, you just
    list it as a keyword argument.
    For example, if you wanted to add a variable for a user,
    you would just add user=user_object.
    """
    return render_template("directions.html", directions=directions)

@app.route('/enternew')
def new_parcel():
    return render_template('parcel.html')

@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
        
            delivery_type = request.form['delivery_type']
            customer_email = request.form['customer_email']
            customer_phone = request.form['customer_phone']
            customer_address = request.form['customer_address']
            customer_postcode = request.form['customer_postcode']
            delivery_postcode = request.form['delivery_postcode']
            delivery_cost = request.form['delivery_cost']
            delivery_status = request.form['delivery_status']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO parcels (delivery_type, customer_email, "
                            "customer_phone, customer_address, customer_postcode, delivery_postcode, "
                            "delivery_cost, delivery_status) VALUES (?,?,?,?,?,?,?,?)",
                            (delivery_type, customer_email, customer_phone, customer_address,
                             customer_postcode, delivery_postcode, delivery_cost, delivery_status))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM parcels")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
