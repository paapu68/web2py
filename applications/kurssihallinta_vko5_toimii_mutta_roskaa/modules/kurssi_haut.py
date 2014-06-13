# -*- coding: utf-8 -*-

#kurssiin liittyvät tietokantahaut
from gluon.sqlhtml import SQLFORM
from gluon.html import INPUT

def hae_kurssin_kurssityot(kurssi_ids, db):
    """haetaan tietokannasta kaikki kurssin kurssityöt
    haetaan samalla opiskelijoiden identiteetit"""
    query = \
        db.kurssityo.kurssi_id.belongs(kurssi_ids)
#        db.opiskelijatKursseilla.kurssi_id.belongs(kurssi_ids)
#        db.opiskelijatKursseilla.opiskelija_id == db.opiskelija.id
    return query

def hae_kurssin_kurssitoiden_otsikot(kurssi_ids, db):
    """Haetaan tietokannasta kaikki kurssin kurssitöiden otsikot.
    Näitä opettaja voi muokata. """
    query = db.kurssityon_nimi.kurssi_id.belongs(kurssi_ids)
    return query

def hae_kurssin_nimi(kurssi_ids, db):
    #haetaan tietokannasta kaikki kurssin kurssityöt
    query = db.kurssi.id.belongs(kurssi_ids)
    return db(query).select(db.kurssi.title)
