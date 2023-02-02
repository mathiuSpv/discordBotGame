

class playersInfo():
    def __init__(self, filename):
        self.filename= filename
        self.playersList= self.__players(filename)
    
    def __players(self, filename):
        players_system= dict()
        with open(f"./{filename}.csv", mode= 'r') as file: players_list= file.readlines(); file.close()
        if players_list:
            for data in players_list:
                user_id, user_name= data.strip().split(";")
                players_system[f'{user_id}']= user_name
        return players_system
    
    def new_player(self, user_id, user_name):
        with open(f"{self.filename}.csv", mode= 'a') as file: file.write(f"{user_id};{user_name}\n"); file.close()
        self.playersList[f'{user_id}']= user_name
        return
        