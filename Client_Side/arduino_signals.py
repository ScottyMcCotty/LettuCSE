import time
def move_toolhead(coords):
    #TODO actually signal arduino
    print("Toolhead moving to " + str(coords))
    time.sleep(1)

def lower_toolhead():
    #TODO actually signal arduino
    print("Toolhead lowering")
    time.sleep(1)

def raise_toolhead():
    #TODO actually signal arduino
    print("Toolhead raising")
    time.sleep(1)

def release_plant():
    #TODO actually signal arduino
    print("Toolhead releasing")
    time.sleep(1)

def grab_plant():
    #TODO actually signal arduino
    print("Toolhead closing")
    time.sleep(1)
