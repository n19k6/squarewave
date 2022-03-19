class OxSignal():
    """Generats OX signal."""
    
    # this class is used to generate the ox1 and ox2 signals. frequency is between 0.1 Hz and 10 Hz.
    # The signal is generated using a single state machine inside the PIO.
    
    def __init__(self, controller, sm_id, pin):
        print("init")
        controller.register(self)
        
    def notify(self, observable, **data):
        print("received the following data: ", data)
    

