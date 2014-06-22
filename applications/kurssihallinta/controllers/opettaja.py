# -*- coding: utf-8 -*-
#reload modules
from gluon.custom_import import track_changes; track_changes(True)
import opettaja_haut  #tietokantahaut ../modules/opettaja_haut.py
import kurssi_haut  #tietokantahaut ../modules/kurssi_haut.py
from gluon.tools import Auth

@auth.requires_membership('opettaja')
def opettaja_alkusivu():
    """ opettaja saa valita ensin 
    1) tutkii kurssitöitä
    2) lisääkö itselleen uusia kursseja tai uusia kurssitöiden otsikoita
    """

    form=FORM('Valitse:',
              SELECT('Tarkasta oppilaiden kurssitöitä',
                     'Lisää kurssien/ kurssitöiden nimiä',
                     _name="my_selector"),
              INPUT(_type='submit')
              )

    if form.process().accepted:
        if request.vars.my_selector == 'Tarkasta oppilaiden kurssitöitä':
            redirect(URL('opettaja_valitse_kurssi'))
        elif request.vars.my_selector == 'Lisää kurssien/ kurssitöiden nimiä':
            redirect(URL('opettaja_lisaa_kursseja'))

    return dict(form=form)

@auth.requires_membership('opettaja')
def ohjaa_kurssitoiden_otsikoihin(kurssi_ids):
    """Ohjataan valittujen kurssien kurssitoiden lisaykseen """
    if kurssi_ids:
        redirect(URL('opettaja_lisaa_kurssitoita',
                     vars=dict(kurssi_ids=kurssi_ids)))
    else:
        print "OHJATAAN TAKAISIN"
        #tyhjä lista
        redirect(URL('opettaja_lisaa_kursseja'))

@auth.requires_membership('opettaja')
def ohjaa_kurssitoihin(kurssi_ids):
    """Ohjataan valittujen kurssien kurssitoiden tutkimiseen """
    if kurssi_ids:
        redirect(URL('opettaja_kurssityot',vars=dict(kurssi_ids=kurssi_ids)))
    else:
        print "OHJATAAN TAKAISIN"
        #tyhjä lista
        redirect(URL('opettaja_lisaa_kursseja'))


@auth.requires_membership('opettaja')
def opettaja_lisaa_kursseja():
    """
    Opettajan lisää kursseja tai valitsee kurssin johon lisätään töitä.
    """
    import sys
    #haetaan opettajan kaikki kurssit tietokannasta
    query = opettaja_haut.hae_opettajan_kaikki_kurssit(db)
    
    #tehdään tietokantahausta lomake
    headers = {'kurssi.title':   'Kurssi'}
    form = SQLFORM.grid(query, searchable = False, 
                        headers=headers,
                        field_id = db.kurssi.id,
                        fields = [db.kurssi.title],
                        selectable = [('Valitse kurssit joihin lisäät töitä tai joita tarkastat',lambda ids: ohjaa_kurssitoiden_otsikoihin(ids))])

    response.view = 'opettaja/opettaja_lisaa_kursseja.html'
    return dict(form=form)

@auth.requires_membership('opettaja')
def opettaja_valitse_kurssi():
    """
    Opettaja valitsee osan kursseistaan
    """
    #haetaan kaikki opettajan kurssit
    query = opettaja_haut.hae_opettajan_kaikki_kurssit(db)
    headers = {'kurssi.title':   'Kurssi'}
    #tehdään lomake jolla voidaan valita osa kursseista tai 
    # lisätä kursseja
    form = SQLFORM.grid(query,create=False,searchable=False,
                        headers = headers,
                        field_id = db.kurssi.id,
                        fields = [db.kurssi.title],
                        selectable = [('Valitse tarkastettavat kurssit',
                                       lambda ids: ohjaa_kurssitoihin(ids))]
                        )

    oppilaita_kurssilla = []

    response.view = 'opettaja/opettaja_valitse_kurssi.html'
    return dict(form=form)

