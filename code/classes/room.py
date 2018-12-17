class Room(object):
    """
    Representation of a room in Schedule
    """

    def __init__(self, name, room_id, capacity):
        self.name = name
        self.room_id = room_id
        self.capacity = capacity

    def __str__(self):
        return self.name
