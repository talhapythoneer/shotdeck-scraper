import scrapy
from scrapy.crawler import CrawlerProcess


class DayClass(scrapy.Spider):
    name = "PostcodesSpider"

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'ExteriorSunrise.csv',
        'CONCURRENT_REQUESTS': '1'
    }

    def start_requests(self):
        yield scrapy.Request(url="https://shotdeck.com/welcome/index", callback=self.parse)

    def parse(self, response):
        yield scrapy.FormRequest.from_response(response, formdata={
            "go": "1",
            "user": "sourcecinema24@gmail.com",
            "pass": "8LFP6ZQG",
            "stay": "1",
        }, callback=self.parse2)

    def parse2(self, response):
        for i in range(0, 300, 30):
            yield scrapy.Request(url="https://shotdeck.com/browse/searchstillsajax/" +
                                     "int_ext/Exterior/time_of_day/Sunrise/limit/30/offset/" +
                                     str(i),
                                 callback=self.parse3)

    def parse3(self, response):
        print(response.body)
        imagesData = response.css("div.outerimage")
        for image in imagesData:
            imgURL = "https://shotdeck.com" + image.css(
                "div > div:nth-of-type(1) > a > img::attr(src)").extract_first().replace("smthumb/small_", "")
            vidURL = ""
            if image.css("div > div:nth-of-type(2) > span::attr(class)").extract_first() == "yesclip":
                vidID = imgURL.split("/")
                vidID = vidID[-1]
                vidID = vidID.replace(".jpg", "")
                vidID = vidID.replace(".JPG", "")
                vidID = vidID.replace(".png", "")
                vidID = vidID.replace(".PNG", "")
                vidURL = "https://shotdeck.com/assets/images/clips/" + vidID + "_clip.mp4"
            yield {
                "Image URL": imgURL,
                "Video URL": vidURL,
                "Movie Name": image.css("div > div:nth-of-type(2) > a::text").extract_first()
            }


process = CrawlerProcess()
process.crawl(DayClass)
process.start()
