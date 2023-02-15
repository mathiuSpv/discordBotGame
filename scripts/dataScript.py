from sqlalchemy import create_engine, Column, Integer, Float, String, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base= declarative_base()

class Player(Base):
    __tablename__= 'players'
    player_discord_id= Column(Integer, primary_key= True)

class PlayerStats(Base):
    __tablename__= 'players_stats'
    player_discord_id= Column(Integer, ForeignKey('players.player_discord_id'), primary_key= True)
    player_table= relationship('players', back_populates= 'players_stats')
    player_exp= Column(Integer)
    player_pts= Column(Integer)
    player_vig = Column(Integer)
    player_end = Column(Integer)
    player_str = Column(Integer)
    player_dex = Column(Integer)
    player_int = Column(Integer)

class PlayerFunctions():
    """Methods of Players"""
    def __init__(self, session):
        self.session = session

    def new_player(self, player_id):
        player = Player(player_discord_id= player_id)
        player_stats= PlayerStats(player_id= player_id, player_exp= 0, player_pts= 8,
                                  player_vig= 1, player_end= 1, player_str= 1, player_dex= 1, player_int= 1)
        self.session.add(player); self.session.add(player_stats)
        self.session.commit()
    
    def update_stats(self, player_id, player_pts, player_vig, player_min, player_end, player_str, player_dex, player_int):
        player= self.session.query(PlayerStats).filter_by(player_discord_id= player_id).first()
        player.player_pts= player_pts
        player.player_vig= player_vig
        player.player_min= player_min
        player.player_end= player_end
        player.player_str= player_str
        player.player_dex= player_dex
        player.player_int= player_int
        self.session.commit()
        
    def update_exp(self, player_id, player_exp):
        player= self.session.query(PlayerStats).filter_by(player_discord_id= player_id).first()
        player.player_exp= player_exp
        self.session.commit()
        
    def get_user(self, player_id):
        """Get a boolean if it user exits"""
        player= self.session.query(Player).filter_by(player_discord_id= player_id).first()
        if player:
            return True
        else:
            return False
        
    def get_stats(self, player_id):
        """Get stats as Dictionary with keys: exp, pts, vig, end, str, dex, int"""
        player= self.session.query(PlayerStats).filter_by(player_id= player_id).first()
        return {'exp':player.player_exp, 'pts':player.player_pts, 
                'vig':player.player_vig, 'end':player.player_end,
                'str':player.player_str, 'dex':player.player_dex, 'int':player.player_int}


engine= create_engine('sqlite:///database/players.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session_player= Session()
player= PlayerFunctions(session_player)