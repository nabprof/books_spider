"""
BooksSpider
---------

Spider for extracting book details from https://books.toscrape.com/

"""
import os
from urllib.parse import urljoin
import scrapy
from scrapy.exceptions import CloseSpider

class BooksSpider(scrapy.Spider):
    """
    Spider class for extracting book details.

    Parameters
    ----------
    is_dump : boolean,
        Choose whether to save pages visited

    Attributes
    ----------
    max_items: str
        Maximum items to scrape.
        Passed as command line argument (-a maxitems=750).

    save_dumps : str
        Save response in "data_dumps" directory.
        Passed as command line argument (-a save_dumps=true).

    Methods
    -------
    parse(response)
        Extracts links for all catergories from home page and
        calls parse_category() for each category.

    parse_category(response)
        Extracts book_elements for a single category page and
        calls get_book_details() for each book element.

        If a category has more than one page, extract link for
        next_page and calls parse_category() for that.

    get_book_details(book_element, curr_url)
        Extracts title, price, image_url and details_url for a
        single book.

    save_response(response)
        Save reponse in "data_dumps" directory.

    """
    name = "books"
    start_urls = [
        "https://books.toscrape.com/",
    ]

    def __init__(self, max_items=None, save_dumps=None, **kwargs):
        super().__init__(**kwargs)

        # checking if command line arguments are passed
        if max_items is None:
            self.logger.info("No command line argument passed for 'max_items'")
            max_items = 1000
        else:
            self.logger.info(f"Command line argument passed, max_items={max_items}")
            max_items = int(max_items)

        if save_dumps is None:
            self.logger.info("No command line argument passed for 'save_dumps'")
            save_dumps = False
        else:
            self.logger.info(f"Command line argument passed, save_dumps={save_dumps}")
            if save_dumps == "true":
                save_dumps = True
            elif save_dumps == "false":
                save_dumps = False
            else:
                self.logger.info("Invalid Command line argument passed for save_dumps")

        self.max_item_cnt = max_items
        self.item_cnt = 0
        self.save_dumps = save_dumps


    def parse(self, response):
        """
        This function parses the home page and extracts the links for different
        categories.

        @url https://books.toscrape.com
        @returns requests 50 50
        """
        category_anchors = response.css('div.side_categories').css("ul li ul li a")
        yield from response.follow_all(category_anchors, callback=self.parse_category)

    def parse_category(self, response):
        """
        This function parses a single category page and extracts book elements.
        If a next page exists for a category, that is also parsed.

        @url https://books.toscrape.com/catalogue/category/books/travel_2/index.html
        @returns items 11 11
        @scrapes title price image_url details_url
        """
        if self.save_dumps:
            self.save_response(response)

        book_elements = response.css("article.product_pod")
        curr_url = response.url

        for book_element in book_elements:
            yield self.get_book_details(book_element, curr_url)

        next_page = response.css("ul.pager li.next a::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_category)

    def get_book_details(self, book_element, curr_url):
        """
        This function parses details of a single book.
        Extracts title, price, image_url and details_url for a single book.
        """
        self.item_cnt += 1

        if self.item_cnt > self.max_item_cnt:
            raise CloseSpider('Maximum item count reached. Closing spider.')

        price = book_element.css("div.product_price p.price_color").xpath("./text()").get()

        title_url_element = book_element.css("h3 a")
        title = title_url_element.attrib["title"]

        book_details_relative_url = title_url_element.attrib["href"]
        ## absolute url
        book_details_url = urljoin(curr_url, book_details_relative_url)

        book_image_relative_url =  book_element.css("div.image_container a img::attr(src)").get()
        ## absolute url
        book_image_url = urljoin(curr_url, book_image_relative_url)

        res = {"title": title,
               "price": price,
               "image_url": book_image_url,
               "details_url": book_details_url}

        return res

    def save_response(self, response):
        """
        This function saves contents in "data_dumps" directory.
        If "data_dumps" directory is not present in current directory, it is created.
        This function is called when command line argument save_dumps=true
        """
        page_name = "_".join(response.url.split("/")[-2:])

        data_dumps_dir = os.path.join(os.getcwd(), "data_dumps")
        if not os.path.exists(data_dumps_dir):
            self.logger.info("Creating data_dumps directory.")
            os.mkdir(data_dumps_dir)

        filename = os.path.join(data_dumps_dir, page_name)
        self.logger.info(f"saving file: {filename}" +
                       f" for response of url: {response.url}")

        with open(filename, "w", encoding="UTF-8") as f:
            f.write(response.text)
