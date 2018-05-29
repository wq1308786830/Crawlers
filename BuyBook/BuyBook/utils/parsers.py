class Parsers:
    dd_selector_str = '//div[@id="search_nature_rg"]/ul/li'
    amaze_selector_str = '//ul[@id="s-results-list-atf"]/li'
    jd_selector_str = '//div[@id="J_goodsList"]/ul/li'

    def get_dd_data(self, resp):
        data = []
        for item in resp.selector.xpath(self.dd_selector_str):
            book_name = item.xpath('.//a[@class="pic"]/@title').extract_first()
            book_info = item.xpath('.//p[@class="search_book_author"]/span/a/@title').extract()
            author = book_info[0] if len(book_info) else ''
            money = item.xpath('.//p[@class="price"]/span[@class="search_now_price"]/text()').extract_first()
            money = float(money[1:]) if money else 0.0
            publisher = book_info[-1] if len(book_info) else ''
            buy_count = int(item.xpath(
                './/p[@class="search_star_line"]/a[@class="search_comment_num"]/text()').extract_first()[:-3])
            time_temp = item.xpath('.//p[@class="search_book_author"]/span/text()').extract()
            time_temp = time_temp[-2] if len(time_temp) > 2 else ''
            time = time_temp[2:] if len(time_temp) > 2 else ''
            like = int(item.xpath(
                './/p[@class="search_star_line"]/span[@class="search_star_black"]/span/@style'
            ).extract_first().split(' ')[1][:-2])
            href = item.xpath('.//a[@class="pic"]/@href').extract_first()
            data.append([book_name, author, money, publisher, time, like, buy_count, href])
        return data

    def get_amaze_data(self, resp):
        data = []
        for item in resp.selector.xpath(self.amaze_selector_str):
            book_name = item.xpath('.//h2[contains(@class, "s-access-title")]/text()').extract_first()
            book_info = item.xpath('string(.//div[@class="a-fixed-left-grid-col a-col-right"]/div/div[2])')
            author = str(book_info.extract())[2:-2]
            money = item.xpath('.//span[contains(@class, "s-price")]/text()').extract_first()
            # money = float(money[1:].replace(',', '')) if money else 0.0
            publisher = str(book_info.extract())[2:-2]
            buy_count = item.xpath('.//div[contains(@class, "a-span-last")]/div/a/text()').extract_first()
            time = book_info.extract()[0]
            like = item.xpath('.//i[@class="a-icon-star"]/span/text()').extract_first()
            href = item.xpath('.//a[contains(@class, "s-access-detail-page")]/@href').extract_first()
            data.append([book_name, author, money, publisher, time, like, buy_count, href])
        return data

    def get_jd_data(self, resp):
        data = []
        for item in resp.selector.xpath(self.jd_selector_str):
            book_name = item.xpath('string(.//div[@class="p-name"]/a/em)').extract_first()
            author = item.xpath('.//div[@class="p-bookdetails"]/span[@class="p-bi-name"]/a/text()').extract_first()
            money = item.xpath('.//div[@class="p-price"]/strong/i/text()').extract_first()
            money = money if money else 0.0  # 后续看能不能转换为float类型，方便excel统计
            publisher = item.xpath('.//div[@class="p-shopnum"]/a/text()').extract_first()
            buy_count = item.xpath('.//div[@class="p-commit"]/strong/a/text()').extract_first()
            time = item.xpath('.//div[@class="p-bookdetails"]/span[@class="p-bi-date"]/text()').extract_first()
            href = item.xpath('string(.//div[@class="p-name"]/a/@href)').extract_first()
            data.append([book_name, author, money, publisher, time, '', buy_count, href])
        return data
