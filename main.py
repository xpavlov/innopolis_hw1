import aiohttp
import aiomysql

from aiohttp import web

async def init_db(app):
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,user='root', password='',db='innopolis')
    app['db'] = pool
    yield
    app['db'].close()
    await app['db'].wait_closed()

routes = web.RouteTableDef()

async def simple_fetch_data(pool,query):
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(query)
            rows = await cur.fetchall()
             #this is a very important thing without it you will not see the changes and will receive the same values across all the time!
            await conn.commit()
            return rows

async def simple_insert_singlerow_data(pool,query,data):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query,data)
            #it's ok for no await here it throws an error if await is used
            id = {"id":conn.insert_id()}
            await cur.execute("commit")
            #this is a very important thing without it you will not see the changes and will receive the same values across all the time!
            await conn.commit()
            return id

@routes.get('/stores')
async def get_stores(request):
    rows = await simple_fetch_data(request.app["db"],"select * from stores")
    return web.json_response(rows)

@routes.get('/items')
async def get_items(request):
    rows = await simple_fetch_data(request.app["db"],"select * from items")
    return web.json_response(rows)

@routes.get('/top10shops')
async def get_items(request):
    rows = await simple_fetch_data(request.app["db"],"select s.name as store_name, s.address as store_address, sum(i.price) as total_sales from (select * from sales WHERE sale_date BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW()) sl inner join stores s on sl.store_id=s.id inner join items i on sl.item_id=i.id group by s.id order by total_sales desc limit 0,10")
    return web.json_response(rows)

@routes.get('/top10items')
async def get_items(request):
    rows = await simple_fetch_data(request.app["db"],"select i.name, count(sl.item_id) as total from sales sl inner join items i on sl.item_id=i.id group by sl.item_id order by total desc limit 0,10")
    return web.json_response(rows)

# example {"store_id":18,"item_id":4}
@routes.post('/addsale')
async def add_sale(request):
     data = await request.json()
     pool = request.app["db"]
     query ="insert into sales (store_id, item_id) values (%(store_id)s,%(item_id)s)"
     resp = await simple_insert_singlerow_data(pool,query,data)
     return web.json_response(resp)

#example {"name":"6th item", "price": 1.6}
@routes.post('/additem')
async def add_sale(request):
     data = await request.json()
     pool = request.app["db"]
     query ="insert into items (name, price) values (%(name)s,%(price)s)"
     resp = await simple_insert_singlerow_data(pool,query,data)
     return web.json_response(resp)

# example {"name":"Test 2", "address": "test address"}
@routes.post('/addstore')
async def add_sale(request):
     data = await request.json()
     pool = request.app["db"]
     query ="insert into stores (name, address) values (%(name)s,%(address)s)"
     resp = await simple_insert_singlerow_data(pool,query,data)
     return web.json_response(resp)
     #return web.Response(status=200)

def main():
    app = web.Application()
    app.cleanup_ctx.append(init_db)
    app.add_routes(routes)
    web.run_app(app)

if __name__ == '__main__':
    main()