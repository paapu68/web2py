# -*- coding: utf-8 -*-

#oppilaaseen liittyvät tietokantahaut
from gluon.sqlhtml import SQLFORM
from gluon.html import INPUT
from gluon.tools import Auth



@auth.requires_membership('opiskelija')
def hae_opiskelijan_kaikki_kurssit(db):
    """haetaan tietokannasta kaikki opiskelijan kurssit"""
    auth = Auth(db)
    query = (db.opiskelija.user_id == auth.user_id)&\
        (db.kurssityo.opiskelija_id == db.opiskelija.id)
    return query

@auth.requires_membership('opiskelija')
def hae_opiskelija(db):
    """ haetaan sisäänkirjautuneen käyttäjän opiskelijaidentiteetti """
    auth = Auth(db)
    query = db(db.opiskelija.user_id == auth.user_id)
    sid = query.select(db.opiskelija.id)[0].id
    return sid
