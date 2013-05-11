import sys
from lxml import etree
from utils.bin_helper import bin_numeric
from scanner_attribute import create_binary_attribute

# jquery, prototype
# modernizr, underscorejs, handlebars
# knockout, angular, backbone, ember

def has_script(website, filename):
    for script in website.soup.find_all('script'):
        src = script.get('src')
        if src is not None:
            return filename in src
    return False

def jquery_scanner(website):
    key = 'has_js_jquery'
    filename = 'jquery'
    return create_binary_attribute(key, has_script(website, filename))

def prototype_scanner(website):
    key = 'has_js_prototype'
    filename = 'prototype'
    return create_binary_attribute(key, has_script(website, filename))

def dojo_scanner(website):
    key = 'has_js_dojo'
    filename = 'dojo'
    return create_binary_attribute(key, has_script(website, filename))

def mootools_scanner(website):
    key = 'has_js_mootools'
    filename = 'mootools'
    return create_binary_attribute(key, has_script(website, filename)) 

def modernizr_scanner(website):
    key = 'has_js_modernizr'
    filename = 'modernizr'
    return create_binary_attribute(key, has_script(website, filename))

def underscore_scanner(website):
    key = 'has_js_underscore'
    filename = 'underscore'
    return create_binary_attribute(key, has_script(website, filename))

def handlebars_scanner(website):
    key = 'has_js_handlebars'
    filename = 'handlebars'
    return create_binary_attribute(key, has_script(website, filename))

def knockout_scanner(website):
    key = 'has_js_knockout'
    filename = 'knockout'
    return create_binary_attribute(key, has_script(website, filename))

def ember_scanner(website):
    key = 'has_js_ember'
    filename = 'ember'
    return create_binary_attribute(key, has_script(website, filename))

def angular_scanner(website):
    key = 'has_js_angular'
    filename = 'angular'
    return create_binary_attribute(key, has_script(website, filename))

def backbone_scanner(website):
    key = 'has_js_backbone'
    filename = 'backbone'
    return create_binary_attribute(key, has_script(website, filename))