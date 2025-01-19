# Copyright Gustav Ebbers
import datetime

from pydantic import BaseModel


class ContactProperties(BaseModel):
    lastPurchaseDate: datetime.datetime | None = None
    birthday: datetime.datetime | None = None
    country: str | None = None
    lastName: str | None = None
    city: str | None = None
    initials: str | None = None
    postalCode: str | None = None
    houseNumber: str | None = None
    organisation: str | None = None
    profileFields: list
    infix: str | None = None
    profileField1: str | None = None
    taal: str | None = None
    firstPurchaseDate: datetime.datetime | None = None
    freeField1: int | None = None
    firstName: str
    customerType: str | None = None
    street: str | None = None
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
