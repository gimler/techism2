 #!/usr/local/bin/python
 # -*- coding: utf-8 -*-
import urllib2
import html5lib
from html5lib import treebuilders, treewalkers, serializer
from datetime import datetime
from django.utils import simplejson as json
from techism2.models import Event, Location

class MixxtParser:
    
    def parse_event_links(self, stream):
        """
        Parses the events index page or an archive page and retursn all the links to events.
        """
        doc = self._parse(stream)
        #print doc.toxml("utf-8")
        
        #<div class="event_text">
        #<h1><a href="/networks/events/show_event.24936" title=">
        links = []
        div_tags = doc.getElementsByTagName('div')
        for div_tag in div_tags:
            clazz =  self._get_attribute_value(div_tag, 'class')
            if clazz == 'event_text':
                a_tags = div_tag.getElementsByTagName('a')
                for a_tag in a_tags:
                    link = a_tag.getAttribute('href')
                    if link.startswith('/networks/events/show_event.'):
                        links.append('http://techism.mixxt.de' + link)
        return links
    
    def parse_event(self, stream):
        """
        Parses the events page and returns a dict with event details.
        """
        doc = self._parse(stream)
        #print doc.toxml("utf-8")
        div_tag =  self._get_event_div_tag(doc)
        #print div_tag.toxml("utf-8")
        
        event = dict()
        event['title'] =  self._get_event_title(div_tag)
        event['begin'] =  self._get_event_begin(div_tag)
        event['end'] =  self._get_event_end(div_tag)
        event['url'] =  self._get_event_url(div_tag)
        event['description'] =  self._get_event_description(div_tag)
        # tags?
        # image?
        
        event['location'] = dict()
        event['location']['name'] =  self._get_location_name(div_tag)
        event['location']['street'] =  self._get_location_street(div_tag)
        event['location']['city'] =  self._get_location_city(div_tag)
        
        return event
    
    def _parse(self, stream):
        parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
        doc = parser.parse(stream)
        return doc
    
    def _get_event_div_tag(self, doc):
        # <div class="show_event">
        return  self._get_tag(doc, 'div', 'class', 'show_event')
    
    def _get_event_title(self, div_tag):
        # <h5 class="summary">OpenStreetMap-Treff</h5>
        tag =  self._get_tag(div_tag, 'h5', 'class', 'summary')
        title = self._get_text(tag)
        return title
    
    def _get_event_begin(self, div_tag):
        # <abbr class="dtstart" title="20101019T190000">
        # <abbr class="dtstart" title="20101111">
        tag =  self._get_tag(div_tag, 'abbr', 'class', None, 0)
        date =  self._get_attribute_value(tag, 'title')
        return date
    
    def _get_event_end(self, div_tag):
        # <abbr class="dtend" title="20101010T170000">
        # <abbr class="dtend" title="20101111">
        # <abbr class="dtstart" title="20101111">
        tag =  self._get_tag(div_tag, 'abbr', 'class', None, 1)
        date =  self._get_attribute_value(tag, 'title')
        return date
    
    def _get_event_url(self, div_tag):
        # <li class="event_link"><a class="url" href="http://wiki.openstreetmap.org/index.php/M%C3%BCnchen" target="_blank">
        # <div><a class="url" href="http://wiki.openstreetmap.org/index.php/M%C3%BCnchen" target="_blank">
        li_tag =  self._get_tag(div_tag, 'li', 'class', 'event_link')
        if li_tag:
            tag =  self._get_tag(li_tag, 'a', 'class', 'url')
            if tag:
                url =  self._get_attribute_value(tag, 'href')
                return url
        # fallback
        tag =  self._get_tag(div_tag, 'a', 'class', 'url')
        if tag:
            url =  self._get_attribute_value(tag, 'href')
            return url
    
    def _get_event_description(self, div_tag):
        # TODO: strip tags?
        # <div class="info_text specHigh1"> \n\t foo <p> \n\t blah blah.</p><p>blub blub.</p>
        tag =  self._get_tag(div_tag, 'div', 'class', 'info_text specHigh1')
        if tag:
            description = []
            for node in tag.childNodes:
                tokens = treewalkers.getTreeWalker("dom")(node)
                for text in serializer.HTMLSerializer(omit_optional_tags=False).serialize(tokens):
                    description.append(text.strip())
            return u''.join(description)
    
    def _get_location_name(self, div_tag):
        # <li class="event_loc"><img .../><p>Baerenwirt, Neuhausen<br/><span class="location"><span style="display: none">...</span>Wendl-Dietrich-Str. 24<br/>Muenchen<br/>
        li_tag =  self._get_tag(div_tag, 'li', 'class', 'event_loc')
        if li_tag:
            p_tag =  self._get_tag(li_tag, 'p')
            name =  self._get_text(p_tag)
            return name
    
    def _get_location_street(self, div_tag):
        # <li class="event_loc"><img .../><p>Baerenwirt, Neuhausen<br/><span class="location"><span style="display: none">...</span>Wendl-Dietrich-Str. 24<br/>Muenchen<br/>
        return  self._get_location_address(div_tag, 0)
    
    def _get_location_city(self, div_tag):
        # <li class="event_loc"><img .../><p>Baerenwirt, Neuhausen<br/><span class="location"><span style="display: none">...</span>Wendl-Dietrich-Str. 24<br/>Muenchen<br/>
        return  self._get_location_address(div_tag, 1)
    
    def _get_location_address(self, div_tag, index):
        li_tag =  self._get_tag(div_tag, 'li', 'class', 'event_loc')
        if li_tag:
            span_tag =  self._get_tag(li_tag, 'span', 'class', 'location')
            address =  self._get_text(span_tag)
            lines = address.splitlines()
            if lines.count > index:
                return lines[index].strip()
    
    
    def _get_tag(self, start_node, tag_name, attribute_name=None, attribute_value=None, index=0):
        count = 0
        tags = start_node.getElementsByTagName(tag_name)
        for tag in tags:
            if attribute_name:
                attribute = tag.getAttribute(attribute_name)
                if attribute_value == None or attribute == attribute_value:
                    if(count == index):
                        return tag
                    else:
                        count += 1
            else:
                return tag
        return None
    
    def _get_attribute_value(self, tag, attribute_name):
        if tag:
            return tag.getAttribute(attribute_name)
    
    def _get_text(self, tag):
        if tag:
            #return tag.childNodes[0].data
            rc = []
            for node in  tag.childNodes:
                if node.nodeType == node.TEXT_NODE:
                    rc.append(node.data)
            return ''.join(rc).strip()


