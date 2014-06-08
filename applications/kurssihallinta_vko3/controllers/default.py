# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def index():
    """

    """
    if (auth.has_membership(auth.id_group('opettaja'),auth.user.id)):
        redirect(URL('opettaja_kaikki_kurssit'))
    elif (auth.has_membership(auth.id_group('oppilas'),auth.user.id)):
        redirect(URL('oppilas_kaikki_kurssit'))
    else:
        redirect(URL('oppilas_kaikki_kurssit'))
    return dict(message=T('Hello World'))

#@auth.requires_login()
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@auth.requires_membership('opettaja')
def opettaja_kaikki_kurssit():
    """
    Opettajan kaikki kurssit
    """
    kurssit = db().select(db.kurssi.ALL, orderby=db.kurssi.title)
    oppilaita_kurssilla = db(db.kurssi.id > 0).count()
    response.menu=[['omat kurssit',False,URL('opettaja_kaikki_kurssit')]]

    return dict(kurssit=kurssit,oppilaita_kurssilla=oppilaita_kurssilla)

#@auth.requires_membership('opettaja')
def opettaja_yksi_kurssi():
    """
    Opettajan yksi kurssi
    """
    kurssit = db().select(db.kurssi.ALL, orderby=db.kurssi.title)
    oppilaita_kurssilla = db(db.kurssi.id > 0).count()
    return dict(kurssit=kurssit,oppilaita_kurssilla=oppilaita_kurssilla)

#@auth.requires_membership('oppilas')
def oppilas_kaikki_kurssit():
    """
    Oppilaan kaikki kurssit
    """
    kurssit = db().select(db.kurssi.ALL, orderby=db.kurssi.title)
    oppilaita_kurssilla = db(db.kurssi.id > 0).count()
    return dict(kurssit=kurssit,oppilaita_kurssilla=oppilaita_kurssilla)


#@auth.requires_membership('oppilas')
def oppilas_yksi_kurssi():
    """
    Oppilaan yksi kurssi
    """
    kurssit = db().select(db.kurssi.ALL, orderby=db.kurssi.title)
    oppilaita_kurssilla = db(db.kurssi.id > 0).count()
    return dict(kurssit=kurssit,oppilaita_kurssilla=oppilaita_kurssilla)

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


#@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
