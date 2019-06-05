import scrapy

from ..utils.parsers import Parsers
from ..utils.write_excel import ExcelRW


class BookSpider(scrapy.Spider):
    name = 'BuyBook'

    params = {'keywords': '解忧杂货店'}
    allow_domains = [
        'https://www.amazon.cn/s',
        'http://search.dangdang.com/',
        'https://search.jd.com/Search'
    ]
    amazon_url = allow_domains[0] + '?k=' + params['keywords'] + '&i=stripbooks'

    dd_url = allow_domains[1] + '?key=' + params['keywords'] + '&act=input'

    jd_url = allow_domains[2] + '?enc=utf-8&keyword=' + params['keywords']

    urls = [amazon_url, dd_url, jd_url]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('============================================', response)
        parsers = Parsers()
        excel = ExcelRW()
        page = response.url.split("/")[2]
        excel_path = './static_files/excels/'
        header_data = [['书名', 50], ['作者', 40], ['价格', 10], ['出版社', 40], ['时间', 10],
                       ['星级', 10], ['评价数', 10], ['详情链接', 50]]
        if page == 'www.amazon.cn':
            # 保存当页数据
            data = parsers.get_amaze_data(response)
            excel.save_excel('Amazon Book', data, excel_path + self.params['keywords'] + '_book.xlsx', header_data)

            # 爬取下一页
            max_page = response.xpath('//ul[@class="a-pagination"]/li/text()').extract()[-1]
            try:
                max_page = int(max_page) if max_page and int(max_page) else 0
                for i in range(2, max_page + 1):
                    next_page = response.urljoin(self.urls[0] + '&page=' + str(i))
                    yield scrapy.Request(next_page, callback=self.parse)
            except Exception as e:
                print('FBI WARNING!!!!!!:', e)

        elif page == 'search.dangdang.com':
            data = parsers.get_dd_data(response)
            excel.save_excel('DangDang Book', data, excel_path + self.params['keywords'] + '_book.xlsx', header_data)

            max_page = int(response.xpath('//div[@class="paging"]/ul/li/a/text()').extract()[-2])
            for i in range(2, max_page + 1):
                next_page = response.urljoin(self.urls[1] + '&page_index=' + str(i))
                yield scrapy.Request(next_page, callback=self.parse)

        elif page == 'search.jd.com':
            data = parsers.get_jd_data(response)
            excel.save_excel('JD Book', data, excel_path + self.params['keywords'] + '_book.xlsx', header_data)

            # 京东页码比较特别，比如：page=1返回第一组数据显示在第一页，page=2时返回第二组数据但是与第一组数据一起显示在第一页，以此类推
            max_page = int(response.xpath('//div[@id="J_topPage"]/span[@class="fp-text"]/i/text()').extract_first()) * 2
            for i in range(4, max_page, 2):
                next_page = response.urljoin(self.urls[2] + '&page=' + str(i))
                yield scrapy.Request(next_page, callback=self.parse)

        # 写入html文件
        # filename = '../../static_files/web/' + page + ".html"
        # with open(filename, 'ab') as f:
        #     if page == 'www.amazon.cn':
        #         f.write(response.xpath('//ul[@id="s-results-list-atf"]').extract_first(default='not-found').encode())
        #     elif page == 'search.dangdang.com':
        #         f.write(response.xpath('//div[@id="search_nature_rg"]/ul').extract_first(default='not-found').encode())
        #     elif page == 'search.jd.com':
        #         f.write(response.xpath('//div[@id="J_goodsList"]').extract_first(default='not-found').encode())

        # data = [{'book_name': '', 'author': '', 'money': float(0),
        #          'publisher': '', 'time': '', 'like': int(''), 'buy_count': int('')}]
