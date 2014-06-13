# -*- coding: utf-8 -*-
#reload modules
from gluon.custom_import import track_changes; track_changes(True)
import opettaja_haut  #tietokantahaut ../modules/opettaja_haut.py
import kurssi_haut  #tietokantahaut ../modules/kurssi_haut.py

#import opettajan_haut #../models/opettajan_haut.py

@auth.requires_membership('opettaja')
def opettaja_alkusivu():
    """ opettaja saa valita ensin 
    1) tutkii kurssitöitä
    2) lisääkö itselleen kursseja tai uusia kurssitöiden otsikoita

    """

    form=FORM('Valitse:',
              SELECT('Oppilaiden työt',
                     'Lisää kurssien/ kurssitöiden nimiä',
                     _name="my_selector"),
##                     _name="my_selector",_multiple='multiple'),
              INPUT(_type='submit')
              )

    if form.process().accepted:
        if request.vars.my_selector == 'Oppilaiden työt':
            redirect(URL('opettaja_valitse_kurssi'))
            #redirect(URL('kurssin_kurssityot'))
        elif request.vars.my_selector == 'Lisää kurssien/ kurssitöiden nimiä':
            redirect(URL('kaikki_kurssit'))
        else:
            print "BUGI"

    print request.vars.my_selector
    return dict(form=form)


def ohjaa_kurssitoiden_otsikoihin(kurssi_ids):
    print "OHJJ: kurssi_ids", kurssi_ids
    if kurssi_ids:
        redirect(URL('kurssitoiden_otsikot',vars=dict(kurssi_ids=kurssi_ids)))
    else:
        print "OHJATAAN TAKAISIN"
        #tyhjä lista
        redirect(URL('kaikki_kurssit'))

def ohjaa_kurssitoihin(kurssi_ids):
    print "OHJ: kurssi_ids", kurssi_ids
    if kurssi_ids:
        redirect(URL('kurssin_kurssityot',vars=dict(kurssi_ids=kurssi_ids)))
    else:
        print "OHJATAAN TAKAISIN"
        #tyhjä lista
        redirect(URL('kaikki_kurssit'))


@auth.requires_membership('opettaja')
def kaikki_kurssit():
    """
    Opettajan kaikki kurssit
    """
    import sys
    print "db.opettaja.id", db.opettaja.id
    print "db.auth_user.id", db.auth_user.id
    query = opettaja_haut.hae_opettajan_kaikki_kurssit(db)
    
    #kun submittia painetaan mennää sivulle ohjaa kursseille
    form = SQLFORM.grid(query, 
                        field_id = db.kurssi.id,
                        fields = [db.kurssi.title],
                        selectable = [('Valitse kurssit joihin lisäät töitä',lambda ids: ohjaa_kurssitoiden_otsikoihin(ids))])

    oppilaita_kurssilla = []

    response.view = 'opettaja/opettaja_kaikki_kurssit.html'
    return dict(form=form)

@auth.requires_membership('opettaja')
def opettaja_valitse_kurssi():
    """
    Opettaja valitsee osan kursseistaan
    """
    import sys
    print "db.opettaja.id", db.opettaja.id
    print "db.auth_user.id", db.auth_user.id
    query = opettaja_haut.hae_opettajan_kaikki_kurssit(db)
    
    #kun submittia painetaan mennää sivulle ohjaa kursseille
    form = SQLFORM.grid(query, 
                        field_id = db.kurssi.id,
                        fields = [db.kurssi.title],
                        selectable = [('Valitse tarkastettavat kurssit',lambda ids: ohjaa_kurssitoihin(ids))])

    oppilaita_kurssilla = []

    response.view = 'opettaja/opettaja_kaikki_kurssit.html'
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
def kurssitoiden_otsikot():
    """
    Opettajan kurssin kurssitöiden otsikot. 
    Tässä voi lisätä myös uusia kurssitöitä
    """
    
    print "request.vars.kurssi_ids_lista",request.vars.kurssi_ids
    kurssit_ids = string2lista(request.vars.kurssi_ids)
    session.kurssit_ids = kurssit_ids

    query1 = kurssi_haut.hae_kurssin_kurssitoiden_otsikot(kurssit_ids, db)
    
    #kurssin kurssitöiden otsikot opettajan muokattavaksi/ lisättäväksi
    grid1 = SQLFORM.grid(query1)

    print "kurssiID", kurssit_ids
    #print "opettajan_kurssin_kurssityot", opettajan_kurssin_kurssityot

    response.view = 'opettaja/kurssitoiden_otsikot.html'


    return dict(grid1 = grid1)

#@auth.requires_membership('opettaja')
def kurssin_kurssityot():
    """
    Valittuun/valittuihin kurssiin/kursseihin liittyvat kurssityot.
    """
    #print "KURSSITYÖT: request.vars.kurssi_ids_lista",request.vars.kurssi_ids
    #global kurssit_ids
    #kurssit_ids = string2lista(request.vars.kurssi_ids)
    print "request.vars.kurssi_ids_lista",request.vars.kurssi_ids
    kurssit_ids = string2lista(request.vars.kurssi_ids)
    print "AAAxxx:",kurssit_ids
    

    #if grid2:
    #    redirect(URL('kurssitoiden_otsikot'))

    query2 = kurssi_haut.hae_kurssin_kurssityot(kurssit_ids, db)
    
    grid2 = SQLFORM.grid(query2)

    #print "opettajan_kurssin_nimi", opettajan_kurssin_nimi[0].values()
    #opettajan_kurssin_nimi = opettajan_kurssin_nimi[0].values()[0]

    #print "opettajan_kurssin_kurssityot", opettajan_kurssin_kurssityot

    response.view = 'opettaja/kurssin_kurssityot.html'
    print "grid2.vars", dir(grid2)

    return dict(grid2 = grid2)
