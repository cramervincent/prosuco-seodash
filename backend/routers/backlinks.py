from dependencies.dependencies import *
router = APIRouter()


@router.post('/backlinks/scan')
async def get_backlink_data(data: list, db: Session = Depends(get_db)):
    import time, requests, json
    if not data:
        raise HTTPException(
            status_code=404)
    
    selectedLinks = []
    for linkId in data:
        dbq = db.query(models.backlinks).filter(models.backlinks.id == linkId).first()
        # print(dbq.website)
        selectedLinks.append(
            {
                "link":dbq.link,
                "website":dbq.website,
                "status":dbq.status
            }
        )
        
    print(selectedLinks)
        
        
    
    for linkdata in selectedLinks:
        try:
            page = requests.get(linkdata['website'])
            if page.status_code == 200:
                if linkdata['link'] in page.text:
                   linkdata['status'] = 'found'
                else:
                    linkdata['status'] = 'notfound'
            else:
                linkdata['status'] = page.status_code
        except Exception as e:
            print(e)
            linkdata['status'] = 'null'
    time.sleep(2)
    
    return selectedLinks


@router.post('/backlink')
def add_backlink_data(data: backlinkData, db: Session = Depends(get_db)):
    backlink_model = models.backlinks()
    backlink_model.link= data.link
    backlink_model.website= data.website
    backlink_model.da= "String"
    backlink_model.pa = "String"
    backlink_model.status = "String"
    backlink_model.last_check = "String"

    db.add(backlink_model)
    db.commit()
    return {'data':backlink_model}


@router.get('/backlinks')
def get_all_backlinks(db: Session = Depends(get_db)):

    backlink_result = db.query(models.backlinks).all()
    returnvalue = []
    for x in backlink_result:
        returnvalue.append(x)
    return returnvalue


@router.delete('/backlinks/{backlink_id}')
def delete_a_backlinks(backlink_id: int, db: Session = Depends(get_db)):

    backlink_result = db.query(models.backlinks).filter(models.backlinks.id == backlink_id).first()

    if backlink_result == None:
        raise HTTPException(
            status_code=404
        )
    
    db.query(models.backlinks).filter(models.backlinks.id == backlink_id).delete()

    db.commit()

    return {'data': backlink_result}
