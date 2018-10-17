from bs4 import BeautifulSoup


def create_org_ingo_forum_myanmar(name, address, phone, email, org_url):
    name = name.find("a").text if name is not None else None
    address = address.text if address is not None else None
    phone = phone.text if phone is not None else None
    email = email.find("a").text if email is not None else None

    # org_url tag has a nested element
    if org_url is not None:
        org_url = org_url.find("a").text if org_url.find("a") is not None else None
    org = Org(name, phone, email, address, None, org_url)
    print(org)
    return org


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
