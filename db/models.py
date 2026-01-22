# from dataclasses import dataclass
# from datetime import date

# @dataclass
# class LabBooking:
#     name: str
#     phone: str
#     email: str
#     test_name: str
#     date: date
#     time: str


from dataclasses import dataclass

@dataclass
class LabBooking:
    name: str
    phone: str
    email: str
    test_name: str
    date: str
    time: str

