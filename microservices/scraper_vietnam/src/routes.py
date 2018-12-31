import api

@api.route("/url")
class ScraperVietnam(Resource):
    def get(self):
        return {"url": "https://www.viet.net/community/nonprofit/"}


@api.route("/data")
class ScraperVietnam(Resource):
    def get(self):
        orgs = get_page_data()
        return {"data": orgs}


@api.route("/test")
class ScraperVietnam(Resource):
    def get(self):
        orgs = get_test_data()
        return {"test": str(orgs[0])}
