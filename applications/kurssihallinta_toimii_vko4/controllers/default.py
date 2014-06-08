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
        redirect(URL('opettaja','kaikki_kurssit'))
    elif (auth.has_membership(auth.id_group('oppilas'),auth.user.id)):
        redirect(URL('oppilas','kaikki_kurssit'))
    else:
        redirect(URL('default','user'))
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
