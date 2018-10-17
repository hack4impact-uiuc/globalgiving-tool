def create_org(line):
    """
    Attempts to parse a line of data into the Org class.
     Input:
        line: an array of strings that could possibly contain organization data.
        Lines are usually arranged as such [ 'name' , 'key:value' ], where key 
        would be a specific field (one of name, phone, email, etc.) and value 
        would be that specific piece of data for the field.
         Some lines do not correspond to this format and do not contain useful
        information.
     Returns:
        If the line contains valid organization data, then we return a serialized 
        Org object containing the data in the input line. Otherwise, we'll return 
        None.
    """
    valid_categories = ["name", "phone", "email", "address", "contact", "url"]
    org_data = {}

    for idx, info in enumerate(line):
        if idx == 0:
            name = info
            continue
        if ":" not in info:
            continue

        delim = info.split(":", 1)
        category = delim[0].lower()
        data = delim[1].strip()

        if category in valid_categories:
            org_data[category] = data

    phone = org_data["phone"] if "phone" in org_data.keys() else None
    email = org_data["email"] if "email" in org_data.keys() else None
    address = org_data["address"] if "address" in org_data.keys() else None
    contact = org_data["contact"] if "contact" in org_data.keys() else None
    url = org_data["url"] if "url" in org_data.keys() else None

    org = Org(name, phone, email, address, contact, url) if bool(org_data) else None
    if org is not None:
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
