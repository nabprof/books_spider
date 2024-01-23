This project scrapes extracts book details from https://books.toscrape.com/.
The scraping is done by visiting category pages whose links are present in the home page.


1. Running the project

	The spider can be run in the project directory with the following command:

	    scrapy crawl books -O book_details.json

	The results will be stored in book_details.json .


2. Limiting the maximum number of items scraped.

	The maximum number of items to be scraped can be limited by command line argument "max_items".

	    scrapy crawl books -O book_details.json -a max_items=750


3. Saving the response pages.

	The response pages can be saved by specifying the command line argument "save_dumps".

	    scrapy crawl books -O book_details.json -a save_dumps=true


4. Custom Middleware

	A custom middleware RandomUserAgentMiddleware is added to select random user-agent for each request.
	This is specified in settings.py as:

		...
		DOWNLOADER_MIDDLEWARES = {
		   'books_details.middlewares.RandomUserAgentMiddleware': 350,
		}
		...


5. Custom Pipeline

	A custom pipeline BookPricePipeline is added, which removes the pound sign '£' from the price and converts it into numerical type.
	This is specified in settings.py as:

		...
		ITEM_PIPELINES = {
		    "books_details.pipelines.BookPricePipeline": 250,
		}
		...

6. Contracts

    The spider has the following contracts:

    1. parse()
       
	    @url https://books.toscrape.com \
	    @returns requests 50 50

    This number of requests : 50 corresponds to the 50 categories present on the home page (https://books.toscrape.com)

    2. parse_category()
       
         @url https://books.toscrape.com/catalogue/category/books/travel_2/index.html \
         @returns items 11 11 \
         @scrapes title price image_url details_url

     The 11 items contract corresponds to "11 results" for books present for "travel" category present on url : https://books.toscrape.com/catalogue/category/books/travel_2/index.html
	
     The "scrapes" contracts ensure that the fields: title, price, image_url and details_url are present in the items scraped.

     The contracts can be run in the project directory with the following command:

	    scrapy check

