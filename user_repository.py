class UserRepository:
    def __init__(self):
        self.users = {}
    
    def username_exists(self, username):
        return username in self.users
    
    def add_user(self, user):
        self.users[user.username] = user
        
    def get_user(self, username):
        if username in self.users:
            return self.users[username]
        return None
            
        
