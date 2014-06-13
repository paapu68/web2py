# -*- coding: utf-8 -*-

#oppilaaseen liittyvät tietokantahaut
from gluon.sqlhtml import SQLFORM
from gluon.html import INPUT


#@auth.requires_membership('oppilas')
def hae_opiskelijan_kaikki_kurssit(db):
    """haetaan tietokannasta kaikki opiskelijan kurssit"""
    from gluon.tools import Auth
    auth = Auth(db)
    query = (db.opiskelija.user_id == auth.user_id)&\
        (db.kurssityo.opiskelija_id == db.opiskelija.id)
    return query
    #return db(query).select()


