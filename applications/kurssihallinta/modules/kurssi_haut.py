# -*- coding: utf-8 -*-

#kurssiin liittyvät tietokantahaut
from gluon.sqlhtml import SQLFORM
from gluon.html import INPUT

def hae_kurssin_kurssityot(kurssi_ids, db):
    #haetaan tietokannasta kaikki kurssin kurssityöt
    query = db.kurssityo.kurssi_id.belongs(kurssi_ids)
    #return SQLFORM.grid(query)
    #return SQLFORM.grid(query, selectable=lambda row: INPUT(_name='actioned',_type="checkbox",_value=id))
    #return db(query).select()
    return SQLFORM.grid(query)

def hae_kurssin_nimi(kurssi_ids, db):
    #haetaan tietokannasta kaikki kurssin kurssityöt
    query = db.kurssi.id.belongs(kurssi_ids)
    return db(query).select(db.kurssi.title)
