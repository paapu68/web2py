# -*- coding: utf-8 -*-
#reload modules
from gluon.custom_import import track_changes; track_changes(True)
import opiskelija_haut  #tietokantahaut ../modules/opiskelija_haut.py
import kurssi_haut  #tietokantahaut ../modules/kurssi_haut.py

@auth.requires_membership('opiskelija')
def kaikki_kurssit():
    """
    Opiskelijan kaikki kurssit
    """
    import sys

    opiskelijan_kurssit = opiskelija_haut.hae_opiskelijan_kaikki_kurssit(db)
    oppilaita_kurssilla = []
    #tehdään fake-database käyttäen haettujen kurssien nimiä
    #jotta saadaan ne alasvetovalikkoon
    db.define_table('valitsekurssi',
                    Field('kurssin_nimi'),
                    format = '%(kurssin_nimi)s'
                    )
    kurssi_idt = []
    for rivi in opiskelijan_kurssit:
        db.valitsekurssi.insert(kurssin_nimi=rivi.kurssi.title)
        print rivi.kurssi.id
        kurssi_idt.append(rivi.kurssi.id)

    form = SQLFORM.factory(
        Field('kurssin_nimi', requires=IS_IN_DB(db, 
                                        db.valitsekurssi.id,
                                        '%(kurssin_nimi)s', zero=None)))

    response.view = 'opiskelija/opiskelija_kaikki_kurssit.html'


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


    return dict(opiskelijan_kurssit=opiskelijan_kurssit,
                oppilaita_kurssilla=oppilaita_kurssilla,
                form=form)


#@auth.requires_membership('opiskelija')
def yksi_kurssi():
    """
    Opiskelijan yksi kurssi
    """
    opiskelijan_kurssin_kurssityot = \
        kurssi_haut.hae_kurssin_kurssityot(request.vars.kurssi_id, db)
    opiskelijan_kurssin_nimi = \
        kurssi_haut.hae_kurssin_nimi(request.vars.kurssi_id, db)
    print "opiskelijan_kurssin_nimi", opiskelijan_kurssin_nimi[0].values()
    opiskelijan_kurssin_nimi = opiskelijan_kurssin_nimi[0].values()[0]

    print "kurssiID", request.vars.kurssi_id
    #print "opiskelijan_kurssin_kurssityot", opiskelijan_kurssin_kurssityot
    oppilaita_kurssilla = 1
    response.view = 'opiskelija/opiskelija_yksi_kurssi.html'

    return dict(opiskelijan_kurssin_kurssityot=opiskelijan_kurssin_kurssityot,
                opiskelijan_kurssin_nimi = opiskelijan_kurssin_nimi)
