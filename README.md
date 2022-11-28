# A simple aiohttp and aiomysql demo

##Setting everything up:
__1.__ Create mysql database and import init_db.sql. This is phpmyadmin-generated dump of the test database without any data. I e it contains only structure. Note that maybe you will have to change manually encoding before import for every table if you want to use utf8 (the default charset was set to latin1)

__2.__ Edit main.py and fill aiomysql.create_pool(...) function call with actual database credentials.

__3.__ Run __pip install -r requirements.txt__

__4.__ To start app simply run  __python main.py__ By default the app listens on 127.0.0.1 port 8080 (You will be noticed it after app launch - just check the console

# Routes

To add data you can post json to (beware of content-type header!):

/addstore - to add new store. Example: {"name":"Test 2", "address": "test address"}

/additem - example: {"name":"6th item", "price": 1.6}

/addsale - to link one sale and store - example: {"store_id":18,"item_id":4}

Every successful request will return 200 OK with corresponding new record id wrapped in json.

To get data:

all stores - /stores

all items - /items

Top 10 selling stores (with actual income) within last 30 days. /top10shops

10 bestselling items across all time - /top10items



