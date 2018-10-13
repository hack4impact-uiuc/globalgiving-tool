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

    name = phone = email = address = contact = url = ""
    parseable = False

    for idx, info in enumerate(line):
        if idx == 0:
            name = info
            continue

        if ":" not in info:
            continue

        delim = info.split(":", 1)
        category = delim[0].lower()
        data = delim[1].strip()

        if category == "email":
            email = data
        if category == "phone":
            parseable = True
            phone = data
        if category == "contact":
            parseable = True
            contact = data
        if category == "url":
            parseable = True
            url = data
        if category == "address":
            parseable = True
            address = data

    if parseable:
        org = Org(name, phone, email, address, contact, url)
        print(org)
        return org
    return None


class Org:
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
