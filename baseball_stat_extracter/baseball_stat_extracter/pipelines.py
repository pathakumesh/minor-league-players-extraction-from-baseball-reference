# -*- coding: utf-8 -*-
import os
import csv
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from baseball_stat_extracter.items import BaseballStatItem
from baseball_stat_extracter.obtain_simplified_data import obtain_simplified_data
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BaseballStatPipeline(object):
    def __init__(self):
        self.files = {}
        self.file_name = 'MiLB-Player-Data-Master.csv'
        self.export_fields = [
            "FIRST",
            "LAST",
            "ID",
            "BATS",
            "TEAM",
            "YEAR",
            "AGE",
            "AgeDiff",
            "Tm",
            "Lg",
            "Lev",
            "Aff",
            "G",
            "PA",
            "AB",
            "R",
            "H",
            "_2B",
            "_3B",
            "HR",
            "RBI",
            "SB",
            "CS",
            "BB",
            "SO",
            "BA",
            "OBP",
            "SLG",
            "OPS",
            "TB",
            "GDP",
            "HBP",
            "SH",
            "SF",
            "IBB",
            "BB_Percent",
            "K_percent",
            "BB_K",
            "HR_Percent",
            "IOS",

        ]

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        output_file = open(self.file_name, 'w+b')
        self.files[spider] = output_file
        self.exporter = CsvItemExporter(output_file,
                                        fields_to_export=self.export_fields)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        print('Updating remaining  names')
        self.update_remaining_names(spider)
        self.exporter.finish_exporting()
        output_file = self.files.pop(spider)
        output_file.close()
        print('Creating simplified file')
        obtain_simplified_data(self.file_name)

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def update_remaining_names(self, spider):
        remaining_names = spider.formatted_input_names -\
            spider.formatted_extracted_names
        remaining_names = sorted(remaining_names)
        print(remaining_names)
        for name in remaining_names:
            item = BaseballStatItem()
            item.update({k: "" for k in self.export_fields})
            FIRST, LAST = name.split()[0], ' '.join(name.split()[1:])
            item.update({
                'FIRST': FIRST.capitalize(),
                'LAST': LAST.capitalize()
            })
            self.exporter.export_item(item)
