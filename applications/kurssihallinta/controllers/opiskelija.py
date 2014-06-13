# -*- coding: utf-8 -*-
#reload modules
from gluon.custom_import import track_changes; track_changes(True)
import opiskelija_haut  #tietokantahaut ../modules/opiskelija_haut.py
import kurssi_haut  #tietokantahaut ../modules/kurssi_haut.py

@auth.requires_membership('opiskelija')
def opiskelija_kaikki_kurssit():
    """
    Opiskelijan kaikki kurssit. Niitä voi editoida, tuhota tai katsoa.
    """
    import sys

    query = opiskelija_haut.hae_opiskelijan_kaikki_kurssit(db)

    form_lisaa = FORM('Lisää työ:',
                         SELECT('Lisää!',
                                _name="my_selector"),
                         INPUT(_type='submit'))
    default_sort_order=[db.kurssityo.kurssi_id]
    fields = (db.kurssityo.nimi_id,db.kurssityo.palautettu, 
              db.kurssityo.korjattu,db.kurssityo.arvosana,
              db.kurssityo.kurssi_id)
    headers = {'kurssityo.nimi_id':   'Kurssityö',
               'kurssityo.palautettu':   'Palautettu',
               'kurssityo.korjattu':   'Korjattu',
               'kurssityo.arvosana':   'Arvosana',
               'kurssityo.kurssi_id':   'Kurssi'}               
    form = SQLFORM.grid(query,create=False,searchable=False,
                        orderby=default_sort_order,
                        fields=fields, headers=headers)

    response.view = 'opiskelija/opiskelija_kaikki_kurssit.html'

    if form_lisaa.process().accepted:
        #print "LISATAAN !!!"
        redirect(URL('opiskelija_lisaa_kurssityo'))

    return dict(form=form, form_lisaa=form_lisaa)

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
        redirect(URL('opiskelija_kaikki_kurssit'))
    return dict(form=form)
