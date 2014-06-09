# -*- coding: utf-8 -*-

#kurssiin liittyvät tietokantahaut
from gluon.sqlhtml import SQLFORM
from gluon.html import INPUT

def hae_kurssin_kurssityot(kurssi_id, db):
    #haetaan tietokannasta kaikki kurssin kurssityöt
    query = (kurssi_id==db.kurssityo.kurssi_id)
    return SQLFORM.grid(query)
    #return SQLFORM.grid(query, selectable=lambda row: INPUT(_name='actioned',_type="checkbox",_value=id))
    #return db(query).select()

def hae_kurssin_nimi(kurssi_id, db):
    #haetaan tietokannasta kaikki kurssin kurssityöt
    query = (kurssi_id==db.kurssi.id)
    return db(query).select(db.kurssi.title)
