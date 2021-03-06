import os
import logging
import json
import subprocess

from flask import Flask, render_template, jsonify, request
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_, and_
from flask.ext.cors import CORS
import mapper

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.debug("Welcome")

SQLALCHEMY_DATABASE_URI = \
    '{engine}://{username}:{password}@{hostname}/{database}'.format(
        engine='mysql+pymysql',
        username='admin',
        password='password',
        hostname='cs373idb_db',
        database='marvel')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

manager = Manager(app)
db = SQLAlchemy(app)

from api import *
from models import *

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/legends')
def legends():
    return render_template('legends.html')

@app.route('/api/characters', methods=["GET"])
def characters():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    count = db.session.query(func.count(Character.id))
    count = count.scalar()
    if offset and limit:
        offset = int(offset)
        limit = int(limit)
        return jsonify({'characters': list(map(mapper.character_to_dict, Character.query.slice(offset, offset+limit))), 'count': count})
    else:
        return jsonify({'characters': list(map(mapper.character_to_dict, Character.query.all())), 'count': count})

@app.route('/api/character/<character_id>', methods=["GET"])
def character(character_id):
    return jsonify({'character': mapper.character_detail_to_dict(Character.query.filter_by(id=character_id).first())})

@app.route('/api/comics', methods=["GET"])
def comics():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    count = db.session.query(func.count(Comic.id))
    count = count.scalar()
    if offset and limit:
        offset = int(offset)
        limit = int(limit)
        return jsonify({'comics': list(map(mapper.comic_to_dict, Comic.query.slice(offset, offset+limit))), 'count': count})
    else:
        return jsonify({'comics': list(map(mapper.comic_to_dict, Comic.query.all())), 'count': count})

@app.route('/api/comic/<comic_id>', methods=["GET"])
def comic(comic_id):
    return jsonify({'comic': mapper.comic_detail_to_dict(Comic.query.filter_by(id=comic_id).first())})

@app.route('/api/creators', methods=["GET"])
def creators():
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    count = db.session.query(func.count(Creator.id))
    count = count.scalar()
    if offset and limit:
        offset = int(offset)
        limit = int(limit)
        return jsonify({'creators': list(map(mapper.creator_to_dict, Creator.query.slice(offset, offset+limit))), 'count': count})
    else:
        return jsonify({'creators': list(map(mapper.creator_to_dict, Creator.query.all())), 'count': count})

@app.route('/api/creator/<creator_id>', methods=["GET"])
def creator(creator_id):
    return jsonify({'creator': mapper.creator_detail_to_dict(Creator.query.filter_by(id=creator_id).first())})

@app.route('/api/search/<search_term>', methods=["GET"])
def search(search_term):
    search_terms = search_term.split(" ")
    ch_a = list(map(mapper.character_to_dict, Character.query.filter(
                    or_(Character.name.contains(search_term), Character.id.contains(search_term), Character.description.contains(search_term),
                        Character.number_of_comics.contains(search_term), Character.number_of_series.contains(search_term),
                        Character.number_of_stories.contains(search_term)
                    )).all()))
    co_a = list(map(mapper.comic_to_dict, Comic.query.filter(
                    or_(Comic.title.contains(search_term), Comic.id.contains(search_term), Comic.issue_num.contains(search_term),
                        Comic.description.contains(search_term), Comic.page_count.contains(search_term), Comic.series.contains(search_term),
                        Comic.number_of_creators.contains(search_term), Comic.number_of_characters.contains(search_term), Comic.number_of_stories.contains(search_term)
                    )).all()))
    cr_a = list(map(mapper.creator_to_dict, Creator.query.filter(
                    or_(Creator.id.contains(search_term), Creator.first_name.contains(search_term), Creator.last_name.contains(search_term), (Creator.first_name+" "+Creator.last_name).contains(search_term),
                        Creator.number_of_comics.contains(search_term), Creator.number_of_stories.contains(search_term),
                        Creator.number_of_series.contains(search_term)
                    )).all()))
    if len(search_terms) > 1:
        ch_o = list(map(mapper.character_to_dict, Character.query.filter(and_(or_(*[or_(
                        Character.name.contains(term), Character.id.contains(term), Character.description.contains(term),
                        Character.number_of_comics.contains(term), Character.number_of_series.contains(term),
                        Character.number_of_stories.contains(term)) for term in search_terms])),
                        and_(Character.name.contains(search_term)==False, Character.id.contains(search_term)==False, Character.description.contains(search_term)==False,
                        Character.number_of_comics.contains(search_term)==False, Character.number_of_series.contains(search_term)==False,
                        Character.number_of_stories.contains(search_term)==False)
                    ).all()))
        co_o = list(map(mapper.comic_to_dict, Comic.query.filter(and_(or_(*[or_(
                        Comic.title.contains(term), Comic.id.contains(term), Comic.issue_num.contains(term),
                        Comic.description.contains(term), Comic.page_count.contains(term), Comic.series.contains(term),
                        Comic.number_of_creators.contains(term), Comic.number_of_characters.contains(term), Comic.number_of_stories.contains(term)) for term in search_terms])),
                        and_(Comic.title.contains(search_term)==False, Comic.id.contains(search_term)==False, Comic.issue_num.contains(search_term)==False,
                            Comic.description.contains(search_term)==False, Comic.page_count.contains(search_term)==False, Comic.series.contains(search_term)==False,
                            Comic.number_of_creators.contains(search_term)==False, Comic.number_of_characters.contains(search_term)==False, Comic.number_of_stories.contains(search_term)==False)
                    ).all()))
        cr_o = list(map(mapper.creator_to_dict, Creator.query.filter(and_(or_(*[or_(
                        Creator.first_name.contains(term), Creator.last_name.contains(term), Creator.id.contains(term),
                        Creator.number_of_comics.contains(term), Creator.number_of_stories.contains(term),
                        Creator.number_of_series.contains(term)) for term in search_terms])),
                        and_(Creator.id.contains(search_term)==False, Creator.first_name.contains(search_term)==False, Creator.last_name.contains(search_term)==False,
                            (Creator.first_name+" "+Creator.last_name).contains(search_term)==False,
                            Creator.number_of_comics.contains(search_term)==False, Creator.number_of_stories.contains(search_term)==False,
                            Creator.number_of_series.contains(search_term)==False)
                    ).all()))
    else:
        ch_o = []
        co_o = []
        cr_o = []
    return jsonify({'characters_and': ch_a,
                    'characters_or': ch_o,
                    'comics_and': co_a,
                    'comics_or': co_o,
                    'creators_and': cr_a,
                    'creators_or': cr_o})

