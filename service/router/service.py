from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schema import ServiceSchema,ServiceTitleData
from typing import List
from ..auth import get_current_user
router= APIRouter(
    prefix="/service",
    tags=["Service"])

@router.get("/",status_code=status.HTTP_200_OK, response_model=List[ServiceTitleData] )
def all_service(db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    data= db.query(models.Service).all()
    return data


#single data by ID
@router.get("/{id}",status_code=status.HTTP_200_OK)  
def get_service(id: int,response: Response, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    data= db.query(models.Service).filter(models.Service.id == id).first()
    #error status code 
    if not data:    
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": "Service not found"}     
    return {"data": data}


# single data by brand name
@router.get("/by-brand/{brand}")
def get_service_by_brand(brand: str, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    data = (
        db.query(models.Service)
        .filter( models.Service.more_data.op("->>")("brand") == brand)
        .all()
    )
    return {"data": data}

#insert data in database
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_service(post: bool,body: ServiceSchema,userid:int,db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    if post:
        new_service = models.Service(title=body.title, description=body.description, productimage=body.productimage, isapprove=body.isapprove, more_data=body.more_data, user_id=userid)
        db.add(new_service)
        db.commit()
        db.refresh(new_service)
        return {"data": new_service}
    return {"data": "Service not created"}
    


#delete data

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_service(id: int,response: Response, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    data= db.query(models.Service).filter(models.Service.id == id).first()
    if not data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": "Service not found"}
    db.delete(data)
    db.commit()    
    return {"data": "Service deleted","satut":"success"}

#update data all data
@router.put("/updateall/{id}",status_code=status.HTTP_200_OK)
def update(id,body: ServiceSchema, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    data= db.query(models.Service).filter(models.Service.id == id).update(dict(body))
    db.commit()
    return {"data": "Service updated","satut":"success"}
        
#update data single data
# @router.put("/service/{id}/isapprove",status_code=status.HTTP_200_OK)
# def update_single_data(id,response: Response,isapprove: bool ,db: Session = Depends(get_db)):
#     data= db.query(models.Service).filter(models.Service.id == id).first()
#     if not data:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"data": "Service not found"}
#     data.isapprove = isapprove  
#     db.commit()
#     return {"data": "Service updated","satut":"success"}

# ///////////////////////////or ///////////////////////                

@router.put("/{id}",status_code=status.HTTP_200_OK)
def update(id, isapprove: bool, db: Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    data= db.query(models.Service).filter(models.Service.id == id)
    if not data.first():
       raise HTTPException(status_code=404, detail="Service not found")
    data.update({"isapprove": isapprove})
    db.commit()
    return {"data": "Service updated","satut":"success"}
