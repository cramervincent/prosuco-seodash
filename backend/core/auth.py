import jwt
import json
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = '96E12CABC44E82AF9A9298B86B989'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user):

        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, hours=6),
            'iat': datetime.utcnow(),
            'sub': {
                'id': user.id,
                'is_super_admin':user.is_super_admin,
                'is_admin':user.is_admin,
                'client_id':user.client_id
            }
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail='JWT has expired'
            )

        except jwt.InvalidTokenError as e:
            print(e)
            raise HTTPException(
                status_code=401,
                detail='JWT is invalid'
            )

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
