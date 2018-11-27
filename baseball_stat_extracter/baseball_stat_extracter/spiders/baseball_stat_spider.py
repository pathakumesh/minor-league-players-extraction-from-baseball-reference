# -*- coding: utf-8 -*-
import csv
import re
import scrapy
import logging as log
from baseball_stat_extracter.items import BaseballStatItem


class BaseBallExtractSpider(scrapy.Spider):
    name = "baseball_extract_spider"
    allowed_domains = ["www.baseball-reference.com"]

    def __init__(self,):
        self.input_names = set()
        self.formatted_input_names = set()
        self.extracted_names = set()
        self.formatted_extracted_names = set()
        self.initials = set()
        self.urls = set()
        self.name_regex = re.compile(r'[^a-zA-Z ]')
        self.headers = {
            'referer': 'https://www.baseball-reference.com/'
                       'register/player.fcgi',
            "accept": 'text/html,application/xhtml+xml,application/'
                      'xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,hi;q=0.8",
            "cache-control": "no-cache"
        }
        self.process_input_file()

    def process_input_file(self,):
        with open('players_list.csv', 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            for i, row in enumerate(csvreader):
                if i == 0:
                    continue
                self.input_names.add("{} {}"
                                     .format(row[0].strip(),
                                             row[1].strip()))
                self.initials.add(row[1][:2].lower())
        self.formatted_input_names = set(
            self.name_regex.sub('', name).lower() for name in self.input_names
        )

    def date_match(self, played_date):
        pattern1 = re.compile(r'^(\d+)$')
        pattern2 = re.compile(r'^\d+-(\d+)$')
        match1 = pattern1.findall(played_date)
        if not match1:
            match2 = pattern2.findall(played_date)
            if match2 and match2[0] in ['2017', '2018']:
                return True
            return False
        if match1[0] in ['2017', '2018']:
            return True
        return False

    def name_match(self, name):
        formatted_name = self.name_regex.sub('', name).lower()
        if formatted_name in self.formatted_input_names:
            return True
        return False

    def name_date_match_and_get_url(self, response, name, played_date):
        names = response.xpath(
            '//div[@class="section_content"]//a[text()="{}"]'.format(name)
        )
        for n in names:
            url = n.xpath('@href').extract_first()
            played_date_block = n.xpath(
                'following-sibling::em[text()="played"]'
                '/following-sibling::text()[1]'
            )
            if not played_date_block:
                played_date_block = n.xpath(
                    '../following-sibling::em[text()="played"]'
                    '/following-sibling::text()[1]')
            extracted_played_date = played_date_block.extract_first().strip()\
                if played_date_block else ""
            if extracted_played_date == played_date and url not in self.urls:
                self.urls.add(url)
                return url

    def start_requests(self):
        # self.initials = ['fl']
        for initial in self.initials:
            intermediate_url = 'https://www.baseball-reference.com/register/'\
                               'player.fcgi?initial={}'.format(initial)
            yield scrapy.Request(
                url=intermediate_url,
                headers=self.headers,
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        players_section = response.xpath('//div[@class="section_content"]')
        players = players_section.xpath('string()').extract_first()
        if players:
            players = players.split('\n')
        pattern = re.compile(r'(.*?),.*played (\d+-?\d*)')
        for player in players:
            # print(player)
            match = pattern.findall(player)
            if not match:
                continue
            name, played_date = match[0]
            if not self.date_match(played_date) or not self.name_match(name):
                continue
            player_url = self.name_date_match_and_get_url(
                response, name, played_date)
            if not player_url:
                continue
            if 'https://www.baseball-reference.com' not in player_url:
                player_url = 'https://www.baseball-reference.com' + player_url
            yield scrapy.Request(
                url=player_url,
                headers=self.headers,
                callback=self.parse_player_data,
                dont_filter=True,
                meta={'original_name': name}
            )

    def parse_player_data(self, response):
        name = response.xpath(
            '//h1[@itemprop="name"]/text()').extract_first()
        _id = response.url.split('id=')[1]
        bats = response.xpath(
            '//strong[contains(text(), "Bats:")]/'
            'following-sibling::text()[1]').extract_first()
        bats = bats.split()[0].strip() if bats else ""
        team = response.xpath(
            '//strong[contains(text(), "Team:")]/'
            'following-sibling::a[1]/text()').extract_first()
        if not team:
            team = ""
        table_rows = response.xpath('//table[@id="standard_batting"]/tbody/tr')
        formatted_name = self.name_regex.sub('', name).lower()
        self.extracted_names.add(name)
        self.formatted_extracted_names.add(formatted_name)
        original_name = response.meta['original_name']
        self.extracted_names.add(original_name)
        formatted_name = self.name_regex.sub('', original_name).lower()
        self.formatted_extracted_names.add(formatted_name)
        for row in table_rows:
            if row.xpath('@class').extract_first() in ["thead", "spacer"]:
                continue
            yield self.get_item(name, _id, bats, team, row)

    def get_item(self, name, _id="", bats="", team="", row=False):
        item = BaseballStatItem()
        FIRST, LAST = name.split()[0], ' '.join(name.split()[1:])
        to_update = {
            "FIRST": FIRST,
            "LAST": LAST,
            "ID": _id,
            "BATS": bats,
            "TEAM": team,
            "YEAR": "",
            "AGE": "",
            "AgeDiff": "",
            "Tm": "",
            "Lg": "",
            "Lev": "",
            "Aff": "",
            "G": "",
            "PA": "",
            "AB": "",
            "R": "",
            "H": "",
            "_2B": "",
            "_3B": "",
            "HR": "",
            "RBI": "",
            "SB": "",
            "CS": "",
            "BB": "",
            "SO": "",
            "BA": "",
            "OBP": "",
            "SLG": "",
            "OPS": "",
            "TB": "",
            "GDP": "",
            "HBP": "",
            "SH": "",
            "SF": "",
            "IBB": "",
            "BB_Percent": "",
            "K_percent": "",
            "BB_K": "",
            "HR_Percent": "",
            "IOS": "",
        }
        item.update(to_update)
        if not row:
            return item
        to_update.update({
            'YEAR': row.xpath(
                'th/a/text()').extract_first(),
            'AGE': row.xpath(
                'td[@data-stat="age"]/text()').extract_first(),
            'AgeDiff': row.xpath(
                'td[@data-stat="age_diff"]/text()').extract_first(),
            'Tm': row.xpath(
                'td[@data-stat="team_ID"]/a/text()').extract_first(),
            'Lg': row.xpath(
                'td[@data-stat="lg_ID"]/a/text()').extract_first(),
            'Lev': row.xpath(
                'td[@data-stat="level"]/text()').extract_first(),
            'Aff': row.xpath(
                'td[@data-stat="affiliation"]/text()').extract_first(),
            'G': row.xpath(
                'td[@data-stat="G"]/text()').extract_first(),
            'PA': row.xpath(
                'td[@data-stat="PA"]/'
                'text()').extract_first() or "0.0",
            'AB': row.xpath(
                'td[@data-stat="AB"]/text()').extract_first(),
            'R': row.xpath(
                'td[@data-stat="R"]/text()').extract_first(),
            'H': row.xpath(
                'td[@data-stat="H"]/text()').extract_first(),
            '_2B': row.xpath(
                'td[@data-stat="2B"]/text()').extract_first(),
            '_3B': row.xpath(
                'td[@data-stat="3B"]/text()').extract_first(),
            'HR': row.xpath(
                'td[@data-stat="HR"]/text()').extract_first(),
            'RBI': row.xpath(
                'td[@data-stat="RBI"]/text()').extract_first(),
            'SB': row.xpath(
                'td[@data-stat="SB"]/text()').extract_first(),
            'CS': row.xpath(
                'td[@data-stat="CS"]/text()').extract_first(),
            'BB': row.xpath(
                'td[@data-stat="BB"]/text()').extract_first(),
            'SO': row.xpath(
                'td[@data-stat="SO"]/text()').extract_first(),
            'BA': row.xpath(
                'td[@data-stat="batting_avg"]/'
                'text()').extract_first() or "0.0",
            'OBP': row.xpath(
                'td[@data-stat="onbase_perc"]/text()').extract_first(),
            'SLG': row.xpath(
                'td[@data-stat="slugging_perc"]/'
                'text()').extract_first() or "0.0",
            'OPS': row.xpath(
                'td[@data-stat="onbase_plus_slugging"]/'
                'text()').extract_first(),
            'TB': row.xpath(
                'td[@data-stat="TB"]/text()').extract_first(),
            'GDP': row.xpath(
                'td[@data-stat="GIDP"]/text()').extract_first(),
            'HBP': row.xpath(
                'td[@data-stat="HBP"]/text()').extract_first(),
            'SH': row.xpath(
                'td[@data-stat="SH"]/text()').extract_first(),
            'SF': row.xpath(
                'td[@data-stat="SF"]/text()').extract_first(),
            'IBB': row.xpath(
                'td[@data-stat="IBB"]/text()').extract_first(),
        })
        if not float(to_update['PA']) == 0.0:
            to_update.update({
                "BB_Percent": "{:.3f}".format(
                    float(to_update['BB'])/float(to_update['PA'])*100),
                "K_percent": "{:.3f}".format(
                    float(to_update['SO'])/float(to_update['PA'])*100),
                "HR_Percent": "{:.3f}".format(
                    float(to_update['HR'])/float(to_update['PA'])*100),
            })
        else:
            to_update.update({
                "BB_Percent": "{:.3f}".format(
                    float(to_update['BB'])),
                "K_percent": "{:.3f}".format(
                    float(to_update['SO'])),
                "HR_Percent": "{:.3f}".format(
                    float(to_update['HR'])),
            })
        if not float(to_update['SO']) == 0.0:
            to_update.update({
                "BB_K": "{:.3f}".format(
                        float(to_update['BB'])/float(to_update['SO'])*100),
            })
        else:
            to_update.update({
                "BB_K": "{:.3f}".format(
                        float(to_update['BB'])),
            })
        to_update.update({
            "IOS": "{:.3f}".format(
                    float(to_update['SLG']) - float(to_update['BA'])),
            })
        item.update(to_update)
        return item
