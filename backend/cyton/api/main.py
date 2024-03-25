
def main():
    import uvicorn
    uvicorn.run("cyton.api.app:app", host="localhost", port=9999, reload=True)
