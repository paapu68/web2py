# -*- coding: utf-8 -*-

#opettajaan liittyvät tietokantahaut
from gluon.sqlhtml import SQLFORM
from gluon.html import INPUT


#@auth.requires_membership('opettaja')
def hae_opettaja(db):
    """ haetaan sisäänkirjautuneen käyttäjän opettajaidentiteetti """
    from gluon.tools import Auth
    auth = Auth(db)
    query = db(db.opettaja.user_id == auth.user_id)
    sid = query.select(db.opettaja.id)[0].id
    return sid

#@auth.requires_membership('opettaja')
def hae_opettajan_kaikki_kurssit(db):
    """haetaan tietokannasta opettajan kaikkien kurssien kurssityöt"""
    from gluon.tools import Auth
    auth = Auth(db)

    query = \
        (db.opettaja.user_id == auth.user_id)&\
        (db.kurssi.opettaja_id == db.opettaja.id)
    return query


