# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    """
    Alkuvalikko ohjaa joko opettajan tai oppilaan alkusivulle, sen mukaan
    kumpaan ryhmään sisäänkirjautunut käyttäjä kuuluu.
    """



    #ohjaus opettajan tai oppilaan alkusivulle
    if (auth.has_membership(auth.id_group('opettaja'),auth.user.id)):
        redirect(URL('opettaja','opettaja_alkusivu'))
    elif (auth.has_membership(auth.id_group('opiskelija'),auth.user.id)):
        redirect(URL('opiskelija','opiskelija_kaikki_kurssit'))
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




