from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class testTable(Base):
    __tablename__ = 'testTable'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    area_id = Column(Integer, ForeignKey('area.id'))

    def __repr__(self):
        return f'<testTalbe {self.name}>'


class area(Base):
    __tablename__ = 'area'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship('testTable', backref="area")

    def __repr__(self):
        return f'<area {self.name}>'


engine = create_engine('sqlite:///F:/projects/sqltest/testDB.db')
Session = sessionmaker(engine)

if __name__ == '__main__':
    s = Session()
    xm = s.query(testTable).filter(testTable.name == 'xiaoming').one()
    nj = s.query(area).filter(area.name == 'nanjing').one()
    xm.area = nj
    s.add(xm)
    s.commit()
