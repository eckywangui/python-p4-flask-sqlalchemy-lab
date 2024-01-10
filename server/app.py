#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    response_body = f'''
    <h1>Animal Details</h1>
    <ul>
        <li>ID: {animal.id}</li>
        <li>Name: {animal.name}</li>
        <li>Species: {animal.species}</li>
        <li>Zookeeper: {animal.zookeeper.name}</li>
        <li>Enclosure: {animal.enclosure.environment}</li>
    </ul>
    '''
    return make_response(response_body)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    response_body = f'''
    <h1>Zookeeper Details</h1>
    <ul>
        <li>ID: {zookeeper.id}</li>
        <li>Name: {zookeeper.name}</li>
        <li>Birthday: {zookeeper.birthday}</li>
    </ul>
    <h2>Animals:</h2>
    <ul>
    '''
    for animal in zookeeper.animals:
        response_body += f'<li>Animal: {animal.name}</li>'

    response_body += '</ul>'
    return make_response(response_body)


@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    response_body = f''
    response_body += f'<ul>ID: {enclosure.id}</ul>'
    response_body += f'<ul>Environment: {enclosure.environment}</ul>'
    response_body += f'<ul>Open to Visitors: {enclosure.open_to_visitors}</ul>'

    for animal in enclosure.animals:
        response_body += f'<ul>Animal: {animal.name}</ul>'

    return make_response(response_body)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
