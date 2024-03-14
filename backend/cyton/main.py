import uvicorn

if __name__ == '__main__':
    uvicorn.run("cyton.api.app:app", host="localhost", port=9999, reload=True)
