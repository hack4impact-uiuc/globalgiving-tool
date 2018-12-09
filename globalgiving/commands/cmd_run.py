import click, requests
from globalgiving.db import list_from_db
from globalgiving.cli import pass_context, authenticate
import os 

@click.command("run", short_help="Subprocess")
@click.argument("n", required=False)
@click.option("-a", is_flag=True)
@pass_context
def cli(ctx, n, a):
    if a:
        print('globalgiving run a')
        os.popen('globalgiving run a')
    else:
        print("globalgiving run " + n)
        os.popen('globalgiving run ' + n)
    # subprocess.call(["sleep", "10"])

    # process = Pccccccjdfhhrhtfdjljdrvujuhdibkrnhiibvbcutlbi
    # open(['sleep', '3'], stdout=PIPE, stderr=PIPE)
    # stdout, stderr = process.communicate()
    # subprocess.call(["sleep", "10", "&&", "echo", "hi"])
    # subprocess.call(["ls", "-l"])
    # authenticate()
    # search = "Finding scraper {} from list of registered scrapers..."
    # ctx.log(search.format(n))
    # try:
    #     scrapers = list_from_db()
    #     route = list(filter(lambda scraper: scraper["name"] == str(n), scrapers))[0][
    #         "routes"
    #     ]["Test"]
    #     ctx.log("Scraper {} found!".format(n))
    # except StopIteration:
    #     ctx.log("Scraper {} not found.".format(n))
    #     return
    # contents = requests.get(route).text
    # print(contents)
