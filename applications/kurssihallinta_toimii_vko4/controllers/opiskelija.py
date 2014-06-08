# -*- coding: utf-8 -*-

#@auth.requires_membership('oppilas')
def oppilas():
    """
    Oppilaan kaikki kurssit
    """
    kurssit = db().select(db.kurssi.ALL, orderby=db.kurssi.title)
    oppilaita_kurssilla = db(db.kurssi.id > 0).count()
    response.view = 'oppilas/oppilas_kaikki_kurssit.html'
    return dict(kurssit=kurssit,oppilaita_kurssilla=oppilaita_kurssilla)


#@auth.requires_membership('oppilas')
def oppilas_yksi_kurssi():
    """
    Oppilaan yksi kurssi
    """
    kurssit = db().select(db.kurssi.ALL, orderby=db.kurssi.title)
    oppilaita_kurssilla = db(db.kurssi.id > 0).count()
    response.view = 'oppilas/oppilas_yksi_kurssi.html'
    return dict(kurssit=kurssit,oppilaita_kurssilla=oppilaita_kurssilla)
