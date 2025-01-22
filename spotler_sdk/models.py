# Copyright Gustav Ebbers
import datetime
from enum import Enum

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
    firstName: str | None = None
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


class Order(BaseModel):
    externalId: str
    externalContactId: str
    date: datetime.datetime
    value: str
    externalProductIds: list[str]


class OrderRequest(BaseModel):
    update: bool = True
    order: Order


class StockEnum(str, Enum):
    LIMITED = "LIMITED"
    GOOD = "GOOD"
    UNKNOWN = "UNKNOWN"


class ProductSpecification(BaseModel):
    description: str
    value: str
    rank: str | None = None


class Product(BaseModel):
    externalId: str
    name: str
    description: str | None = None
    link: str | None = None
    price: str
    oldPrice: str | None = None
    imageUrl: str
    category: str | None = None
    gtin: str | None = None
    sku: str | None = None
    brand: str | None = None
    ratingImageUrl: str | None = None
    reviewLink: str | None = None
    creationDate: datetime.datetime | None = None
    changeDate: datetime.datetime | None = None
    addToCartLink: str | None = None
    imageLargeUrl: str
    ratingValue: str | None = None
    language: str | None = None
    stock: StockEnum = StockEnum.UNKNOWN
    deleted: bool = False
    visible: bool = True
    specifications: list[ProductSpecification] | None = None


class ProductRequest(BaseModel):
    update: bool = True
    product: Product
