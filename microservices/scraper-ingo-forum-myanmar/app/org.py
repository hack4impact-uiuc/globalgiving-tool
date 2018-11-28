from bs4 import BeautifulSoup
from app.models.organization import Org


def create_org_ingo_forum_myanmar(name, address, phone, email, org_url):
    name = name.find("a").text if name is not None else None
    address = address.text if address is not None else None
    phone = phone.text if phone is not None else None
    email = email.find("a").text if email is not None else None

    # org_url tag has a nested element
    if org_url is not None:
        org_url = org_url.find("a").text if org_url.find("a") is not None else None
    org = Org(
        name=name,
        phone=phone,
        email=email,
        address=address,
        url=org_url,
        country="Myanmar",
    )
    print(org)
    return org
