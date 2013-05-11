#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from scanner_attribute import create_binary_attribute

def has_topic(website, topics):
    threshold = 3
    count = 0

    # Check in text
    texts = website.soup.findAll(text=True)
    for text in texts:
        for topic in topics:
            if topic.lower() in text.lower():
                count += 1
                break

    # Check in keywords
    meta_tags = website.soup.find_all('meta')
    for meta_tag in meta_tags:
        if meta_tag.has_key('name') and meta_tag.has_key('content'):
            name = meta_tag['name']
            content = meta_tag['content']

            if not 'keywords' in name.lower():
                continue

            for topic in topics:
                if topic.lower() in content.lower():
                    count += 1
                    break

    return count >= threshold

def content_news_scanner(website):
    key = 'has_content_news'
    topic = ['nyheder', 'news', 'avis', '']
    return create_binary_attribute(key, has_topic(website, topic))

def content_sport_scanner(website):
    key = 'has_content_sport'
    topic = ['sport', 'bold', 'ball', 'spiller', 'tennis', 'cykling', 'boksning', 'gold', 'motion']
    return create_binary_attribute(key, has_topic(website, topic))

def content_games_scanner(website):
    key = 'has_content_games'
    topic = ['game', 'spil', 'xbox', 'playstation', 'wii']
    return create_binary_attribute(key, has_topic(website, topic))

def content_technology_scanner(website):
    key = 'has_content_technology'
    topic = ['computer', 'pc', 'mac', 'phone', 'tablet', 'hardware', 'software', u'bærbar', 'laptop', 'notebook']
    return create_binary_attribute(key, has_topic(website, topic))

def content_xxx_scanner(website):
    key = 'has_content_xxx'
    topic = ['xxx', 'porn', 'erotic', 'sex', 'naked', 'nude', u'nøgen', u'fræk']
    return create_binary_attribute(key, has_topic(website, topic))

def content_music_scanner(website):
    key = 'has_content_music'
    topic = ['music', 'musik', 'lyd', 'audio', 'song', 'sang', 'pop', 'rock']
    return create_binary_attribute(key, has_topic(website, topic))

def content_shop_scanner(website):
    key = 'has_content_shop'
    topic = ['shop', 'butik', u'køb', 'buy', 'bestil', 'order', 'basket', 'kurv', 'cart', 'sell', u'sælg']
    return create_binary_attribute(key, has_topic(website, topic))

def content_transport_scanner(website):
    key = 'has_content_transport'
    topic = ['transport', 'bus', 'bil', 'car', 'bike', 'bicycle', 'cykel', 'vej', 'road', 'tog', 'train', 'metro']
    return create_binary_attribute(key, has_topic(website, topic))

def content_food_scanner(website):
    key = 'has_content_food'
    topic = ['food', 'mad', 'opskrift', 'recipe', 'frokost', 'brunch', 'restaurant', 'cafe']
    return create_binary_attribute(key, has_topic(website, topic))

def content_film_scanner(website):
    key = 'has_content_film'
    topic = ['film', 'movie', 'biograf', 'cinema', 'dvd', 'bluray', u'skærm', 'screen', 'tv', 'fjernsyn']
    return create_binary_attribute(key, has_topic(website, topic))

def content_health_scanner(website):
    key = 'has_content_health'
    topic = ['sundhed', 'health', 'motion', 'diet', 'kur', 'slank', u'vægt', 'weight', u'træning', 'workout']
    return create_binary_attribute(key, has_topic(website, topic))

def content_business_scanner(website):
    key = 'has_content_business'
    topic = ['business', 'arbejde', u'økonomi', 'economi', 'work', 'money', 'penge', 'finance', 'finans', 'aktie', 'stock']
    return create_binary_attribute(key, has_topic(website, topic))
