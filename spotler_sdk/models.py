# Copyright Gustav Ebbers
import datetime

from pydantic import BaseModel


class ContactProperties(BaseModel):
    lastPurchaseDate: datetime.datetime | None = None
    birthday: datetime.datetime | None = None
    country: str
    lastName: str
    city: str
    initials: str
    postalCode: str | None = None
    houseNumber: str | None = None
    organisation: str
    profileFields: list
    infix: str
    profileField1: str | None = None
    taal: str
    firstPurchaseDate: datetime.datetime | None = None
    freeField1: int | None = None
    firstName: str
    customerType: str | None = None
    street: str
    permissions: list
    email: str


class Contact(BaseModel):
    externalId: str
    created: datetime.datetime
    encryptedId: str
    testGroup: bool
    lastChanged: datetime.datetime
    temporary: bool
    properties: ContactProperties
    channels: list
