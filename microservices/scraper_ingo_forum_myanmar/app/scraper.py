from bs4 import BeautifulSoup
from requests import get

from app.models.organization import Org

url = "http://www.imngoforummyanmar.org/en/members"


def get_page_data():
    print("here")
    target_url = get(url)
    page_data = BeautifulSoup(target_url.content, "html.parser")

    ngo_list = []

    tags = page_data.find_all("div", attrs={"class": ["member-info"]})
    for tag in tags:
        name = tag.find("div", attrs={"class": ["member-title"]})
        address = tag.find("div", attrs={"class": ["member-address"]})
        phone = tag.find("div", attrs={"class": ["member-phone"]})
        email = tag.find("div", attrs={"class": ["member-email"]})
        org_url = tag.find("div", attrs={"class": ["web-link"]})

        # get text from fields
        name = name.find("a").text if name is not None else None
        address = address.text if address is not None else None
        phone = phone.text if phone is not None else None
        email = email.find("a").text if email is not None else None

        # org_url tag has a nested element
        if org_url is not None:
            org_url = org_url.find("a").text if org_url.find("a") is not None else None

        ngo_list.append(
            Org(
                name=name, address=address, phone=phone, email=email, url=org_url
            ).to_json()
        )
    return ngo_list


def get_one_ngo():
    target_url = get(url)
    page_data = BeautifulSoup(target_url.content, "html.parser")

    tag = page_data.find_all("div", attrs={"class": ["member-info"]})[0]
    #     for tag in tags:
    name = tag.find("div", attrs={"class": ["member-title"]})
    address = tag.find("div", attrs={"class": ["member-address"]})
    phone = tag.find("div", attrs={"class": ["member-phone"]})
    email = tag.find("div", attrs={"class": ["member-email"]})
    org_url = tag.find("div", attrs={"class": ["web-link"]})

    # get text from fields
    name = name.find("a").text if name is not None else None
    address = address.text if address is not None else None
    phone = phone.text if phone is not None else None
    email = email.find("a").text if email is not None else None

    # org_url tag has a nested element
    if org_url is not None:
        org_url = org_url.find("a").text if org_url.find("a") is not None else None

    return Org(
        name=name, phone=phone, email=email, address=address, url=org_url
    ).to_json()


if __name__ == "__main__":
    get_page_data()
