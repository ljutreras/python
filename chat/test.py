import requests

db = ['188651194', '192408156', '123456789']



def dni_from_db(dni):

    res = ['yes' if dni == e else 'no' for e in db]
    print(res)
    
dni_from_db('188651193')
