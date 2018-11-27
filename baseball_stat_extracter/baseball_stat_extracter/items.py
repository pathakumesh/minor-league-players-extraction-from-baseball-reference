# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseballStatItem(scrapy.Item):
    # define the fields for your item here like:

    FIRST = scrapy.Field()
    LAST = scrapy.Field()
    ID = scrapy.Field()
    BATS = scrapy.Field()
    TEAM = scrapy.Field()
    YEAR = scrapy.Field()
    AGE = scrapy.Field()
    AgeDiff = scrapy.Field()
    Tm = scrapy.Field()
    Lg = scrapy.Field()
    Lev = scrapy.Field()
    Aff = scrapy.Field()
    G = scrapy.Field()
    PA = scrapy.Field()
    AB = scrapy.Field()
    R = scrapy.Field()
    H = scrapy.Field()
    _2B = scrapy.Field()
    _3B = scrapy.Field()
    HR = scrapy.Field()
    RBI = scrapy.Field()
    SB = scrapy.Field()
    CS = scrapy.Field()
    BB = scrapy.Field()
    SO = scrapy.Field()
    BA = scrapy.Field()
    OBP = scrapy.Field()
    SLG = scrapy.Field()
    OPS = scrapy.Field()
    TB = scrapy.Field()
    GDP = scrapy.Field()
    HBP = scrapy.Field()
    SH = scrapy.Field()
    SF = scrapy.Field()
    IBB = scrapy.Field()
    BB_Percent = scrapy.Field()
    K_percent = scrapy.Field()
    BB_K = scrapy.Field()
    HR_Percent = scrapy.Field()
    IOS = scrapy.Field()
