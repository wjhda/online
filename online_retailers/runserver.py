import uvicorn

if __name__ == '__main__':
    uvicorn.run(app='online_retailers.asgi:application', host='0.0.0.0', port=9000, reload=False, workers=1)