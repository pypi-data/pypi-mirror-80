class Lnwyod:
    def __init__(self): 
        self.name = 'Attaporn'
        self.lastname = 'Ninsuwan'
        self.nickname = 'Yod'

    def WhoIAm(self):
        '''
        This is function of LnwYod class for show the name 
        '''
        print('My name is     : {}'.format(self.name))
        print('My lastname is : {}'.format(self.lastname))
        print('My nickname is : {}'.format(self.nickname))

    @property    
    def email(self):
        '''
        This function will show an email.
        '''
        return 'My email is   : {}.{}@gmail.com'.format(self.name.lower(),self.lastname.lower())

    def thainame(self):
        print('อรรถพร นิลสุวรรณ')
        return('อรรถพร นิลสุวรรณ')
    
    def __str__(self):
        '''
        This function when you call self
        '''
        return 'This is a lnwYod class'
    
#สามารถรันได้เมื่อเป็นของตัวเอง    
if __name__ == '__main__':   

    mylnw = Lnwyod()

    print(help(mylnw.WhoIAm))

    print(mylnw.name)
    print(mylnw.lastname)
    print(mylnw.nickname)

    mylnw.WhoIAm()

    print(mylnw.email)

    print(mylnw)

    mylnw.thainame()

    print('-----------------')

    myson = Lnwyod()
    myson.name = 'Ratchaneekorn'
    myson.lastname = 'Promkaew'
    myson.nickname = 'Gam'
    print(myson.name)
    print(myson.lastname)
    print(myson.nickname)
    myson.WhoIAm()

        
        
