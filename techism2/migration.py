 #!/usr/local/bin/python
 # -*- coding: utf-8 -*-
import urllib2
import html5lib
from html5lib import treebuilders, treewalkers, serializer
from datetime import datetime

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
            clazz = get_attribute_value(div_tag, 'class')
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
        div_tag = get_event_div_tag(doc)
        #print div_tag.toxml("utf-8")
        
        event = dict()
        event['title'] = get_event_title(div_tag)
        event['begin'] = get_event_begin(div_tag)
        event['end'] = get_event_end(div_tag)
        event['url'] = get_event_url(div_tag)
        event['description'] = get_event_description(div_tag)
        # tags?
        # image?
        
        event['location'] = dict()
        event['location']['name'] = get_location_name(div_tag)
        event['location']['street'] = get_location_street(div_tag)
        event['location']['city'] = get_location_city(div_tag)
        
        return event
    
    
    def _parse(self, stream):
        parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))
        doc = parser.parse(stream)
        return doc


def get_event_div_tag(doc):
    # <div class="show_event">
    return get_tag(doc, 'div', 'class', 'show_event')

def get_event_title(div_tag):
    # <h5 class="summary">OpenStreetMap-Treff</h5>
    tag = get_tag(div_tag, 'h5', 'class', 'summary')
    title = get_text(tag)
    return title

def get_event_begin(div_tag):
    # <abbr class="dtstart" title="20101019T190000">
    # <abbr class="dtstart" title="20101111">
    tag = get_tag(div_tag, 'abbr', 'class', None, 0)
    date = get_attribute_value(tag, 'title')
    return date

def get_event_end(div_tag):
    # <abbr class="dtend" title="20101010T170000">
    # <abbr class="dtend" title="20101111">
    # <abbr class="dtstart" title="20101111">
    tag = get_tag(div_tag, 'abbr', 'class', None, 1)
    date = get_attribute_value(tag, 'title')
    return date

def get_event_url(div_tag):
    # <li class="event_link"><a class="url" href="http://wiki.openstreetmap.org/index.php/M%C3%BCnchen" target="_blank">
    # <div><a class="url" href="http://wiki.openstreetmap.org/index.php/M%C3%BCnchen" target="_blank">
    li_tag = get_tag(div_tag, 'li', 'class', 'event_link')
    if li_tag:
        tag = get_tag(li_tag, 'a', 'class', 'url')
        if tag:
            url = get_attribute_value(tag, 'href')
            return url
    # fallback
    tag = get_tag(div_tag, 'a', 'class', 'url')
    if tag:
        url = get_attribute_value(tag, 'href')
        return url

def get_event_description(div_tag):
    # TODO: strip tags?
    # <div class="info_text specHigh1"> \n\t foo <p> \n\t blah blah.</p><p>blub blub.</p>
    tag = get_tag(div_tag, 'div', 'class', 'info_text specHigh1')
    if tag:
        description = []
        for node in tag.childNodes:
            tokens = treewalkers.getTreeWalker("dom")(node)
            for text in serializer.HTMLSerializer(omit_optional_tags=False).serialize(tokens):
                description.append(text.strip())
        return u''.join(description)

def get_location_name(div_tag):
    # <li class="event_loc"><img .../><p>Baerenwirt, Neuhausen<br/><span class="location"><span style="display: none">...</span>Wendl-Dietrich-Str. 24<br/>Muenchen<br/>
    li_tag = get_tag(div_tag, 'li', 'class', 'event_loc')
    if li_tag:
        p_tag = get_tag(li_tag, 'p')
        name = get_text(p_tag)
        return name

def get_location_street(div_tag):
    # <li class="event_loc"><img .../><p>Baerenwirt, Neuhausen<br/><span class="location"><span style="display: none">...</span>Wendl-Dietrich-Str. 24<br/>Muenchen<br/>
    return get_location_address(div_tag, 0)

def get_location_city(div_tag):
    # <li class="event_loc"><img .../><p>Baerenwirt, Neuhausen<br/><span class="location"><span style="display: none">...</span>Wendl-Dietrich-Str. 24<br/>Muenchen<br/>
    return get_location_address(div_tag, 1)

def get_location_address(div_tag, index):
    li_tag = get_tag(div_tag, 'li', 'class', 'event_loc')
    if li_tag:
        span_tag = get_tag(li_tag, 'span', 'class', 'location')
        address = get_text(span_tag)
        lines = address.splitlines()
        if lines.count > index:
            return lines[index].strip()


def get_tag(start_node, tag_name, attribute_name=None, attribute_value=None, index=0):
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

def get_attribute_value(tag, attribute_name):
    if tag:
        return tag.getAttribute(attribute_name)

def get_text(tag):
    if tag:
        #return tag.childNodes[0].data
        rc = []
        for node in  tag.childNodes:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc).strip()








#if link:
#    f = urllib2.urlopen(link)
#else:
#    f = open("mixxt_events.txt")