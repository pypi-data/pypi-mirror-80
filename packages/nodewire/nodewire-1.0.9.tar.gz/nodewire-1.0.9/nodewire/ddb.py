import asyncio
import motor.motor_asyncio
from bson.objectid import ObjectId


class db(object):
    def __init__(self, server = '138.197.6.173', database='4uvbzvlwyyia'):
        mongo_client = motor.motor_asyncio.AsyncIOMotorClient(server, 27017)
        # self.server = server
        self.database = mongo_client[database]

    async def get(self, table, query, projection=None, options={}):
        """ahmad = await db.get('test', {'age', 20})"""
        collection = self.database[table]
        if type(query) is list:
            pipeline = query
            # if '_id' in query: query['_id'] = ObjectId(query['_id'])
            results = await collection.aggregate(pipeline).to_list(None)
            rs = []
            try:
                for result in results:
                    if '_id' in result: result['_id'] = str(result['_id'])
                    rs.append(result)
                return rs
            except Exception as ex:
                print('pass 4')
        else:
            if '_id' in query: query['_id'] = ObjectId(query['_id'])
            if projection == None and options == {}:
                results = await collection.find(query).to_list(None)
            else:
                sort = options['$sort'] if '$sort' in options else {}
                limit = options['$limit'] if '$limit' in options else {}
                skip = options['$skip'] if '$skip' in options else 0
                if sort != {} and type(sort) == dict:
                    sort = list(sort.items())
                if sort and limit:
                    results = await collection.find(query, projection).skip(skip).sort(sort).limit(limit).to_list(None)
                elif sort:
                    results = await collection.find(query, projection).skip(skip).sort(sort).to_list(None)
                elif limit:
                    results = await collection.find(query, projection).skip(skip).limit(limit).to_list(None)
                else:
                    results = await collection.find(query, projection).skip(skip).to_list(None)
            for result in results:
                if '_id' in result: result['_id'] = str(result['_id'])
            return results

    async def first(self, table, query, projection=None, options=None):
        result = await self.get(table, query, projection, options if options else {'$limit':1})
        if result:
            return result[0]
        else:
            return None

    async def last(self, table, query, projection=None, options=None):
        result = await self.get(table, query, projection, options if options else {'$limit':1, '$sort':{'$natural':-1}})
        if result:
            return result[-1]
        else:
            return None

    async def index(self, table, keys, options = None):
        collection = self.database[table]
        if isinstance(keys, dict):
            keys = [(k, keys[k]) for k in keys]
        if options:
            await collection.create_index(keys, background=True, **options)
        else:
            await collection.create_index(keys, background=True)

    async def drop(self, table):
        """db.drop('test')"""
        collection = self.database[table]
        await collection.drop()

    async def remove(self, table, query):
        """db.remove('test', {'age',40})"""
        collection = self.database[table]
        if '_id' in query: query['_id'] = ObjectId(query['_id'])
        await collection.delete_many(query)

    async def set(self, table, docs):
        """db.set('test', {'name':'ahmad', 'age': 40})"""
        collection = self.database[table]
        if type(docs) is dict:
            docs = [docs]
        for doc in docs:
            if '_id' in doc:
                doc['_id'] = ObjectId(doc['_id'])
                await collection.replace_one({'_id': doc['_id']}, doc)
                id = doc['_id']
            else:
                result = (await collection.insert_one(doc))
                id = result.inserted_id
        return id

    async def update(self, table, query, doc):
        """db.set('test', {'name':'ahmad', 'age': 40}, {'$set':{'age':41}})"""
        collection = self.database[table]
        if isinstance(doc, list) or '$set' in doc:
            id = await collection.update_many(query, doc)  # update_many
        else:
            id = await collection.replace_one(query, doc)  # replace one
        return id


if __name__ == '__main__':
    async def myloop():
        mydb = db(server='localhost')
        # id = await mydb.set('test', {'name': 'ahmad sadiq', 'age': 43})
        ahmad = await mydb.first('test', {})
        print(ahmad)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(myloop())