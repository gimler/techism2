 #!/usr/local/bin/python
 # -*- coding: utf-8 -*-
import unittest
from techism2.migration import MixxtParser


class MigrationTest(unittest.TestCase):
    
    def test_parse_event_links_index(self):
        links = self._parse_event_links("mixxt_events_index.html")
        self.assertEquals(len(links), 33)
        self.assertEquals(links[0], "http://techism.mixxt.de/networks/events/show_event.27414")
        self.assertEquals(links[32], "http://techism.mixxt.de/networks/events/show_event.13290")
    
    def test_parse_event_links_archive_first_page(self):
        links = self._parse_event_links("mixxt_events_archive1.html")
        self.assertEquals(len(links), 20)
    
    def test_parse_event_links_archive_last_page(self):
        links = self._parse_event_links("mixxt_events_archive32.html")
        self.assertEquals(len(links), 4)
    
    def _parse_event_links(self, file):
        parser = MixxtParser()
        stream = open("techism2/tests/"+file)
        links = parser.parse_event_links(stream)
        stream.close()
        return links
    
    def test_parse_event_osm(self):
        event = self._parse_event("mixxt_event_osm.html")
        self.assertEquals(len(event), 6)
        self.assertEquals(event['title'], u"OpenStreetMap-Treff")
        self.assertEquals(event['description'], u"<p>Regelmäßiges Treffen für interessierte OpenStreetMap-Nutzer.</p>")
        self.assertEquals(event['url'], u"http://wiki.openstreetmap.org/index.php/M%C3%BCnchen")
        self.assertEquals(event['begin'], u"20101019T190000")
        self.assertEquals(event['end'], None)
        self.assertEquals(len(event['location']), 3)
        self.assertEquals(event['location']['name'], u"Bärenwirt, Neuhausen")
        self.assertEquals(event['location']['street'], u"Wendl-Dietrich-Str. 24")
        self.assertEquals(event['location']['city'], u"München")
    
    def test_parse_event_barcamp(self):
        event = self._parse_event("mixxt_event_barcamp.html")
        self.assertEquals(len(event), 6)
        self.assertEquals(event['title'], u"Barcamp Munich 2010")
        self.assertEquals(event['description'], None)
        self.assertEquals(event['url'], u"http://barcampmunich.mixxt.de/")
        self.assertEquals(event['begin'], u"20101009T083000")
        self.assertEquals(event['end'], u"20101010T170000")
        self.assertEquals(len(event['location']), 3)
        self.assertEquals(event['location']['name'], None)
        self.assertEquals(event['location']['street'], None)
        self.assertEquals(event['location']['city'], None)
    
    def test_parse_event_da(self):
        event = self._parse_event("mixxt_event_da.html")
        self.assertEquals(len(event), 6)
        self.assertEquals(event['title'], u"Digital.Analog 6 1/2")
        self.assertEquals(event['description'].find(u"18.10.08 - EINTRITT FREI"), 0)
        self.assertEquals(event['description'].rfind(u"Sehtest"), 956)
        self.assertEquals(event['url'], u"http://www.digitalanalog.org/")
        self.assertEquals(event['begin'], u"20081018T180000")
        self.assertEquals(event['end'], None)
        self.assertEquals(len(event['location']), 3)
        self.assertEquals(event['location']['name'], None)
        self.assertEquals(event['location']['street'], None)
        self.assertEquals(event['location']['city'], None)
    
    def test_parse_event_ele(self):
        event = self._parse_event("mixxt_event_ele.html")
        self.assertEquals(len(event), 6)
        self.assertEquals(event['title'], u"electronica 2010")
        self.assertEquals(event['description'], None)
        self.assertEquals(event['url'], u"http://www.electronica.de/de/home")
        self.assertEquals(event['begin'], u"20101109")
        self.assertEquals(event['end'], u"20101112")
        self.assertEquals(len(event['location']), 3)
        self.assertEquals(event['location']['name'], None)
        self.assertEquals(event['location']['street'], None)
        self.assertEquals(event['location']['city'], None)
    
    def test_parse_event_mongo(self):
        event = self._parse_event("mixxt_event_mongo.html")
        self.assertEquals(len(event), 6)
        self.assertEquals(event['title'], u"Mongo Munich")
        #self.assertEquals(event['description'].find(u"Es gibt ja nicht nur"), 0)
        #self.assertEquals(event['description'].rfind(u"Party am Abend"), 956)
        self.assertEquals(event['url'], u"http://www.10gen.com/conferences/mongomunich2010")
        self.assertEquals(event['begin'], u"20101006T120000")
        self.assertEquals(event['end'], u"20101006T170000")
        self.assertEquals(len(event['location']), 3)
        self.assertEquals(event['location']['name'], u"The Westin Grand Munich")
        self.assertEquals(event['location']['street'],u"Arabellastrasse 6")
        self.assertEquals(event['location']['city'], u"81925 München")
    
    def test_to_json(self):
        from django.utils import simplejson as json
        event = self._parse_event("mixxt_event_mongo.html")
        dump = json.dumps(event)
        restoredEvent = json.loads(dump)
        self.assertEquals(event, restoredEvent)
    
    def _parse_event(self, file):
        parser = MixxtParser()
        stream = open("techism2/tests/"+file)
        event = parser.parse_event(stream)
        stream.close()
        return event

def suite():
    return unittest.TestLoader().loadTestsFromName(__name__)
