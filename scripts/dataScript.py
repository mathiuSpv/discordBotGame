from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base= declarative_base()

class Player(Base):
    __tablename__= 'players'
    discord_id= Column(Integer, primary_key= True)

class PlayerLevel(Base):
    __tablename__= 'players_level'
    discord_id= Column(Integer, ForeignKey('players.discord_id'), primary_key= True)
    player_r_table= relationship('players', back_populates= 'players_level')
    level= Column(Integer)
    experience= Column(Integer)
    stats_points= Column(Integer)
    
class PlayerStats(Base):
    __tablename__= 'players_stats'
    discord_id= Column(Integer, ForeignKey('players.discord_id'), primary_key= True)
    player_r_table= relationship('players', back_populates= 'players_stats')
    vigor = Column(Integer)
    endurance = Column(Integer)
    strenght = Column(Integer)
    dexterity = Column(Integer)
    intelligence = Column(Integer)

class FunctionsPlayers():
    """Methods from Players"""
    def __init__(self, session):
        self.session = session

    def new_player(self, player_id):
        """Create a data of new player: player_id and player_stats"""
        player = Player(player_discord_id= player_id)
        player_level= PlayerLevel(discord_id= player_id,
                                  level= 1, experience= 0, stats_points= 9)
        player_stats= PlayerStats(discord_id= player_id,
                                  player_vig= 1, player_end= 1, player_str= 1, player_dex= 1, player_int= 1)
        self.session.add(player); self.session.add(player_level); self.session.add(player_stats)
        self.session.commit()
    
    def update_stats_info(self, player_id, player_stats: dict):
        """Must give a dictionary from .get_stats() modified"""
        player= self.session.query(PlayerStats).filter_by(player_discord_id= player_id).first()
        player.vigor= player_stats['vig']
        player.endurance= player_stats['end']
        player.strenght= player_stats['str']
        player.dexterity= player_stats['dex']
        player.intelligence= player_stats['int']
        self.session.commit()
        
    def update_level_info(self, player_id, player_level: dict):
        """Must give a dictionary from .get_level() modified"""
        player= self.session.query(PlayerLevel).filter_by(player_discord_id= player_id).first()
        player.level= player_level['lvl']
        player.experience= player_level['exp']
        player.stats_points = player_level['pts']
        self.session.commit()
        
    def get_user(self, player_id):
        """Get a boolean if it user exits"""
        player= self.session.query(Player).filter_by(player_discord_id= player_id).first()
        if player:
            return True
        else:
            return False
    
    def get_level(self, player_id):
        """Get level as Dictionary with keys: lvl, exp, pts"""
        player= self.session.query(PlayerLevel).filter_by(player_discord_id= player_id).first()
        return {'lvl': player.level, 'exp': player.experience, 'pts': player.stats_points}
        
    def get_stats(self, player_id):
        """Get stats as Dictionary with keys: vig, end, str, dex, int"""
        player= self.session.query(PlayerStats).filter_by(player_id= player_id).first()
        return {'vig': player.vigor, 'end': player.endurance,
                'str': player.strenght, 'dex': player.dexterity, 'int': player.intelligencet}


engine= create_engine('sqlite:///database/players.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session_player= Session()
player= FunctionsPlayers(session_player)