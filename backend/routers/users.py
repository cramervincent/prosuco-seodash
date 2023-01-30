from dependencies.dependencies import *
router = APIRouter()





@router.get('/users')
def get_all_users(db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)):

    user_result = db.query(models.users).filter(models.users.client_id == user['client_id']).all()

    if user_result == None:
        raise HTTPException(
            status_code=404,
            detail='No users'
        )

    
    return {'data': [{x} for x in user_result]}


@router.get('/users/{user_id}')
def get_one_users(user_id: int, db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)):

    user_result = db.query(models.users).filter(
        models.users.id == user_id).filter(models.users.client_id == user['client_id']).first()

    if user_result == None:
        raise HTTPException(
            status_code=404,
            detail='User not found.'
        )
    
    
    

    return {'data': user_result}

@router.post('/users/register')
def register_new_user(data:RegisterData, db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)):
    user_results = db.query(models.users).filter(models.users.email == data.email).first()
    
    if user_results:
        raise HTTPException(
            status_code=400,
            detail='Email is allready registered.'
        )

    admin_check(user)

    new_user = models.users()
    
    new_user.firstname =  data.firstname
    new_user.lastname = data.lastname
    new_user.email = data.email
    new_user.password = auth_handler.get_password_hash(data.password)
    new_user.birthday =  data.birthday
    new_user.photo =  data.photo
    new_user.is_admin = data.is_admin
    new_user.is_super_admin = False
    new_user.client_id = user['id']

    db.add(new_user)
    db.commit()
      
    return 


@router.patch('/users/{user_id}')
def edit_a_user(data:RegisterData, db: Session = Depends(get_db), user_id=int, user=Depends(auth_handler.auth_wrapper)):
    user_results = db.query(models.users).filter(models.users.id == user_id and models.users.client_id == user['client_id']).first()
    
    if not user_results:
        raise HTTPException(
            status_code=404,
        )
    if not user['is_admin'] and not user['is_super_admin'] and not user['id'] == user_id:
        raise HTTPException(
            status_code=401
        )

    

    new_user = db.get(models.users, user_id)
    
    new_user.firstname =  data.firstname
    new_user.lastname = data.lastname
    new_user.email = data.email
    new_user.password = auth_handler.get_password_hash(data.password)
    new_user.birthday =  data.birthday
    new_user.photo =  data.photo
    new_user.is_admin = data.is_admin
    

    db.add(new_user)
    db.commit()
      
    return    


@router.delete('/users/{user_id}')
def delete_a_users(user_id: int, db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)):

    user_result = db.query(models.users).filter(
        models.users.id == user_id).filter(models.users.id == user_id and models.users.client_id == user['client_id']).first()

    if user_result == None:
        raise HTTPException(
            status_code=404
        )
    if not user['is_admin'] and not user['is_super_admin']:
        raise HTTPException(
            status_code=401
        )
    
    db.query(models.users).filter(models.users.id == user_id).delete()
    
    db.commit()
    

    return {'data': user_result}
