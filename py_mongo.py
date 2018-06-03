import pymongo
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId


class Mongo(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['interfacelift']

    def add_one(self, obj, data):
        '''新增一条数据'''
        print("mongodb 新增一条数据", data)
        return self.db[obj].insert_one(data)

    def add_many(self, obj, data):
        '''新增多条数据'''
        return self.db[obj].insert_many(data)

    def get_one(self, obj, params):
        '''查询一条数据'''
        return self.db[obj].find_one(params)

    def count(self, obj, params):
        '''统计总条数'''
        return self.db[obj].find(params).count()

    # pymongo.ASCENDING升序,pymongo.DESCENDING 降序
    def get_many(self, obj, params, page_index=1, page_size=10, sortby="_id", sortdir=pymongo.DESCENDING):
        '''查询多条数据'''
        return self.db[obj].find(params).skip(int((page_index-1))*int(page_size)).limit(int(page_size)).sort(sortby,sortdir)

    def update_one(self, obj, params, data):
        '''更新一条数据'''
        return self.db[obj].update_one(params, data)

    def update_many(self, obj, params, data):
        '''更新多条数据'''
        return self.db[obj].update_many(params, data)

    def delete_one(self, obj, params):
        '''删除一条数据'''
        return self.db[obj].delete_one(params)

    def delete_many(self, obj, params):
        '''删除多条数据'''
        return self.db[obj].delete_many(params)


def main():
    obj = Mongo()

    # 添加数据
    # data = {
    #     'proportion': '新加118888811',
    #     'url': 'qazwsx',
    #     'time': datetime.now()
    # }
    # rest = obj.add_one('res_widescreen_16_10',data)
    # print(rest)
    # print(rest.inserted_id)

    # 查询一条
    # rest = obj.get_one('res_widescreen_16_10', {"url": "qazwsx"})
    # print("查询", rest)

    # 统计条数
    # rest = obj.count('res_widescreen_16_10', {"url": "qazwsx"})
    # print("统计条数", rest)

    # 查询多条
    # rest = obj.get_many('res_widescreen_16_10', {"url": "qazwsx"})
    # for item in rest:
    #     print("查询多条", item)

    # 更新一条数据
    # rest = obj.update_one('res_widescreen_16_10', {'url': 'qazwsx'}, {'$inc': {'age': 1}})
    # print("更新一条数据", rest)
    # print(rest.matched_count, rest.modified_count)

    # 更新多条数据
    # rest = obj.update_many('res_widescreen_16_10', {'url': 'qazwsx'}, {'$inc': {'age': 10}})
    # print("更新多条数据", rest)
    # print(rest.matched_count, rest.modified_count)

    # 删除一条数据
    # rest = obj.delete_one('res_widescreen_16_10', {'age': 12})
    # print("删除一条数据", rest)
    # print(rest.deleted_count)

    # 删除多条数据
    # rest = obj.delete_many('res_widescreen_16_10', {'age': 10})
    # print("删除多条数据", rest)
    # print(rest.deleted_count)


if __name__ == '__main__':
    main()

