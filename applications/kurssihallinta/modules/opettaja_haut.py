# -*- coding: utf-8 -*-

#opettajaan liittyvät tietokantahaut
from gluon.sqlhtml import SQLFORM
from gluon.html import INPUT

#@auth.requires_membership('opettaja')
def hae_opettajan_kaikki_kurssit(db):
    #haetaan tietokannasta kaikki opettajan kurssit
    query = (db.opettaja.id == db.auth_user.id)&\
        (db.kurssi.opettaja_id == db.opettaja.id)
    return db(query).select()


