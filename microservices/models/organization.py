class Org:
    """
    Serialized object for easy input and retrieval of relevant organization text data.
    Contains name, phone number, email address, physical address, contact information,
    and web url.
    """

    def __init__(self, name, phone, email, address, contact, url):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.contact = contact
        self.url = url

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (
            self.name,
            self.phone,
            self.email,
            self.address,
            self.contact,
            self.url,
        )
