import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"

# scraping for quotes or tags
    def start_requests(self):
        tag = getattr(self, 'tag', None)
        if tag is None:
            url_quote = 'http://quotes.toscrape.com/page/1/'
            yield scrapy.Request(url_quote, self.parse_quote)

        url_tag = 'http://quotes.toscrape.com/'
        if tag is not None:
            url_tag = url_tag + 'tag/' + tag
            yield scrapy.Request(url_tag, self.parse_tag)

    def parse_quote(self, response):
        for quote in response.selector.xpath('//div[@class = "quote"]'):
            yield {
                'text': quote.xpath('.//span[@class = "text"]/text()').get(),
                'author': quote.xpath('.//small[@class = "author"]/text()').get(),
                'tags': quote.xpath('.//a[@class = "tag"]/text()').getall()
            }

        next_pageq = response.xpath(
            '//li[@class = "next"]//a[contains(@href, "page")]/@href').get()
        if next_pageq is not None:
            yield response.follow(next_pageq, callback=self.parse_quote)
