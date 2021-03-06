from app import db, logger
from models import *

def add_character(json_data):
    id = json_data[u'id']
    thumbnail = json_data[u'thumbnail'][u'path']+'.' +json_data[u'thumbnail'][u'extension']
    name = json_data[u'name']
    description = json_data[u'description']
    number_of_comics = json_data[u'comics'][u'available']
    number_of_stories = json_data[u'stories'][u'available']
    number_of_series = json_data[u'series'][u'available']

    comic_ids = []
    for comic in json_data[u'comics'][u'items']:
        comic_ids.append(int(comic[u'resourceURI'].split('/comics/')[1]))

    character_test = Character.query.filter_by(id=id).first()
    if not character_test:
        character = Character(id=id, thumbnail=thumbnail, name=name, description=description,
        number_of_comics=number_of_comics, number_of_stories=number_of_stories, number_of_series=number_of_series)

        for comic_id in comic_ids:
            comic = Comic.query.filter_by(id=comic_id).first()
            if comic:
                character.comics.append(comic)

        db.session.add(character)
        logger.debug('Added %s', character)
        db.session.commit()

def add_comic(json_data):
    id = json_data[u'id']
    thumbnail = json_data[u'thumbnail'][u'path']+'.' +json_data[u'thumbnail'][u'extension']
    title = json_data[u'title']
    issue_num = json_data[u'issueNumber']
    description = json_data[u'description']
    page_count = json_data[u'pageCount']
    series = json_data[u'series'][u'name']
    number_of_characters = json_data[u'characters'][u'available']
    number_of_creators = json_data[u'creators'][u'available']
    number_of_stories = json_data[u'stories'][u'available']

    comic_test = Comic.query.filter_by(id=id).first()
    if not comic_test and id != 47352:
        comic = Comic(id=id, thumbnail=thumbnail, title=title, issue_num=issue_num, description=description,
        page_count=page_count, series=series, number_of_characters=number_of_characters, number_of_creators=number_of_creators,
        number_of_stories=number_of_stories)

        character_ids = []
        for character in json_data[u'characters'][u'items']:
            character_ids.append(int(character[u'resourceURI'].split('/characters/')[1]))

        creator_ids = []
        for creator in json_data[u'creators'][u'items']:
            creator_ids.append(int(creator[u'resourceURI'].split('/creators/')[1]))

        for character_id in character_ids:
            character = Character.query.filter_by(id=character_id).first()
            if character:
                comic.characters.append(character)

        for creator_id in creator_ids:
            creator = Creator.query.filter_by(id=creator_id).first()
            if creator:
                comic.creators.append(creator)

        db.session.add(comic)
        logger.debug('Added %s', comic)
        db.session.commit()

def add_creator(json_data):
    id = json_data[u'id']
    thumbnail = json_data[u'thumbnail'][u'path']+'.' +json_data[u'thumbnail'][u'extension']
    first_name = json_data[u'firstName']
    last_name = json_data[u'lastName']
    number_of_comics = json_data[u'comics'][u'available']
    number_of_stories = json_data[u'stories'][u'available']
    number_of_series = json_data[u'series'][u'available']

    creator_test = Creator.query.filter_by(id=id).first()
    if not creator_test:
        creator = Creator(id=id, thumbnail=thumbnail, first_name=first_name, last_name=last_name,
        number_of_comics=number_of_comics, number_of_series=number_of_series,
        number_of_stories=number_of_stories)

        comic_ids = []
        for comic in json_data[u'comics'][u'items']:
            comic_ids.append(int(comic[u'resourceURI'].split('/comics/')[1]))

        for comic_id in comic_ids:
            comic = Comic.query.filter_by(id=comic_id).first()
            if comic:
                creator.comics.append(comic)

        db.session.add(creator)
        logger.debug('Added %s', creator)
        db.session.commit()

def update_character(json_data):
    id = json_data[u'id']
    character = Character.query.filter_by(id=id).first()
    logger.debug(character)
    if character:
        comic_ids = []
        for comic in json_data[u'comics'][u'items']:
            comic_ids.append(int(comic[u'resourceURI'].split('/comics/')[1]))

        for comic_id in comic_ids:
            comic = Comic.query.filter_by(id=comic_id).first()
            if comic and comic not in character.comics:
                character.comics.append(comic)

        logger.debug('Updated %s', character)
        db.session.commit()

def update_comic(json_data):
    id = json_data[u'id']
    comic = Comic.query.filter_by(id=id).first()

    if comic:
        character_ids = []
        for character in json_data[u'characters'][u'items']:
            character_ids.append(int(character[u'resourceURI'].split('/characters/')[1]))

        creator_ids = []
        for creator in json_data[u'creators'][u'items']:
            creator_ids.append(int(creator[u'resourceURI'].split('/creators/')[1]))

        for character_id in character_ids:
            character = Character.query.filter_by(id=character_id).first()
            if character and character not in comic.characters:
                comic.characters.append(character)

        for creator_id in creator_ids:
            creator = Creator.query.filter_by(id=creator_id).first()
            if creator and creator not in comic.creators:
                comic.creators.append(creator)

        logger.debug('Updated %s', comic)
        db.session.commit()

def update_creator(json_data):
    id = json_data[u'id']
    creator = Creator.query.filter_by(id=id).first()

    if creator:
        comic_ids = []
        for comic in json_data[u'comics'][u'items']:
            comic_ids.append(int(comic[u'resourceURI'].split('/comics/')[1]))

        for comic_id in comic_ids:
            comic = Comic.query.filter_by(id=comic_id).first()
            if comic and comic not in creator.comics:
                creator.comics.append(comic)

        logger.debug('Updated %s', creator)
        db.session.commit()
