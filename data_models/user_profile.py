# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class UserProfile:
    def __init__(self, name: str = None, age: int = 0, date: str = None):
        self.name = name
        self.age = age
        self.date = date


class BookingProfile:
    def __init__(self, bavail: str = None, bvenue: str = None, fdate: int = 0, tdate: str = None):
        self.bavail = bavail
        self.bvenue = bvenue
        self.fdate = fdate
        self.tdate = tdate
