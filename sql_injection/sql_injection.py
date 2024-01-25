from flask import Flask, request, session
import psycopg2
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import Session, declarative_base

DB_URL = "postgresql://" + "postgres" + ":" + "12345" + "@localhost:9000/postgres"
app = Flask(__name__)
engine = create_engine(DB_URL, echo=True)
Base = declarative_base()

class Doctor(Base):
    __tablename__ = "doctor"
    doctor_id=Column(Integer,primary_key=True)
    doctor_name = Column(String)
    authentication_key = Column(String, nullable=False)


@app.route("/add_doctor", methods=["POST"])
def add_doctor():
    
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)

    doctor_id=request.json.get('doctor_id')
    doctor_name=request.json.get('doctor_name')
    authentication_key=request.json.get('authentication_key')

    session = Session(engine)

    dummyDoctor = Doctor(doctor_id=doctor_id,doctor_name=doctor_name,authentication_key=authentication_key)
    session.add_all([dummyDoctor])
    session.commit()
    
    session.close()
    return f"Success"

DB_CONFIG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '12345',
    'port':9000
}

@app.route("/get_doctor", methods=["GET"])
def get_doctor():
    doctor_id=request.json.get('doctor_id')
    authentication_key=request.json.get('authentication_key')

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    #injection
    #"6 OR TRUE;--",

    # sql_query = "SELECT * FROM public.doctor WHERE doctor_id = " + str(doctor_id)  + " AND authentication_key = '" + authentication_key + "'"
    sql_query="SELECT * FROM public.doctor WHERE doctor_id = %s AND authentication_key = %s", (doctor_id, authentication_key)
    print(sql_query)
    try:
        cursor.execute(sql_query)
        record = cursor.fetchone()
        doctor_session = {}
        print(record)
        if record:
            doctor_session['logged_doctor'] = doctor_id
        try:
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)
        return "Login successful" if 'logged_doctor' in doctor_session else "Login failed"
    except Exception as e:
        return "Invalid credentials"
    
    
@app.route("/delete_doctor", methods=["DELETE"])
def delete_doctor():
    doctor_id=request.json.get('doctor_id')
    authentication_key=request.json.get('authentication_key')
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    sql_query="DELETE FROM public.doctor WHERE doctor_id = "+str(doctor_id)+" AND authentication_key = '"+authentication_key+"'"
    print(sql_query)
    cursor.execute(sql_query)
    cursor.close()
    conn.close()
    return "DEleted Record"
if __name__ == "__main__":
    app.run()