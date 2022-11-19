from fastapi import FastAPI


__author__ = 'Ricardo'
__version__ = 0.1


app = FastAPI(
    title='Blog API',
    description='In this API we will be able to create publications and comment them',
    version=0.1
)


@app.on_event('startup')
def startup():
    print('ENCENDIDO')


@app.on_event('shutdown')
def shutdown():
    print('APAGADO')
