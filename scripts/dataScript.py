

class playersInfo():
    def __init__(self, filename):
        self.filename= filename
        self.userList= self.__users(filename)
    
    def __users(self, filename):
        players_system= dict()
        with open(f"./{filename}.csv", mode= 'r') as file: players_list= file.readlines(); file.close()
        if players_list:
            for data in players_list:
                userID, userNAME= data.strip().split(";")
                players_system[int(userID)]= userNAME
        return players_system
    
    def new_player(self, userID, userNAME):
        """"Parameters: userID, userNAME"""
        with open(f"{self.filename}.csv", mode= 'a') as file: file.write(f"{userID};{userNAME}\n"); file.close()
        self.playersList[userID]= userNAME
        return
        