# -*- coding: utf-8 -*-

#opettajaan liittyvät tietokantahaut
from gluon.sqlhtml import SQLFORM

#@auth.requires_membership('opettaja')
def hae_opettajan_kaikki_kurssit(db):
    #haetaan tietokannasta kaikki opettajan kurssit
    query = (db.opettaja.id == db.auth_user.id)&\
        (db.kurssi.opettaja_id == db.opettaja.id)
    return db(query).select()

def hae_kurssin_kurssityot(kurssi_id, db):
    #haetaan tietokannasta kaikki kurssin kurssityöt
    query = (kurssi_id==db.kurssityo.kurssi_id)
    return SQLFORM.grid(query)
    #return db(query).select()

def hae_kurssin_nimi(kurssi_id, db):
    #haetaan tietokannasta kaikki kurssin kurssityöt
    query = (kurssi_id==db.kurssi.id)
    return db(query).select(db.kurssi.title)
