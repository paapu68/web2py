# -*- coding: utf-8 -*-
#reload modules
from gluon.custom_import import track_changes; track_changes(True)
import opettaja_haut  #tietokantahaut ../modules/opettaja_haut.py
import kurssi_haut  #tietokantahaut ../modules/kurssi_haut.py

#import opettajan_haut #../models/opettajan_haut.py

def ohjaa_kursseille(kurssi_ids):
    redirect(URL('yksi_kurssi',vars=dict(kurssi_ids=kurssi_ids)))


@auth.requires_membership('opettaja')
def kaikki_kurssit():
    """
    Opettajan kaikki kurssit
    """
    import sys
    query = opettaja_haut.hae_opettajan_kaikki_kurssit(db)
    
    form = SQLFORM.grid(query, 
                        field_id = db.kurssi.id,
                        fields = [db.kurssi.title],
                        selectable = lambda ids: ohjaa_kursseille(ids))

    oppilaita_kurssilla = []
    #tehdään fake-database käyttäen haettujen kurssien nimiä
    #jotta saadaan ne alasvetovalikkoon
    #db.define_table('valitsekurssi',
    #                Field('kurssin_nimi'),
    #                format = '%(kurssin_nimi)s'
    #                )
    #kurssi_idt = []
    #for rivi in opettajan_kurssit:
    #    db.valitsekurssi.insert(kurssin_nimi=rivi.kurssi.title)
    #    print rivi.kurssi.id
    #    kurssi_idt.append(rivi.kurssi.id)

    #form = SQLFORM.factory(
    #    Field('kurssin_nimi', requires=IS_IN_DB(db, 
    #                                    db.valitsekurssi.id,
    #                                    '%(kurssin_nimi)s', zero=None)))

    

    response.view = 'opettaja/opettaja_kaikki_kurssit.html'


    #if form.process().accepted:
    #    print "HYVÄKSYTTY", form.vars.kurssin_nimi
    #    kurssi_id_tmp = int(form.vars.kurssin_nimi)-1
    #    kurssi_id = kurssi_idt[kurssi_id_tmp]
    #    form.vars.kurssin_nimi = kurssi_id
    #    print "HYVÄKSYTTY222", form.vars.kurssin_nimi

    #    #pitää pudottaa fake-tietokantataulu pois 
    #    # jottei se kasva kokoajan
    #    db.valitsekurssi.drop()
    #    redirect(URL('yksi_kurssi',vars=dict(kurssi_id=kurssi_id)))


    return dict(form=form)

def string2lista(ids):
    #tehdään kurssi id:stä lista jos se on string (eli vain yksi id)
    if (isinstance(ids, basestring)):
        ids_lista = ids.split()
    else:
        ids_lista = ids
    print "MUUTETUT kurssi_ids", ids_lista
    return ids_lista


#@auth.requires_membership('opettaja')
def yksi_kurssi():
    """
    Opettajan yksi kurssi
    """
    
    print "request.vars.kurssi_ids_lista",request.vars.kurssi_ids
    ids = string2lista(request.vars.kurssi_ids)
    
    opettajan_kurssin_kurssityot = \
        kurssi_haut.hae_kurssin_kurssityot(ids, db)
    opettajan_kurssin_nimi = \
        kurssi_haut.hae_kurssin_nimi(ids, db)
    #print "opettajan_kurssin_nimi", opettajan_kurssin_nimi[0].values()
    #opettajan_kurssin_nimi = opettajan_kurssin_nimi[0].values()[0]

    print "kurssiID", ids
    #print "opettajan_kurssin_kurssityot", opettajan_kurssin_kurssityot
    oppilaita_kurssilla = 1
    response.view = 'opettaja/opettaja_yksi_kurssi.html'


    return dict(opettajan_kurssin_kurssityot=opettajan_kurssin_kurssityot,
                opettajan_kurssin_nimi = opettajan_kurssin_nimi)
