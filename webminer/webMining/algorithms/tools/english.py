class DomainDictionary:
    domainDictionary=str()
    def __init__(self):
        self.domainDictionary=open("dictionary.txt",'r')
        
    def validate(self,word=''):
        return self.domainDictionary.read()
        #return word in self.domainDictionary.read()

obj=DomainDictionary()
print obj.validate()
