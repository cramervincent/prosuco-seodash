from dependencies.dependencies import *
router = APIRouter()

@router.get('/dummy')
def get_dummy_data(db: Session = Depends(get_db)):
    return {'data':db.query(models.dummy).all()}

@router.get('/dummy/{dummy_id}')
def get_single_dummy_data(dummy_id:int, db: Session = Depends(get_db)):
    
    dummy_model = db.query(models.dummy).filter(models.dummy.id == dummy_id).first()
    if dummy_model == None:
        raise HTTPException(status_code=404, detail='Id not found.')
    else:
        return {'data':dummy_model}

@router.post('/dummy')
def add_dummy_data(data: DummyData, db: Session = Depends(get_db)):
    dummy_model = models.dummy()
    dummy_model.title = data.title
    dummy_model.author =data.author
    dummy_model.rating =data.rating
    dummy_model.description = data.description

    db.add(dummy_model)
    db.commit()
    return {'data':dummy_model}

@router.put('/dummy/{dummy_id}')
def edit_dummy_data(dummy_id:int, data:DummyData, db: Session = Depends(get_db)):
    dummy_model =  db.query(models.dummy).filter(models.dummy.id == dummy_id).first()
    if dummy_model == None:
        raise HTTPException(status_code=404, detail='Id not found.')
    else:
        dummy_model.title = data.title
        dummy_model.author =data.author
        dummy_model.rating =data.rating
        dummy_model.description = data.description

        db.add(dummy_model)
        db.commit()
        return {'data':dummy_model}

@router.delete('/dummy/{dummy_id}')
def delete_dummy_data(dummy_id:int, data:DummyData, db: Session = Depends(get_db)):
    dummy_model =  db.query(models.dummy).filter(models.dummy.id == dummy_id).first()
    if dummy_model == None:
        raise HTTPException(status_code=404, detail='Id not found.')
    else:
        db.query(models.dummy).filter(models.dummy.id == dummy_id).delete()
        db.commit()
        return {'data':'Entry deleted.'}