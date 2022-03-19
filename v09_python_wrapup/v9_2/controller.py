class Controller():
    """test."""
    
    def __init__(self):
        self._observers = []
    
    def register(self, observer):
        self._observers.append(observer)
        
    def notify(self, **data):
        for observer in self._observers:
            #print(observer)
            observer.notify(self, **data)
            
