import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["www.ethiojobs.net"]
    start_urls = [
        "https://www.ethiojobs.net/search-results-jobs/?searchId=1713396767.1632&action=search&page=1&listings_per_page=100&view=list"
    ]

    def parse(self, response):
        res = response.xpath('//tbody[@class="searchResultsJobs"]/tr')

        for r in res:
            position = r.xpath(".//td/div/div[@class='listing-title']/h2/text()").get()
            recruiter = r.xpath(
                ".//td/div/div[@class='listing-info']/div[@class='detailed-view']/span[@class['company-name']/text()]"
            ).get()

            yield {"Position": position, "Company": recruiter}

            next_page = res.xpath("//ul[@class='pagination pagination-blue']/li[7]/a/@href")
            if next_page:
                
