from fastapi import APIRouter
from dependencies.dependencies import *
from models import models
from models import *


from schemas.backlinks import *

router = APIRouter()


@router.get("/backlinks/")
async def get_all_backlinks(db:Session = Depends(get_db)):
    result = db.query(models.Backlinks).all()
    return result

@router.get("/backlinks/{bId}")
async def get_all_backlinks(bId, db:Session = Depends(get_db)):
    result = db.query(models.Backlinks).filter(models.Backlinks.id == bId).first()
    if not result:
        raise HTTPException(status_code=404)
    return result

@router.post("/backlinks/")
async def create_new_backlink(data:backlink_schema, db:Session =  Depends(get_db)):
    new_backlink = models.Backlinks(
        link = "String",
        site = "String",
        status = "String",
        pa = "String",
        da = "String",
        last_check = "String"
    )
    db.add(new_backlink)
    db.commit()
    db.refresh(new_backlink)

    return {'status':'ok'}

@router.delete("/backlinks/{bId}")
async def delete_a_backlink(bId, db:Session =  Depends(get_db)):
    result = db.query(models.Backlinks).filter(models.Backlinks.id == bId).first()
    if not result:
        raise HTTPException(status_code=404)
    db.delete(result)
    db.commit()
    return {'ok':True}

# @router.put("/backlinks/{bId}")
# async def edit_a_backlink():
#     return ["All backlinks"]    