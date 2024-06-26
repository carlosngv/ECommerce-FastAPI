from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from config import get_db
from models import BusinessTable
from schemas import BusinessCreate, BusinessUpdate

business_router = APIRouter(prefix='/business', tags=['business'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth')

@business_router.post('/')
async def create_business(business: BusinessCreate, db: AsyncSession = Depends(get_db)):
    new_business = await BusinessTable.create(db, **business.__dict__)
    if not new_business:
        return JSONResponse(status_code=400, content={'msg': 'Business was not created'})
    return JSONResponse(status_code=201, content={'msg': 'Business successfully created'})

@business_router.put('/{id}')
async def update_business(id: str, business: BusinessUpdate, db: AsyncSession = Depends(get_db)):
    update_status = await BusinessTable.update(db, id, **business.__dict__)
    if not update_status:
        return JSONResponse(status_code=400, content={'msg': 'Bussiness was not updated'})
    return JSONResponse(status_code=201, content={'msg': 'Business successfully updated'})

@business_router.get('/{id}')
async def get_business_by_id(id: str, db: AsyncSession = Depends(get_db)):
    db_business = await BusinessTable.get(id, db)
    if not db_business:
        return JSONResponse(status_code=400, content={'msg': 'Bussiness was not found'})
    return JSONResponse(status_code=200, content={'business': jsonable_encoder(db_business)})

@business_router.get('/')
async def get_all_business(db: AsyncSession = Depends(get_db)):
    businesses = await BusinessTable.get_all(db)
    if not businesses:
        return JSONResponse(status_code=400, content={'msg': 'Contact your administrator'})
    return JSONResponse(status_code=200, content={'businesses': jsonable_encoder(businesses)})
