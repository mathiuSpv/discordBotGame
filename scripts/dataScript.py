from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

Base= declarative_base()

class Player(Base):
    __tablename__= 'players'
    discord_id= Column(Integer, primary_key= True)
    level= relationship('PlayerLevel')
    stats= relationship('PlayerStats')

class PlayerLevel(Base):
    __tablename__= 'players_level'
    discord_id= Column(Integer, ForeignKey('players.discord_id'), primary_key= True)
    n_level= Column(Integer)
    experience= Column(Integer)
    stats_points= Column(Integer)
    
class PlayerStats(Base):
    __tablename__= 'players_stats'
    discord_id= Column(Integer, ForeignKey('players.discord_id'), primary_key= True)
    vigor= Column(Integer)
    endurance= Column(Integer)
    strenght= Column(Integer)
    dexterity= Column(Integer)
    intelligence= Column(Integer)

class FunctionsPlayers():
    """Methods from Players"""
    def __init__(self, session):
        self.session = session

    def new_player(self, player_id):
        """Create a data of new player: player_id and player_stats"""
        player = Player(discord_id= player_id)
        player.level= [PlayerLevel(n_level= 1, experience= 0, stats_points= 9)]
        player.stats= [PlayerStats(vigor= 1, endurance= 1, strenght= 1, dexterity= 1, intelligence= 1)]
        self.session.add(player)
        self.session.commit()
        self.session.close()
        
    def update_stats_info(self, player_id, player_stats: dict):
        """Must give a dictionary from .get_stats() modified"""
        player= self.session.query(PlayerStats).filter_by(discord_id= player_id).first()
        player.vigor= player_stats['vig']
        player.endurance= player_stats['end']
        player.strenght= player_stats['str']
        player.dexterity= player_stats['dex']
        player.intelligence= player_stats['int']
        self.session.commit()
        self.session.close()
        
    def update_level_info(self, player_id, player_level: dict):
        """Must give a dictionary from .get_level() modified"""
        player= self.session.query(PlayerLevel).filter_by(discord_id= player_id).first()
        player.n_level= player_level['lvl']
        player.experience= player_level['exp']
        player.stats_points = player_level['pts']
        self.session.commit()
        self.session.close()
        
    def get_user(self, player_id):
        """Get a boolean if it user exits"""
        if self.session.query(Player).filter(Player.discord_id== player_id).first():
            return True
        else:
            return False
    
    def get_level(self, player_id):
        """Get level as Dictionary with keys: lvl, exp, pts"""
        player= self.session.query(PlayerLevel).filter_by(discord_id= player_id).first()
        self.session.close()
        return {'lvl': player.n_level, 'exp': player.experience, 'pts': player.stats_points}
        
    def get_stats(self, player_id):
        """Get stats as Dictionary with keys: vig, end, str, dex, int"""
        player= self.session.query(PlayerStats).filter_by(discord_id= player_id).first()
        self.session.close()
        return {'vig': player.vigor, 'end': player.endurance,
                'str': player.strenght, 'dex': player.dexterity, 'int': player.intelligence}
    
    def delete_db(self):
        """Delete all Player Data Base"""
        self.session.query(Player).delete()
        self.session.query(PlayerLevel).delete()
        self.session.query(PlayerStats).delete()
        self.session.commit()
        self.session.close()


engine_player= create_engine('sqlite:///database/players.db')
Base.metadata.create_all(engine_player)
session_player = sessionmaker(bind=engine_player)
session_player= session_player()
player_db= FunctionsPlayers(session_player)