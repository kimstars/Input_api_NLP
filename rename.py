import pymongo


myclient = pymongo.MongoClient("mongodb://chukim2001:kietkiet@cluster0-shard-00-00.zrxqw.mongodb.net:27017,cluster0-shard-00-01.zrxqw.mongodb.net:27017,cluster0-shard-00-02.zrxqw.mongodb.net:27017/kiet?ssl=true&replicaSet=atlas-gulela-shard-0&authSource=admin&retryWrites=true&w=majority")

mydb = myclient["NLPdataBase"]
collection = mydb["database"]

mydb.database.rename('Normans')