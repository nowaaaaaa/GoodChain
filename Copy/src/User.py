class User:
    def __init__(self, user_list):
        self.username = user_list[0]
        self.password = user_list[1]
        self.private_key = user_list[2]
        self.public_key = user_list[3]
    
    def get_private_key(self):
        from cryptography.hazmat.primitives import serialization
        return serialization.load_pem_private_key(self.private_key, password=self.password.encode('utf-8'))
    
    def get_protected_user(self):
        return User([self.username, self.password, self.private_key, self.public_key])