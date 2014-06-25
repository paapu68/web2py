# -*- coding: utf-8 -*-
#reload modules
from gluon.custom_import import track_changes; track_changes(True)
import opiskelija_haut  #tietokantahaut ../modules/opiskelija_haut.py
import kurssi_haut  #tietokantahaut ../modules/kurssi_haut.py
#from gluon.tools import Auth
#auth = Auth(db)


@auth.requires_membership('opiskelija')
def opiskelija_kaikki_kurssit():
    """
    Opiskelijan kaikki kurssit. Niitä voi editoida, tuhota tai katsoa.
    """
    import sys

    query = opiskelija_haut.hae_opiskelijan_kaikki_kurssit(db)

    form_lisaa = FORM('', INPUT(_type='submit',_value='LISÄÄ KURSSITYÖ !'))

    default_sort_order=[db.kurssityo.kurssi_id]

    form = SQLFORM.grid(query,create=False,searchable=False,
                        orderby=default_sort_order,
                        fields = (db.kurssityo.kurssityon_nimi,
                                  db.kurssityo.palautettu, 
                                  db.kurssityo.korjattu,
                                  db.kurssityo.arvosana,
                                  db.kurssityo.kurssi_id),
                        headers = {'kurssityo.kurssityon_nimi':   'Kurssityö',
                                   'kurssityo.palautettu':   'Palautettu',
                                   'kurssityo.korjattu':   'Korjattu',
                                   'kurssityo.arvosana':   'Arvosana',
                                   'kurssityo.kurssi_id':   'Kurssi'}   )

    response.view = 'opiskelija/opiskelija_kaikki_kurssit.html'

    if form_lisaa.process().accepted:
        redirect(URL('opiskelija_lisaa_kurssityo'))

    return dict(form=form, form_lisaa=form_lisaa)

@auth.requires_membership('opiskelija')
def opiskelija_lisaa_kurssityo():
    """
    Opiskelija voi lisätä yhden kurssityön
    """
# alasvetovalikon rajoituksia
    form = SQLFORM(db.kurssityo,
                   fields = ['kurssityon_nimi','palautettu'])
    sid = opiskelija_haut.hae_opiskelija(db)
    form.vars.opiskelija_id = sid
    if form.process().accepted:
        #haetaan mille kurssille kurssityö kuuluu
        #päivitetään tämä tieto tietokantaan
        rows = db(db.kurssityo).select()
        last_row = rows.last()
        kid = kurssi_haut.hae_kurssinimen_kurssi_id(last_row, db)
        last_row.update_record(kurssi_id = kid) 
        redirect(URL('opiskelija_kaikki_kurssit'))
    return dict(form=form)
