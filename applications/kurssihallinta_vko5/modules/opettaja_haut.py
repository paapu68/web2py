# -*- coding: utf-8 -*-

#opettajaan liittyvät tietokantahaut
from gluon.sqlhtml import SQLFORM
from gluon.html import INPUT

#@auth.requires_membership('opettaja')
def hae_opettajan_kaikki_kurssit(db):
    """haetaan tietokannasta opettajan kaikkien kurssien kurssityöt"""
    from gluon.tools import Auth
    auth = Auth(db)
    print "haetaan open kurssit", auth.user_id
    query = \
        (db.opettaja.user_id == auth.user_id)&\
        (db.kurssi.opettaja_id == db.opettaja.id)
#        (db(db.opettaja.user_id == auth.user_id))&\

        
#    selectable = lambda ids: nayta(ids)
    return query
#    return SQLFORM.grid(query,
#                        selectable=selectable)
#    return db(query).select()


