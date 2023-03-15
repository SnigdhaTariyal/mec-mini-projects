import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-css"


# scraping for quotes
    #start_urls = [ 'http://quotes.toscrape.com/page/1/',]

    # def parse(self, response):
    #page = response.url.split("/")[-2]
    #filename = 'quotes-%s.html' % page
    # with open(filename, 'wb') as f:
    #   f.write(response.body)
    #self.log('Saved file %s' % filename)

    # for quote in response.css('div.quote'):
    # yield {
    # 'text': quote.css('span.text::text').get(),
    # 'author': quote.css('small.author::text').get(),
    # 'tags': quote.css('div.tags a.tag::text').getall(),
    # }

    #next_page = response.css('li.next a::attr(href)').get()
    # if next_page is not None:
    #next_page = response.urljoin(next_page)
    # yield scrapy.Request(next_page, callback=self.parse)

    #next_page = response.css('li.next a::attr(href)').get()
    # if next_page is not None:
    # yield response.follow(next_page, callback=self.parse)

    # for href in response.css('ul.pager a::attr(href)'):
    # yield response.follow(href, callback=self.parse)

    # for a in response.css('ul.pager a'):
    # yield response.follow(a, callback=self.parse)

    #anchors = response.css('ul.pager a')
    # yield from response.follow_all(anchors, callback=self.parse)


# Scraping for tags


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
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_pageq = response.css('li.next a::attr(href)').get()
        if next_pageq is not None:
            yield response.follow(next_pageq, callback=self.parse_quote)

    def parse_tag(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_tag)
