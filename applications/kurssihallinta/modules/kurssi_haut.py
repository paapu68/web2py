# -*- coding: utf-8 -*-

#kurssiin liittyvät tietokantahaut
from gluon.sqlhtml import SQLFORM
from gluon.html import INPUT

def hae_kurssin_kurssityot(kurssi_ids, db):
    """haetaan tietokannasta kaikki kurssin kurssityöt
    haetaan samalla opiskelijoiden identiteetit"""
    query = \
        db.kurssityo.kurssi_id.belongs(kurssi_ids)
    return query

def hae_kurssin_kurssitoiden_otsikot(kurssi_ids, db):
    """Haetaan tietokannasta kaikki kurssin/kurssien kurssitöiden otsikot.
    Näitä opettaja voi muokata. """
    query = db.kurssityon_nimi.kurssi_id.belongs(kurssi_ids)
    return query

def hae_kursseja(kurssi_ids, db):
    """  Haetaan lista kursseja kurssityon_nimi taulusta """
    query = db.kurssityon_nimi.kurssi_id.belongs(kurssi_ids)
    return query
    #return db(query).select(db.kurssityon_nimi.kurssi_id)

def hae_kurssit(kurssi_ids, db):
    """  Haetaan tietokannasta kaikki kurssin kurssityöt """
    query = db.kurssi.id.belongs(kurssi_ids)
    return db(query).select(db.kurssi.title)

def hae_kurssinimen_kurssi_id(last_row, db):
    """ haetaan tietokannasta mille kurssille kurssityö kuuluu """
    query = db(last_row.kurssityon_nimi == db.kurssityon_nimi.id)
    kid = query.select(db.kurssityon_nimi.kurssi_id)[0].kurssi_id
    return kid
