class Arduino():
    def __init__(self, name):
        self.name = name

    def connect(self):
        print("Connect operation")

    def read_analog(self, pin):
        print("Reading from analog pin {}".format(pin))
        #return value

    def write_analog(self, pin, value):
        print("Writing to analog pin {} value {}".format(pin, value))

