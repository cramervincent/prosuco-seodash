from dependencies.dependencies import *
router = APIRouter()



@router.post('/auth/login')
def local_login(data:LoginData, db: Session = Depends(get_db)):
    user = db.query(models.users).filter(models.users.email == data.username).first()
        
    if (user is None) or (not auth_handler.verify_password(data.password, user.password)):
        raise HTTPException(
            status_code=401,
            detail='Incorrect username and/or password'
        )
    
    token = auth_handler.encode_token(user)
    return {'data':{'token':token}}

@router.get('/auth/me')
def get_me(db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)):

    user_result = db.query(models.users).filter(
        models.users.id == user['id']).first()

    if user_result == [] or not user_result:
        raise HTTPException(
            status_code=418
        )

    return {'data':
            {   'client':user_result.client,
                'firstname': user_result.firstname,
                'lastname': user_result.lastname,
                'email': user_result.email,
                'birthday': user_result.birthday,
                'id': user_result.id
            }

            }