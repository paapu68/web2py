# -*- coding: utf-8 -*-
#reload modules
from gluon.custom_import import track_changes; track_changes(True)
import opettaja  #tietokantahaut ../modules/opettaja.py

#import opettajan_haut #../models/opettajan_haut.py

@auth.requires_membership('opettaja')
def kaikki_kurssit():
    """
    Opettajan kaikki kurssit
    """
    import sys

    opettajan_kurssit = opettaja.hae_opettajan_kaikki_kurssit(db)
    oppilaita_kurssilla = []
    #tehdään fake-database käyttäen haettujen kurssien nimiä
    #jotta saadaan ne alasvetovalikkoon
    db.define_table('valitsekurssi',
                    Field('kurssin_nimi'),
                    format = '%(kurssin_nimi)s'
                    )
    kurssi_idt = []
    for rivi in opettajan_kurssit:
        db.valitsekurssi.insert(kurssin_nimi=rivi.kurssi.title)
        print rivi.kurssi.id
        kurssi_idt.append(rivi.kurssi.id)

    form = SQLFORM.factory(
        Field('kurssin_nimi', requires=IS_IN_DB(db, 
                                        db.valitsekurssi.id,
                                        '%(kurssin_nimi)s', zero=None)))

    response.view = 'opettaja/opettaja_kaikki_kurssit.html'


    if form.process().accepted:
        print "HYVÄKSYTTY", form.vars.kurssin_nimi
        kurssi_id_tmp = int(form.vars.kurssin_nimi)-1
        kurssi_id = kurssi_idt[kurssi_id_tmp]
        form.vars.kurssin_nimi = kurssi_id
        print "HYVÄKSYTTY222", form.vars.kurssin_nimi

        #pitää pudottaa fake-tietokantataulu pois 
        # jottei se kasva kokoajan
        db.valitsekurssi.drop()
        redirect(URL('yksi_kurssi',vars=dict(kurssi_id=kurssi_id)))


    return dict(opettajan_kurssit=opettajan_kurssit,
                oppilaita_kurssilla=oppilaita_kurssilla,
                form=form)

#@auth.requires_membership('opettaja')
def yksi_kurssi():
    """
    Opettajan yksi kurssi
    """
    opettajan_kurssin_kurssityot = \
        opettaja.hae_kurssin_kurssityot(request.vars.kurssi_id, db)
    opettajan_kurssin_nimi = \
        opettaja.hae_kurssin_nimi(request.vars.kurssi_id, db)
    print "opettajan_kurssin_nimi", opettajan_kurssin_nimi[0].values()
    opettajan_kurssin_nimi = opettajan_kurssin_nimi[0].values()[0]

    print "kurssiID", request.vars.kurssi_id
    #print "opettajan_kurssin_kurssityot", opettajan_kurssin_kurssityot
    oppilaita_kurssilla = 1
    response.view = 'opettaja/opettaja_yksi_kurssi.html'

    return dict(opettajan_kurssin_kurssityot=opettajan_kurssin_kurssityot,
                opettajan_kurssin_nimi = opettajan_kurssin_nimi)
