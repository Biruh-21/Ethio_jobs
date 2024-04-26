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
        """
        this method is used to parse the job posts lists information
        it extracts the information from the job posts including the link to
        the job details page and send it to the parse_detail method to parse the details
        """

        jobs = response.xpath('//div[@class="listing-section"]')

        for job in jobs[:4]:
            position = job.xpath(".//div[@class='listing-title']/h2/a/text()").get()
            recruiter = job.xpath(
                ".//div[contains(@class, 'listing-info')]/div[contains(@class, 'brief_view')]/div[1]/a/text()"
            ).get()
            work_place = (
                job.xpath(".//span[contains(@class, 'work-palce')][last()]/text()")
                .get()
                .strip()
            )
            deadline = job.xpath(
                ".//div[@class='detailed_view']/div[@class='pull-left']/span[last()]/text()"
            ).get()
            level = job.xpath(
                ".//div[@class='detailed_view']/div[@class='pull-left']/span[5]/text()"
            ).get()
            job_detail_link = job.xpath(".//li[@class='viewDetails']/a/@href").get()

            yield {
                "Position": position,
                "Company": recruiter,
                "Work_place": work_place,
                "Deadline": deadline,
                "Level": level,
                "Job_detail_link": job_detail_link,
            }
            yield from response.follow(job_detail_link, self.parse_detail)

        # next_page = response.urljoin(
        #     response.xpath(
        #         "//ul[@class='pagination pagination-blue']/li[last()]/a/@href"
        #     ).get()
        # )
        # if next_page:
        #     yield scrapy.Request(
        #         url=next_page, callback=self.parse, headers=self.headers
        #     )

    def parse_detail(self, response):
        """
        this method is used to parse the job details
        """

        catagory = (
            response.xpath("//div[@id='col-wide']/div[1]/div[2]/text()").get().strip()
        )
        employement_type = response.xpath(
            "//div[@id='col-wide']/div[4]/div[2]/text()"
        ).get()
        salary = response.xpath("//div[@id='col-wide']/div[5]/div[2]/text()").get()
        about_recruiter = response.xpath(
            "//div[@class='listingInfoContent'][1]/p[2]/text()"
        ).get()
        job_grade = (
            response.xpath(
                "substring-after(//div[@class='listingInfoContent'][1]/p[4]/text(), 'Job grade')"
            )
            .get()
            .strip()
        )
        # required_num =
        # department = ''

        # job_summary = ''
        # job_responsibities = ''
        # education_and_experience = ''
        # personal_skill = ''
        # how_to_apply = ''

        yield {
            "Catagory": catagory,
            "Employement_type": employement_type,
            "Salary": salary,
            "About_recruiter": about_recruiter,
            "Job_grade": job_grade,
        }
