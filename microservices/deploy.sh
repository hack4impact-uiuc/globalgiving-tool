#loops through all the folders and deploys everything (takes 1-2 min per scraper)
for d in */ ; do
    if [[ "$d" == "scraper"* ]];
    then
        DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
        cd "$DIR/$d"
        now && now alias
        cd "$DIR"
    fi
done