@app.route('/run-tests')
def run_tests():
    b_output = subprocess.check_output(['python3', 'tests.py'], stderr=subprocess.STDOUT)
    test_output = b_output.decode('ascii')
    return render_template('about.html', test_output=test_output)

# Serves the initial website (the catch-all is to facilitate react-router routes)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@manager.command
def create_db():
    logger.debug("create_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.create_all()

@manager.command
def drop_db():
    logger.debug("drop_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()

@manager.command
def add_characters():
    logger.debug("add characters")
    app.config['SQLALCHEMY_ECHO'] = True
    with open("characters.json") as data_file:
        data = json.load(data_file)
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                json_data = data[i][j]
                add_character(json_data)

@manager.command
def add_comics():
    logger.debug("add comics")
    app.config['SQLALCHEMY_ECHO'] = True
    with open("comics1.json") as data_file:
        data = json.load(data_file)
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                json_data = data[i][j]
                add_comic(json_data)
    with open("comics2.json") as data_file:
        data = json.load(data_file)
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                json_data = data[i][j]
                add_comic(json_data)

@manager.command
def add_creators():
    logger.debug("add creators")
    app.config['SQLALCHEMY_ECHO'] = True
    with open("creators.json") as data_file:
        data = json.load(data_file)
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                json_data = data[i][j]
                add_creator(json_data)

@manager.command
def update_characters():
    logger.debug("update characters")
    app.config['SQLALCHEMY_ECHO'] = True
    with open("characters.json") as data_file:
        data = json.load(data_file)
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                json_data = data[i][j]
                update_character(json_data)

@manager.command
def update_comics():
    logger.debug("update comics")
    app.config['SQLALCHEMY_ECHO'] = True
    with open("comics1.json") as data_file:
        data = json.load(data_file)
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                json_data = data[i][j]
                update_comic(json_data)
    with open("comics2.json") as data_file:
        data = json.load(data_file)
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                json_data = data[i][j]
                update_comic(json_data)

@manager.command
def update_creators():
    logger.debug("update creators")
    app.config['SQLALCHEMY_ECHO'] = True
    with open("creators.json") as data_file:
        data = json.load(data_file)
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                json_data = data[i][j]
                update_creator(json_data)

@manager.command
def test_all_data():
    logger.debug("test all data")
    app.config['SQLALCHEMY_ECHO'] = True
    creators = Creator.query.all()
    for creator in creators:
        logger.debug(creator.first_name)
        logger.debug(creator.comics)
    comics = Comic.query.all()
    for comic in comics:
        logger.debug(comic.title)
        logger.debug(comic.characters)
        logger.debug(comic.creators)
    characters = Character.query.all()
    for character in characters:
        logger.debug(character.name)
        logger.debug(character.comics)

if __name__ == '__main__':
    manager.run()
