class NoStrError(Exception):

    def __init__(self):
        self.message = 'El valor no es válido dado que no es un string y/o su tamaño es > a 10 caractéres'
    
    def __str__(self):    #se sobreescribe el método __str__. 
        return self.message  #Solo se puede retornar un string.