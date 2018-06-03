from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import and_
# 引入创建session连接会话需要的处理
from sqlalchemy.orm import sessionmaker

from datetime import datetime

engine = create_engine('mysql://root:root@127.0.0.1:3306/interfacelift?charset=utf8', encoding="utf-8", echo=True)
Base = declarative_base()

# 创建一个连接会话对象；需要指定是和那个数据库引擎之间的会话
Session = sessionmaker(bind=engine)

#声明一个创建的class
class RES_WIDESCREEN_16_10(Base):
    # 表名
    __tablename__ = 'RES_WIDESCREEN_16_10'
    id = Column(Integer, primary_key=True)
    proportion = Column(String(20))
    url = Column(String(300))
    time = Column(DateTime, default=datetime.now())
    # 转换成json格式
    def to_json(self):
        return {
            'id': self.id,
            'proportion': self.proportion,
            'url': self.url,
            'time': self.time
        }

class RES_WIDESCREEN_16_9(Base):
    __tablename__ = 'RES_WIDESCREEN_16_9'
    id = Column(Integer, primary_key=True)
    proportion = Column(String(20), nullable=False)
    url = Column(String(300), nullable=False)
    time = Column(DateTime, default=datetime.now())
    def to_json(self):
        return {
            'id': self.id,
            'proportion': self.proportion,
            'url': self.url,
            'time': self.time
        }

class RES_WIDESCREEN_21_9(Base):
    __tablename__ = 'RES_WIDESCREEN_21_9'
    id = Column(Integer, primary_key=True)
    proportion = Column(String(20), nullable=False)
    url = Column(String(300), nullable=False)
    time = Column(DateTime, default=datetime.now())
    def to_json(self):
        return {
            'id': self.id,
            'proportion': self.proportion,
            'url': self.url,
            'time': self.time
        }

class RES_DUAL_MONITORS(Base):
    __tablename__ = 'RES_DUAL_MONITORS'
    id = Column(Integer, primary_key=True)
    proportion = Column(String(20), nullable=False)
    url = Column(String(300), nullable=False)
    time = Column(DateTime, default=datetime.now())
    def to_json(self):
        return {
            'id': self.id,
            'proportion': self.proportion,
            'url': self.url,
            'time': self.time
        }

class RES_TRIPLE_MONITORS(Base):
    __tablename__ = 'RES_TRIPLE_MONITORS'
    id = Column(Integer, primary_key=True)
    proportion = Column(String(20), nullable=False)
    url = Column(String(300), nullable=False)
    time = Column(DateTime, default=datetime.now())
    def to_json(self):
        return {
            'id': self.id,
            'proportion': self.proportion,
            'url': self.url,
            'time': self.time
        }

class RES_IPHONE(Base):
    __tablename__ = 'RES_IPHONE'
    id = Column(Integer, primary_key=True)
    proportion = Column(String(20), nullable=False)
    url = Column(String(300), nullable=False)
    time = Column(DateTime, default=datetime.now())
    def to_json(self):
        return {
            'id': self.id,
            'proportion': self.proportion,
            'url': self.url,
            'time': self.time
        }

class RES_IPAD(Base):
    __tablename__ = 'RES_IPAD'
    id = Column(Integer, primary_key=True)
    proportion = Column(String(20), nullable=False)
    url = Column(String(300), nullable=False)
    time = Column(DateTime, default=datetime.now())
    def to_json(self):
        return {
            'id': self.id,
            'proportion': self.proportion,
            'url': self.url,
            'time': self.time
        }

class RES_ANDROID(Base):
    __tablename__ = 'RES_ANDROID'
    id = Column(Integer, primary_key=True)
    proportion = Column(String(20), nullable=False)
    url = Column(String(300), nullable=False)
    time = Column(DateTime, default=datetime.now())
    def to_json(self):
        return {
            'id': self.id,
            'proportion': self.proportion,
            'url': self.url,
            'time': self.time
        }


class MysqlOrmInit(object):
    # 初始化
    def __init__(self):
        self.session = Session()

    def add_one(self, table, data):
        '''添加一条记录'''
        new_obj = table(
            proportion=data["proportion"],
            url=data["url"]
        )
        self.session.add(new_obj)
        self.session.commit()
        return new_obj

    def get_one(self, table, *params):
        '''获取一条数据'''
        # print("查询参数", params)
        return self.session.query(table).filter(and_(*params)).first()

    def get_many(self, table, *params, page_index=1, page_size=10):
        '''获取多条数据'''
        # print("查询参数", params)
        return self.session.query(table).filter(and_(*params)).offset(int(page_index - 1) * int(page_size)).limit(int(page_size)).all()

    def count(self, table, *params):
        '''统计条数'''
        return self.session.query(table).filter(and_(*params)).count()
        # return self.session.query(func.count(User.id))


    def update(self, table, data, *params):
        '''更新数据'''
        print("data", data)
        rest = self.session.query(table).filter(and_(*params)).update(data)
        self.session.commit()
        return rest

    def delete(self, table, *params):
        '''删除数据'''
        data = self.session.query(table).filter(and_(*params)).all()
        if data:
            for item in data:
                self.session.delete(item)
            self.session.commit()
            return True
        else:
            return False

def main():
    obj = MysqlOrmInit()

    # 添加数据
    data = {
        'proportion': '6400x4000',
        'url': 'https://www.baidu.com/img/bd_logo1.png'
    }
    rest = obj.add_one(RES_WIDESCREEN_16_10, data)
    print('rest: %s' % rest)
    print("rest.id", rest.id)

    # 统计条数
    # prams = (
    #     # RES_WIDESCREEN_16_10.id == 2,
    #     RES_WIDESCREEN_16_10.url == 'https://www.baidu.com/img/bd_logo1.png',
    # )
    # rest = obj.count(RES_WIDESCREEN_16_10, *prams)
    # print("统计条数", rest)

    # 查询一条数据
    # prams = (
    #     RES_WIDESCREEN_16_10.url == 'https://www.baidu.com/img/bd_logo1.png',
    # )
    # rest = obj.get_one(RES_WIDESCREEN_16_10, *prams)
    # print("一条数据", rest.to_json())

    # 查询多条数据
    # prams = (
    #     # RES_WIDESCREEN_16_10.id == 2,
    #     RES_WIDESCREEN_16_10.url == 'https://www.baidu.com/img/bd_logo1.png',
    # )
    # rest = obj.get_many(RES_WIDESCREEN_16_10, *prams)
    # data = []
    # for x in rest:
    #     data.append(x.to_json())
    # print(data)

    # 更新数据
    # prams = (
    #         # RES_WIDESCREEN_16_10.id == 2,
    #         RES_WIDESCREEN_16_10.url == 'https://www.baidu.com/img/bd_logo1.png',
    #     )
    # data = {
    #     RES_WIDESCREEN_16_10.url: 'url123',
    #     RES_WIDESCREEN_16_10.proportion: 'proportion456'
    # }
    # rest = obj.update(RES_WIDESCREEN_16_10, data, *prams)
    # print("更新数据", rest)


    # 删除数据
    # prams = (
    #         # RES_WIDESCREEN_16_10.id == 13,
    #         RES_WIDESCREEN_16_10.url == 'url123',
    #     )
    # rest = obj.delete(RES_WIDESCREEN_16_10, *prams)
    # print("删除数据", rest)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    # main()

