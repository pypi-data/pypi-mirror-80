from .ValidateStr import validate_size_string, validate_type_str
from .error import NoStrError 

def str_value(val, call_back = None):  
    try:
        if validate_size_string(val) and validate_type_str(val):
            return True 
        else:
            raise NoStrError()   
    except NoStrError as e:
        if call_back is not None:
            call_back()
        else:
            print(e)
            #return e    

def call_back_function():      #Funcion OPCIONAL
    print('Esto se ejecuta cuando se presenta un error') #OPCIONAL