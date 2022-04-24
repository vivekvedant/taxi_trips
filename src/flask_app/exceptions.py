class SameLocation(Exception):
    def __init__(self, message="Pickup and dropoff location is same"):
        self.message = message
        super().__init__(self.message)


class SameTime(Exception):
    def __init__(self, message="Pickup and dropoff time is same"):
        self.message = message
        super().__init__(self.message)



class PassengerCount(Exception):
    def __init__(self, message="Passenger count is invalid"):
        self.message = message
        super().__init__(self.message)
