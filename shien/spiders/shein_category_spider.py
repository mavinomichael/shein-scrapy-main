import scrapy
from ..items import ShienProductItem
import re
from scrapy.exporters import JsonLinesItemExporter


class ShienProductsByCategorySpider(scrapy.Spider):
    name = "shein_product_by_category_spider"
    page_number = 2
    start_urls = [
        "https://us.shein.com/style/Men-Clothing-sc-001121429.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_16%60ps%3D4_10%60jc%3DitemPicking_001121429&src_tab_page_id=page_home1685081052871&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D4592778_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-10_ABT%3DSPcCccWomenHomepage_expgroup_100004156&page=1"]

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.HEADERS)

    def parse(self, response):
        product = ShienProductItem()

        all_products = response.css(".product-list.j-expose__product-list.j-product-list-info.j-da-event-box")
        last_pagination_link = response.css("div > span.sui-pagination__total").get()
        # last_item =  int(re.findall(r'\d+',last_pagination_link))
        # print(last_item,"lastitem")
        last_item = 40
        exporter = JsonLinesItemExporter(open('products.json', 'ab'))

        for prod in all_products:
            name = prod.css(".S-product-item__link::text").get()
            price = prod.css("span.normal-price-ctn__sale-price::text").get()
            image = "https:" + prod.css(
                ".S-product-item.j-expose__product-item.product-list__item>.S-product-item__wrapper>.S-product-item__img-container.j-expose__product-item-img>.falcon-lazyload::attr(data-src)").get()
            url = "https://us.shein.com" + prod.css(
                ".S-product-item.j-expose__product-item.product-list__item>.S-product-item__wrapper>.S-product-item__img-container.j-expose__product-item-img::attr(href)").get()

            product['name'] = name
            product['price'] = price
            product['image'] = image
            product['source'] = "shein"
            product['url'] = url
            # product['last_modified'] = datetime.now().isoformat()

            exporter.export_item(product)

            yield product

        next_page = f'https://us.shein.com/style/Men-Clothing-sc-001121429.html?src_module=Women&src_identifier=on%3DIMAGE_COMPONENT%60cn%3Dcat%60hz%3DhotZone_16%60ps%3D4_10%60jc%3DitemPicking_001121429&src_tab_page_id=page_home1685081052871&ici=CCCSN%3DWomen_ON%3DIMAGE_COMPONENT_OI%3D4592778_CN%3DONE_IMAGE_COMPONENT_TI%3D50001_aod%3D0_PS%3D4-10_ABT%3DSPcCccWomenHomepage_expgroup_100004156&page={str(self.page_number)}'

        if self.page_number <= last_item:
            self.page_number += 1
            print(next_page)
            yield response.follow(next_page, callback=self.parse, headers=self.HEADERS)
