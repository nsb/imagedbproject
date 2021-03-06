# -*- coding: utf-8 -*-

# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.


from django.db.models import signals

from models import Location, Installation, People, HSE, Graphics, Communications, Archive, Year
import models

def create_category_values(app, created_models, verbosity, **kwargs):
    """
    create default category values
    """

    # locations
    Location.objects.get_or_create(name="Algeria - Hydra")
    Location.objects.get_or_create(name="Angola - Luanda")
    Location.objects.get_or_create(name="Brazil - Rio de Janeiro")
    Location.objects.get_or_create(name="Denmark - All")
    Location.objects.get_or_create(name="Denmark - Baltikavej Lab")
    Location.objects.get_or_create(name="Denmark - Copenhagen")
    Location.objects.get_or_create(name="Denmark - Esbjerg")
    Location.objects.get_or_create(name="Denmark - M-PACT Center")
    Location.objects.get_or_create(name="Germany")
    Location.objects.get_or_create(name="Kazakhstan - Almaty")
    Location.objects.get_or_create(name="Morocco")
    Location.objects.get_or_create(name="Norway - Stavanger")
    Location.objects.get_or_create(name="Oman - Muscat")
    Location.objects.get_or_create(name="Qatar - Doha")
    Location.objects.get_or_create(name="Turkmenistan - Ashgabat")
    Location.objects.get_or_create(name="United Kingdom - Aberdeen")
    Location.objects.get_or_create(name="United States - Houston")

    # installations & vessels
    Installation.objects.get_or_create(name="Affleck, UK")
    Installation.objects.get_or_create(name="Al Shaheen, QA")
    Installation.objects.get_or_create(name="Dan, DK")
    Installation.objects.get_or_create(name="Dagmar, DK")
    Installation.objects.get_or_create(name="Dumbarton, UK")
    Installation.objects.get_or_create(name="Dunga, KZ")
    Installation.objects.get_or_create(name="El Kheit et Tessekha, AO")
    Installation.objects.get_or_create(name="El Merk, AO")
    Installation.objects.get_or_create(name="Gorm, DK")
    Installation.objects.get_or_create(name="Gryphon, UK")
    Installation.objects.get_or_create(name="Halfdan, DK")
    Installation.objects.get_or_create(name="Harald, DK")
    Installation.objects.get_or_create(name="Hassi Berkine, AO")
    Installation.objects.get_or_create(name="James, UK")
    Installation.objects.get_or_create(name="Janice, UK")
    Installation.objects.get_or_create(name="Kraka, DK")
    Installation.objects.get_or_create(name="Ourhoud, AO")
    Installation.objects.get_or_create(name="Qoubba, AO")
    Installation.objects.get_or_create(name="Regnar")
    Installation.objects.get_or_create(name="Rhourde Berkine, AO")
    Installation.objects.get_or_create(name="Roar, DK")
    Installation.objects.get_or_create(name="Rolf, DK")
    Installation.objects.get_or_create(name="Saigak, KZ")
    Installation.objects.get_or_create(name="Skjold, DK")
    Installation.objects.get_or_create(name="Svend, DK")
    Installation.objects.get_or_create(name="Tullic, UK")
    Installation.objects.get_or_create(name="Tyra, DK")
    Installation.objects.get_or_create(name="Valdemar, DK")
    Installation.objects.get_or_create(name="Unique Installations")
    Installation.objects.get_or_create(name="Vessels")
    Installation.objects.get_or_create(name="ENSCO 101. DK")

    # people
    People.objects.get_or_create(name="Office")
    People.objects.get_or_create(name="Offshore")
    People.objects.get_or_create(name="Onshore")
    People.objects.get_or_create(name="Tech/Lab")

    # hse
    HSE.objects.get_or_create(name="Environment")
    HSE.objects.get_or_create(name="Health & Safety")

    # graphics
    Graphics.objects.get_or_create(name="Environment")
    Graphics.objects.get_or_create(name="Events")
    Graphics.objects.get_or_create(name="Health & Safety")
    Graphics.objects.get_or_create(name="Innovation")
    Graphics.objects.get_or_create(name="Logos")
    Graphics.objects.get_or_create(name="Maps")
    Graphics.objects.get_or_create(name="Publications")
    Graphics.objects.get_or_create(name="Satellite")
    Graphics.objects.get_or_create(name="Seismic")
    Graphics.objects.get_or_create(name="Technology")
    Graphics.objects.get_or_create(name="Effect photos")

    # communications
    Communications.objects.get_or_create(name="Maersk Brochure")
    Communications.objects.get_or_create(name="Management Photos")
    Communications.objects.get_or_create(name="Visual Identity")
    Communications.objects.get_or_create(name="Employee Events")
    Communications.objects.get_or_create(name="Offshore Visit")

    # archive
    Archive.objects.get_or_create(id=1, name="Colombia")
    Archive.objects.get_or_create(id=2, name="Kazakhstan")

    # year
    Year.objects.get_or_create(name="1985")
    Year.objects.get_or_create(name="1986")
    Year.objects.get_or_create(name="1987")
    Year.objects.get_or_create(name="1988")
    Year.objects.get_or_create(name="1989")
    Year.objects.get_or_create(name="1990")
    Year.objects.get_or_create(name="1991")
    Year.objects.get_or_create(name="1992")
    Year.objects.get_or_create(name="1993")
    Year.objects.get_or_create(name="1994")
    Year.objects.get_or_create(name="1995")
    Year.objects.get_or_create(name="1996")
    Year.objects.get_or_create(name="1997")
    Year.objects.get_or_create(name="1998")
    Year.objects.get_or_create(name="1999")
    Year.objects.get_or_create(name="2001")
    Year.objects.get_or_create(name="2002")
    Year.objects.get_or_create(name="2003")
    Year.objects.get_or_create(name="2004")
    Year.objects.get_or_create(name="2005")
    Year.objects.get_or_create(name="2006")
    Year.objects.get_or_create(name="2007")
    Year.objects.get_or_create(name="2008")
    Year.objects.get_or_create(name="2009")

signals.post_syncdb.connect(create_category_values, sender=models)
