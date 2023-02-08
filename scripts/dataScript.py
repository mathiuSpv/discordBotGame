from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base= declarative_base()
stats_name= ["EXP","PTS","VIG", "MIN", "END", "STR", "DEX", "INT"]

# class Player(Base):
#     pass

class playersDataStats():
    def __init__(self, file_user_stats):
        self.filename= file_user_stats
        self.users= self.__userSTATS()
    
    def __userSTATS(self):
        players_stats= dict()
        with open(f"./discordGame/{self.filename}.csv", mode= 'r') as file: players_list= file.readlines(); file.close()
        if players_list:
            for data in players_list:
                data= data.strip().split(";")[0][1:]; userID, userSTATS= int(data[0]), data[1:]
                players_stats[int(userID)]= dict(zip(userSTATS, stats_name))
        return players_stats
    
    def new_player(self, userID):
        userSTATS= [0,10,1,1,1,1,1,1]
        """"Parameters: userID"""
        with open(f"./discordGame/{self.filename}.csv", mode= 'a') as file: file.write(f"{userID};{userSTATS}\n"); file.close()
        self.users[userID]= dict(zip(userSTATS, stats_name))
        return
    
    def update(self):
        players_list= list(self.users.items())
        

class playerStats():
    def __init__(self, playerID, playerStats):
        self.playerID= playerID
        self.playerStats= playerStats
    
    def get_stats(self,):
        pass