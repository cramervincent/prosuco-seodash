from dependencies.dependencies import *
router = APIRouter()

@router.post('/clients/register')
def register_new_client(data:ClientRegisterData, db: Session = Depends(get_db)):
    client_results = db.query(models.clients).filter(models.clients.email == data.email).first()
    
    if client_results:
        raise HTTPException(
            status_code=400,
            detail='Email is already registered.'
        )
    new_client = models.clients()
    new_client.name = data.name
    new_client.email = data.email
    
    db.add(new_client)
    db.commit()

   
    client_results = db.query(models.clients).filter(models.clients.email == data.email).first()
   

    new_user = models.users()
    new_user.firstname =  data.name
    new_user.lastname = 'Admin'
    new_user.email = data.email
    new_user.password = auth_handler.get_password_hash(data.password)
    new_user.is_admin = True
    new_user.client_id = client_results.id
        
    db.add(new_user)
    db.commit()
      
    return

@router.patch('/clients/{client_id}')
def edit_a_client(data:ClientPatchData,client_id:int, db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)):

    if not user['is_super_admin']:
        raise HTTPException(status_code=401)

    client_results = db.query(models.clients).filter(models.clients.id == client_id).first()
    
    if not client_results:
        raise HTTPException(
            status_code=404,
        )
    
    
    edit_client =db.get(models.clients, client_id)
    edit_client.name = data.name
    edit_client.email = data.email
    
    
    db.add(edit_client)
    db.commit()

   
    client_results = db.query(models.clients).filter(models.clients.email == data.email).first()
   

    new_user = models.users()
    new_user.firstname =  data.name
    new_user.lastname = 'Admin'
    new_user.email = data.email
    new_user.password = auth_handler.get_password_hash(data.password)
    new_user.is_admin = True
    new_user.client_id = client_results.id
        
    db.add(new_user)
    db.commit()
      
    return

@router.get('/clients')
def get_all_clients(db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)):
    if not user['is_super_admin']:
        raise HTTPException(status_code=401)

    return db.query(models.clients).all()


@router.get('/clients/{client_id}')
def get_a_client(client_id:int, db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)):
    if not user['is_super_admin']:
        raise HTTPException(status_code=401)
    return db.query(models.clients).filter(models.clients.id == client_id).first()

@router.delete('/clients/{client_id}')
def edit_a_client(client_id:int, db: Session = Depends(get_db), user=Depends(auth_handler.auth_wrapper)):
    if not user['is_super_admin']:
        raise HTTPException(status_code=401)
    selected_client = db.query(models.clients).filter(models.clients.id == client_id).first()
    
    if not selected_client:
        raise HTTPException(
            status_code=404
        )
    
    db.query(models.clients).filter(models.clients.id == client_id).delete()
    db.commit()

    return