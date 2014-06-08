# -*- coding: utf-8 -*-
import kurssidb

def kurssit():
    """ kurssilistaan liittyvät asiat """
    kurssit = db().select(db.kurssi.ALL, orderby=db.kurssi.title)
    return dict(kurssit=kurssit)


