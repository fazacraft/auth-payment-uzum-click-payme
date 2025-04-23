from enum import Enum

class UzumResponse(Enum):
    Ok = 'OK'
    Failed = 'FAILED'
    Cancelled = 'CANCELLED'
    Created = 'CREATED'
    Confirmed = 'CONFIRMED'
    Reversed = 'REVERSED'

    def __str__(self):
        return self.value
