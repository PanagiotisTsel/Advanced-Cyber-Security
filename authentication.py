import hashlib
import uuid
import jwt
import datetime

SECRET_KEY = "FtDPpnqJHm"

class Authentication:
    def __init__(self, database):
        self.db = database

    def register(self, username, password, email, phone):
        hashed_password = self.hash_password(password)
        success, message = self.db.register_user(username, hashed_password, email, phone)
        return success, message

    def login(self, username, password):
        user_info = self.db.get_user_info(username)
        if user_info is None:
            return False, "User not found", None

        db_id, db_username, db_password, db_email, db_phone = user_info

        if self.verify_password(password, db_password):
            token = self.generate_token(username)
            return True, "Login successful", token
        else:
            return False, "Incorrect password", None

    def hash_password(self, password):
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
        return hashed_password

    def verify_password(self, provided_password, stored_password):
        password, salt = stored_password.split(':')
        return password == hashlib.sha256(salt.encode() + provided_password.encode()).hexdigest()

    def generate_token(self, username):
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        token = jwt.encode({'username': username, 'exp': expiration_time}, SECRET_KEY, algorithm='HS256')
        return token

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return True, payload['username']
        except jwt.ExpiredSignatureError:
            return False, "Token expired"
        except jwt.InvalidTokenError:
            return False, "Invalid token"
