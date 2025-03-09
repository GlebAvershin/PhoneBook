from flask import Flask, request, redirect, render_template
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)
Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    fio = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    note = Column(Text)

Base.metadata.create_all(engine)

@app.route('/', methods=['GET'])
def index():
    session = Session()
    contacts = session.query(Contact).all()
    session.close()
    return render_template('index.html', contacts=contacts)

@app.route('/create', methods=['POST'])
def create():
    session = Session()
    new_contact = Contact(
        fio=request.form['fio'],
        phone_number=request.form['phone_number'],
        note=request.form['note']
    )
    session.add(new_contact)
    session.commit()
    session.close()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    session = Session()
    contact = session.query(Contact).get(id)
    if request.method == 'POST':
        contact.fio = request.form['fio']
        contact.phone_number = request.form['phone_number']
        contact.note = request.form['note']
        session.commit()
        session.close()
        return redirect('/')
    session.close()
    return render_template('index.html', update_id=id, update_fio=contact.fio, update_phone_number=contact.phone_number, update_note=contact.note)

@app.route('/delete/<int:id>')
def delete(id):
    session = Session()
    contact = session.query(Contact).get(id)
    session.delete(contact)
    session.commit()
    session.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
