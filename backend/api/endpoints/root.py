from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def root():

    return {'message': 'This is an example message', 'data': 0}

@router.get('/test')
def test():
    time.sleep(10)
    return {'task':'slept for 10 seconds'}

@router.get('/s')
def test():
    return {'task':'no sleep'}