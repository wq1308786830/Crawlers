# -*- coding: utf-8 -*-
# !/usr/bin/python

from scrapy import cmdline


name = 'BuyBook'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())