def string2lista(ids):
    """ Tehdään kurssi id:stä lista jos se on string (eli vain yksi id)
    eli lopputulos on lista joka tapauksessa """
    if (isinstance(ids, basestring)):
        ids_lista = ids.split()
    else:
        ids_lista = ids
    return ids_lista

@auth.requires_membership('opettaja')
def opettaja_lisaa_kurssitoita():
    """
    Opettajan voi lisätä kurssilleen uusia töitä (eli töiden otsakkeita). 
    """
    
    kurssit_ids = string2lista(request.vars.kurssi_ids)
    session.kurssit_ids = kurssit_ids

    #haetaan valittujen kurssien kurssitöiden nimet 
    query1 = kurssi_haut.hae_kurssin_kurssitoiden_otsikot(kurssit_ids, db)
    
    #submit nappi joka johtaa kurssitöiden otsikoiden lisäykseen
    form_lisaa = FORM('', INPUT(_type='submit',
                                _value='LISÄÄ KURSSITYÖIDEN OTSIKOITA !'))
    
    #kurssin kurssitöiden otsikot opettajan muokattavaksi/ lisättäväksi
    fields = (db.kurssityon_nimi.title, db.kurssityon_nimi.kurssi_id)
    grid1 = SQLFORM.grid(query1, create = False, searchable=False, 
                         fields = fields)


    response.view = 'opettaja/opettaja_lisaa_kurssitoita.html'

    if form_lisaa.process().accepted:
        redirect(URL('opettaja_lisaa_kurssityo_otsikoita',
                     vars=dict(kurssit_ids=kurssit_ids)))

    return dict(grid1 = grid1, form_lisaa=form_lisaa)

@auth.requires_membership('opettaja')
def opettaja_kurssityot():
    """
    Valittuun/valittuihin kurssiin/kursseihin liittyvat kurssityot
    opettajan muokattavaksi.
    """

    kurssit_ids = string2lista(request.vars.kurssi_ids)

    #haetaan opettajan kursseita hänen valitsemiensa kurssien kurssityöt
    query2 = kurssi_haut.hae_kurssin_kurssityot(kurssit_ids, db)
    default_sort_order=[db.kurssityo.kurssi_id]    
    fields = (db.kurssityo.kurssityon_nimi, db.kurssityo.palautettu, 
              db.kurssityo.korjattu,db.kurssityo.arvosana,
              db.kurssityo.kurssi_id, )
    headers = {'kurssityo.kurssityon_nimi':   'Kurssityö',
               'kurssityo.palautettu':   'Palautettu',
               'kurssityo.korjattu':   'Korjattu',
               'kurssityo.arvosana':   'Arvosana',
               'kurssityo.kurssi_id':   'Kurssi',
               'kurssityo.opiskelija_id':   'Opiskelija'}    

    #tehdään sql hausta lomake
    grid2 = SQLFORM.grid(query2, create=False,searchable=False,
                         orderby=default_sort_order,
                         fields=fields, headers=headers)

    response.view = 'opettaja/opettaja_kurssityot.html'

    return dict(grid2 = grid2)


@auth.requires_membership('opettaja')
def opettaja_lisaa_kurssityo_otsikoita():
    """
    Opettaja voi lisätä kursseille uusia kurssitöiden otsikoita
    """
    from gluon.tools import Auth

    kurssit_ids = string2lista(request.vars.kurssit_ids)
    #En saanut alasvetovalikon rajoitusta toiminaan...
    #query = kurssi_haut.hae_kursseja(kurssit_ids, db)
    #db.kurssityon_nimi.kurssi_id.requires = IS_IN_DB(db(query),"kurssityon_nimi.kurssi_id")

    form = SQLFORM(db.kurssityon_nimi,
                   fields = ['title','kurssi_id'])
    auth = Auth(db)
    query = db(db.opettaja.user_id == auth.user_id)
    sid = query.select(db.opettaja.id)[0].id
    #sid = opettaja_haut.hae_opettaja(db)
    form.vars.opettaja_id = sid
    if form.process().accepted:
        redirect(URL('opettaja_alkusivu'))
    return dict(form=form)
