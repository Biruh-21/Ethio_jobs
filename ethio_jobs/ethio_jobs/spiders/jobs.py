from typing import Iterable
import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["www.ethiojobs.net"]
    start_urls = [
        "https://www.ethiojobs.net/search-results-jobs/?searchId=1713396767.1632&action=search&page=1&listings_per_page=100&view=list",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        res = response.xpath('//tbody[@class="searchResultsJobs"]/tr')

        for r in res:
            position = r.xpath(
                ".//td/div/div[@class='listing-title']/h2/a/text()"
            ).get()
            recruiter = r.xpath(
                ".//td/div/div[contains(@class, 'listing-info')]/div[contains(@class, 'brief_view')]/div[1]/a/text()"
            ).get()

            yield {"Position": position, "Company": recruiter}

            next_page = response.urljoin(
                res.xpath(
                    "//ul[@class='pagination pagination-blue']/li[7]/a/@href"
                ).get()
            )
            if next_page:
                yield scrapy.Request(
                    url=next_page, callback=self.parse, headers=self.headers
                )
