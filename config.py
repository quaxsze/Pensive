import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGODB_DB = 'pensive'
    MONGODB_HOST = 'mongodb+srv://m001-student:jUCAiM16o8VwyMBM@cluster0.sfsdf.mongodb.net/pensivessdd?retryWrites=true&w=majority'
