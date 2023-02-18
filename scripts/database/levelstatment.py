from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from math import factorial

Base= declarative_base()


class LevelStatment(Base):
    __tablename__= 'level_requied'
    level= Column(Integer, primary_key= True)
    exp_needed= Column(Integer)
    points_add= Column(Integer)
    
def session_level():
    engine= create_engine('sqlite:///database/levelstatment.db')
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    session= session()
    return session    
__session= session_level()
class LevelFunctions():
    
    def __init__(self, session):
        self.session= session

    lvl_max= 60
    def create_lvl_statment(self):
        exp_ecuation= lambda x: int((factorial(x)/(1.75*factorial(x-2)))+24) if x >1 else 0
        points_ecuation= lambda x: 1 if x !=  1 and x != self.lvl_max else 5
        levels= list()
        for n_level in range(1, self.lvl_max+1 ):
            level= LevelStatment(level= n_level, exp_needed= exp_ecuation(n_level), points_add= points_ecuation(n_level))
            levels.append(level)
        self.session.add_all(levels)
        self.session.commit()
            
    def get_exp_needed(self, lvl: int):
        """Get exp needed for the next level if not can level up return None"""
        lvl = self.session.query(LevelStatment).filter_by(level=lvl+1).one_or_none()
        if lvl is not None:
            return lvl.exp_needed
        return None
    
    def get_points_add(self, lvl: int):
        """Get points add for the next level if not can level up return None"""
        lvl = self.session.query(LevelStatment).filter_by(level=lvl+1).one_or_none()
        if lvl is not None:
            return lvl.points_add
        return None
level= LevelFunctions(__session)


if __name__ == "__main__":
    cmd= input("del for delete\nrl for reload\n>>  ")
    while cmd:
        if cmd == 'del':
            level.delete()
            __session.commit()
            __session.close()
            print("Done")
        elif cmd == 'rl':
            level.create_lvl_statment()
            __session.commit()
            __session.close()
        cmd= input("del for delete\nrl for reload\n>>  ")