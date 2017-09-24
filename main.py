from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    dist_id = Column(Integer, ForeignKey('dist.id'))

    def __repr__(self):
        return f'<User {self.name}>'


class Dist(Base):
    __tablename__ = 'dist'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city_id = Column(Integer, ForeignKey('city.id'))
    users = relationship('User', backref="dist")

    def __repr__(self):
        return f'<Dist {self.name}>'


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    districts = relationship('Dist', backref="city")

    def __repr__(self):
        return f'<City {self.name}>'


engine = create_engine('sqlite:///F:/projects/sqltest/testDB.db')
Session = sessionmaker(engine)

if __name__ == '__main__':
    # 连接
    s = Session()
    # 查询
    xm = s.query(User).filter(User.name == 'xiaoming').one()
    jiangning = s.query(Dist).filter(Dist.name == 'jiangning').one()
    # 改写
    xm.dist = jiangning
    s.add(xm)
    s.commit()
    # pandas.read
    query = s.query(User).filter(User.dist == jiangning)
    df = pd.read_sql(query.statement, s.bind, index_col='id')
    # in的用法
    query = s.query(User).filter(User.name.in_(['xiaoming', 'xiaohong']))
