import os
def get_path():
    a = os.getcwd()
    b = a.split('/')[:3]
    result = '/'.join(b)
    return result+'/'
a = get_path() +'sdadadasd/dsada/dasdsad'
print(a)