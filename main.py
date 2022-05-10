import jwt
import requests
import uvicorn

from fastapi import FastAPI, Request, Form, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse

from starlette import status

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/', tags=['main'])
async def index(req: Request, bearer: str = Cookie(None)):
    posts = requests.get('http://127.0.0.1:8000/api/post').json()

    if bearer is not None:
        payload = jwt.decode(bearer, 'secret', algorithms=['HS256'])
        name = payload.get('nickname')
    else:
        name = 'Guest'

    return templates.TemplateResponse("main.html", {"request": req,
                                                    "authorized": False if bearer is None else True,
                                                    "nickname": name,
                                                    "posts": posts})


@app.get('/login', tags=['main'])
async def login(req: Request):
    return templates.TemplateResponse("login.html", {"request": req,
                                                     "authorized": False})


@app.get('/logout', tags=['main'])
async def login(req: Request):
    respones = RedirectResponse('/login')
    respones.delete_cookie('bearer')
    return respones


@app.get('/me', tags=['main'])
async def me(req: Request, bearer: str = Cookie(None)):
    print(bearer)
    if bearer is not None:
        payload = jwt.decode(bearer, 'secret', algorithms=['HS256'])
        name = payload.get('nickname')
        uid = payload.get('id')
        user = requests.get(f'http://127.0.0.1:8000/api/user?uid={uid}').json()
        print(user)
    else:
        user = dict()
        user["posts"] = ""
        name = 'Guest'

    return templates.TemplateResponse("profile.html", {"request": req,
                                                       "authorized": False if bearer is None else True,
                                                       "nickname": name,
                                                       "posts": user['posts']})


@app.get('/reg', tags=['main'])
async def reg(req: Request):
    return templates.TemplateResponse('reg.html', {"request": req})


@app.get('/create')
async def create(req: Request):
    return templates.TemplateResponse('createpost.html', {"request": req})


@app.post('/createpost')
async def createpost(title: str = Form(...), content: str = Form(...), bearer: str = Cookie(...)):
    q = requests.post('http://127.0.0.1:8000/api/post',
                      json={'title': title,
                            'content': content},
                      headers={'Authorization': f'Bearer {bearer}'})

    if q.status_code == 200:
        return RedirectResponse('/me', status_code=status.HTTP_303_SEE_OTHER)

    response = RedirectResponse("/create", status_code=status.HTTP_303_SEE_OTHER)
    return response


@app.post('/create')
async def r(email: str = Form(...), username: str = Form(...), password: str = Form(...)):
    q = requests.post('http://127.0.0.1:8000/api/user', json={'nickname': username,
                                                              'email': email,
                                                              'password': password})

    if q.status_code == 200:
        return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)

    response = RedirectResponse("/reg", status_code=status.HTTP_303_SEE_OTHER)
    return response


@app.post('/r')
async def r(email: str = Form(...), username: str = Form(...), password: str = Form(...)):
    q = requests.post('http://127.0.0.1:8000/api/user', json={'nickname': username,
                                                              'email': email,
                                                              'password': password})

    if q.status_code == 200:
        return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)

    response = RedirectResponse("/reg", status_code=status.HTTP_303_SEE_OTHER)
    return response


@app.post('/auth', tags=['main'])
async def auth(req: Request, username: str = Form(...), password: str = Form(...)):
    q = requests.post('http://127.0.0.1:8000/api/user/auth', data={'username': username,
                                                                   'password': password})

    if q.status_code == 401:
        return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)

    q = q.json()
    response = RedirectResponse("/me", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key='bearer', value=q['token'])
    return response


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8001)
