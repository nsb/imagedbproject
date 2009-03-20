# -*- coding: utf-8 -*-

# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.


from django.db.models import signals

from models import Location, Field, Installation, People, HSE, Event, Graphics, Communications, Archive
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

    # fields
    Field.objects.get_or_create(name="Affleck, UK")
    Field.objects.get_or_create(name="Al Shaheen, QA")
    Field.objects.get_or_create(name="Dan, DK")
    Field.objects.get_or_create(name="Dagmar, DK")
    Field.objects.get_or_create(name="Dumbarton, UK")
    Field.objects.get_or_create(name="Dunga, KZ")
    Field.objects.get_or_create(name="El Kheit et Tessekha, AO")
    Field.objects.get_or_create(name="El Merk, AO")
    Field.objects.get_or_create(name="Gorm, DK")
    Field.objects.get_or_create(name="Gryphon, UK")
    Field.objects.get_or_create(name="Halfdan, DK")
    Field.objects.get_or_create(name="Harald, DK")
    Field.objects.get_or_create(name="Hassi Berkine, AO")
    Field.objects.get_or_create(name="James, UK")
    Field.objects.get_or_create(name="Janice, UK")
    Field.objects.get_or_create(name="Kraka, DK")
    Field.objects.get_or_create(name="Ourhoud, AO")
    Field.objects.get_or_create(name="Qoubba, AO")
    Field.objects.get_or_create(name="Regnar, DK")
    Field.objects.get_or_create(name="Rhourde Berkine, AO")
    Field.objects.get_or_create(name="Roar, DK")
    Field.objects.get_or_create(name="Rolf, DK")
    Field.objects.get_or_create(name="Saigak, KZ")
    Field.objects.get_or_create(name="Skjold, DK")
    Field.objects.get_or_create(name="Svend, DK")
    Field.objects.get_or_create(name="Tullich, UK")
    Field.objects.get_or_create(name="Tyra, UK")
    Field.objects.get_or_create(name="Valdemar, DK")
    Field.objects.get_or_create(name="ENSCO 101. DK")

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

    # events
    Event.objects.get_or_create(id=1, name="Conferences & Exhibitions")
    Event.objects.get_or_create(id=3, name="GeoCenter Møns Klint, DK")
    Event.objects.get_or_create(id=4, name="Official Visits")

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

    # archive
    Archive.objects.get_or_create(id=2, name="Colombia")
    Archive.objects.get_or_create(id=15, name="Suriname")

signals.post_syncdb.connect(create_category_values, sender=models)