def fetch_events_from_mixxt(output_file):
    event_index_url = 'http://techism.mixxt.de/networks/events/index'
    links = _fetch_event_links(event_index_url)
    events = _fetch_events(links)
    _write_events_to_json(events, output_file)
    print 'Done'
    

def fetch_archvie_from_mixxt(output_file):
    archive_index_base = 'http://techism.mixxt.de/networks/events/archive'
    links = []
    for i in (1,32):
        event_archive_url = 'http://techism.mixxt.de/networks/events/archive.' + str(i)
        links.extend(_fetch_event_links(event_index_url))
    events = _fetch_events(links)
    _write_events_to_json(events, output_file)
    print 'Done'

def import_from_json(input_file):
    input = open(input_file, 'rb')
    mixxt_events = json.load(input)
    
    print 'Importing %s Events from JSON' % len(mixxt_events)
    for mixxt_event in mixxt_events:
        l_name = mixxt_event['location']['name']
        l_street = mixxt_event['location']['street']
        l_city = mixxt_event['location']['city']
        if l_name:
            print 'Creating Location %s' % l_name
            location, created = Location.objects.get_or_create(name=l_name, defaults={'street':l_street, 'city':l_city})
            if not created:
                print ' ... already exists'

        print 'Creating Event %s' % mixxt_event['title']
        event = Event()
        event.location = location
        event.title = mixxt_event['title']
        event.url = mixxt_event['url']
        event.description = mixxt_event['description']
        event.set_date_time_begin_cet(_parse_datetime(mixxt_event['begin']))
        event.set_date_time_end_cet(_parse_datetime(mixxt_event['end']))
        event.published = True
        event.update_archived_flag()
        event.save()
    
    print 'Done'
    input.close()

def _parse_datetime(date_string):
    if date_string == None:
        return None
    
    if len(date_string) == 8:
        date_string = date_string + 'T000000'
    
    dt = datetime.strptime(date_string, '%Y%m%dT%H%M%S')
    #try:
    #except ValueError:
    #    try:
    #        dt = datetime.strptime(date_string, '%Y%m%dT')
    #        dt.
    #    except ValueError:
    #        return None
    return dt

def _fetch_event_links(url):
    print 'Fetching Event Links from %s' % url
    links = _parse_event_links(url)
    return links

def _fetch_events(links):
    events = []
    print 'Fetching %s Events' % len(links)
    for link in links:
        print 'Fetching Event from %s' % link
        event = _parse_event(link)
        events.append(event)
    return events

def _parse_event_links(url):
    parser = MixxtParser()
    stream = urllib2.urlopen(url)
    links = parser.parse_event_links(stream)
    stream.close()
    return links

def _parse_event(url):
    parser = MixxtParser()
    stream = urllib2.urlopen(url)
    event = parser.parse_event(stream)
    stream.close()
    return event

def _write_events_to_json(events, file_name):
    print 'Writing %s Events in JSON format to %s' % (len(events), file_name)
    output = open(file_name, 'wb')
    dump = json.dump(events, output)
    output.close()

