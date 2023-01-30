from fastapi import APIRouter
from fastapi import Depends, HTTPException
from models import models
from db.database import engine, Sessionlocal
from sqlalchemy.orm import Session
from base_models.models import *
from core.auth import AuthHandler
from fastapi.middleware.cors import CORSMiddleware
import os



auth_handler = AuthHandler()


def get_db():
    try:
        db = Sessionlocal()
        yield db
    finally:
        db.close()


def admin_check(user):
    if not user['is_admin'] and not user['is_super_admin']:
        raise HTTPException(
            status_code=401
        )
def same_client_check(user, user_result):    
    if not user_result.client_id == user.client_id or not user.is_super_admin:
         raise HTTPException(
            status_code=403
        )

def init_super_admin():
    super_admin_email = os.getenv("SUPER_ADMIN_EMAIL")
    super_admin_password = auth_handler.get_password_hash(os.getenv("SUPER_ADMIN_PASSWORD"))
    
    
    