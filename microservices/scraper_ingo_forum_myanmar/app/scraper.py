from bs4 import BeautifulSoup
from requests import get
from scraper_ingo_forum_myanmar.app.org import create_org_ingo_forum_myanmar
from scraper_ingo_forum_myanmar.app.models.organization import Org

url = "http://www.ingoforummyanmar.org/en/members"


def get_page_data():
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

        ngo_list.append(
            create_org_ingo_forum_myanmar(
                name, address, phone, email, org_url
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

    return create_org_ingo_forum_myanmar(name, address, phone, email, org_url).to_json()


if __name__ == "__main__":
    get_page_data()
