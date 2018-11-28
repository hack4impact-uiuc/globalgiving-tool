import json


class Org:
    """
    Serialized object for easy input and retrieval of relevant organization text data.
    Contains name, phone number, email address, physical address, contact information,
    and web url.
    """

    def __init__(
        self=None,
        name=None,
        phone=None,
        email=None,
        address=None,
        contact=None,
        registration=None,
        url=None,
        facebook=None,
        country=None,
        description=None,
    ):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.contact = contact
        self.registration = registration
        self.url = url
        self.facebook = facebook
        self.country = country
        self.description = description

    def to_json(self):
        org = {
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "contact": self.contact,
            "registration": self.registration,
            "url": self.url,
            "facebook": self.facebook,
            "country": self.country,
            "description": self.description,
        }
        return org

    def __str__(self):
        return json.dumps(self.to_json(), indent=4, separators=(",", ": "))
