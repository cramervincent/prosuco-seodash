from dependencies.dependencies import *
router = APIRouter()


@router.post('/backlinks/scan')
def get_backlink_data(data: LinkData):
    import time, requests, json
    if not data:
        raise HTTPException(
            status_code=404)
    
    for linkdata in data:
        try:
            page = requests.get(linkdata.website)
            if page.status_code == 200:
                if linkdata.link in page.text:
                    linkdata.status = 'found'
                else:
                    linkdata.status = 'notfound'
            else:
                linkdata.status = page.status_code
        except:
            linkdata['status'] = 'null'
            

    time.sleep(2)
    return json.loads(data)


# @router.post('/backlink')
# def add_backlink_data(data: backlinkData, db: Session = Depends(get_db)):
#     backlink_model = models.backlink()
#     backlink_model.title = data.title
#     backlink_model.author =data.author
#     backlink_model.rating =data.rating
#     backlink_model.description = data.description

#     db.add(backlink_model)
#     db.commit()
#     return {'data':backlink_model}

# @router.put('/backlink/{backlink_id}')
# def edit_backlink_data(backlink_id:int, data:backlinkData, db: Session = Depends(get_db)):
#     backlink_model =  db.query(models.backlink).filter(models.backlink.id == backlink_id).first()
#     if backlink_model == None:
#         raise HTTPException(status_code=404, detail='Id not found.')
#     else:
#         backlink_model.title = data.title
#         backlink_model.author =data.author
#         backlink_model.rating =data.rating
#         backlink_model.description = data.description

#         db.add(backlink_model)
#         db.commit()
#         return {'data':backlink_model}

# @router.delete('/backlink/{backlink_id}')
# def delete_backlink_data(backlink_id:int, data:backlinkData, db: Session = Depends(get_db)):
#     backlink_model =  db.query(models.backlink).filter(models.backlink.id == backlink_id).first()
#     if backlink_model == None:
#         raise HTTPException(status_code=404, detail='Id not found.')
#     else:
#         db.query(models.backlink).filter(models.backlink.id == backlink_id).delete()
#         db.commit()
#         return {'data':'Entry deleted.'}
