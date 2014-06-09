# -*- coding: utf-8 -*-

#oppilaaseen liittyvät tietokantahaut
from gluon.sqlhtml import SQLFORM
from gluon.html import INPUT

#@auth.requires_membership('oppilas')
def hae_opiskelijan_kaikki_kurssit(db):
    #haetaan tietokannasta kaikki opiskelijan kurssit
    query = (db.opiskelija.id == db.auth_user.id)&\
        (db.opiskelijatKursseilla.opiskelija_id == db.opiskelija.id)&\
        (db.opiskelijatKursseilla.kurssi_id == db.kurssi.id)
    return db(query).select()


