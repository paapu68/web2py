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

    query = opiskelija_haut.hae_opiskelijan_kaikki_kurssit(db)

    form_lisaa = FORM('Lisää työ:',
                         SELECT('Lisää!',
                                _name="my_selector"),
                         INPUT(_type='submit'))
    form = SQLFORM.grid(query,create=False,searchable=False)

    response.view = 'opiskelija/opiskelija_kaikki_kurssit.html'


    if form_lisaa.process().accepted:
        #print "LISATAAN !!!"
        redirect(URL('opiskelija_lisaa_kurssityo'))

    return dict(form=form, form_lisaa=form_lisaa)


@auth.requires_membership('opiskelija')
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


@auth.requires_membership('opiskelija')
def opiskelija_lisaa_kurssityo():
    """
    Opiskelija voi lisätä yhden kurssityön
    """
    from gluon.tools import Auth
    auth = Auth(db)
# xxx alasvetovalikon rajoitus ei vielä toimi xxx
#    print "opiskelija id", \
#    db(db.opiskelija.user_id == auth.user_id).select(db.opiskelija.id)
#    current_opiskelija = \
#        db(db.opiskelija.user_id == auth.user_id).select(db.opiskelija)
#    query = (db.kurssityo.opiskelija_id==current_opiskelija)
#    db.kurssityo.property.requires=IS_IN_DB(db(query)) 
#    db.kurssityo.opiskelija_id.requires=IS_IN_DB(db(query),'kurssityo.id') 
    form = SQLFORM(db.kurssityo,fields = ['nimi_id','palautettu','opiskelija_id'])
    if form.process().accepted:
        print form.vars.id
        #db.kurssityo[form.vars.id] = dict(opiskelija_id=current_opiskelija)
        #db.kurssityo[form.vars.id] = dict(kurssi_id=1)
    return dict(form=form)
