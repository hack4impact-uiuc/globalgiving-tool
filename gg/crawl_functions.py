from googlesearch import search
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urlparse
import requests
import phonenumbers

# dictionary that maps directory url to rank_info for one website
url_rank = {}
"""
{
    URL: rank_info dict
}
"""
# dictionary template that stores all the ranking information for one directory
rank_info = {}
"""
{
    'num_links': (number of links),
    'num_subpages': (number of subpages)
    'num_addresses': (number of addresses)
    'num_phone_numbers': (number of phone numbers)
    'num_word_ngo' : (number of times word "ngo" appears on website)
    'num_word_directory': (number of times word "directory appears on website)
    'composite_score': (composite score for website)
    'page_or_dir': (boolean to indicate whether we think URL is ngo page or ngo directory)
}
"""
static country_name = ""

address_keywords = [
    "street",
    "st.",
    "st",
    "blvd",
    "blvd.",
    "ln",
    "ln.",
    "lane",
    "road",
    "rd",
    "rd.",
    "circle",
    "cir",
    "cir.",
    "highway",
    "hwy",
    "hwy.",
    "court",
    "ct",
    "ct.",
    "square",
    "sq",
    "sq.",
    "terrace",
    "ter.",
    "ter",
    "drive",
    "dr",
    "dr.",
    "way",
    "wy",
    "wy.",
    "crossing",
    "cross",
    "cross.",
    "xing",
    "xing.",
    "heights",
    "hts",
    "hts.",
    "landing",
    "landng",
    "landng.",
    "loop",
    "loop.",
    "parkway",
    "pky",
    "pky.",
    "pass",
    "pass.",
    "plaza",
    "plaza.",
    "promenade",
    "prom",
    "prom.",
    "building",
    "parade",
    " hous",
]

country_code = {'Afghanistan': 'AF',
 'Albania': 'AL',
 'Algeria': 'DZ',
 'American Samoa': 'AS',
 'Andorra': 'AD',
 'Angola': 'AO',
 'Anguilla': 'AI',
 'Antarctica': 'AQ',
 'Antigua and Barbuda': 'AG',
 'Argentina': 'AR',
 'Armenia': 'AM',
 'Aruba': 'AW',
 'Australia': 'AU',
 'Austria': 'AT',
 'Azerbaijan': 'AZ',
 'Bahamas': 'BS',
 'Bahrain': 'BH',
 'Bangladesh': 'BD',
 'Barbados': 'BB',
 'Belarus': 'BY',
 'Belgium': 'BE',
 'Belize': 'BZ',
 'Benin': 'BJ',
 'Bermuda': 'BM',
 'Bhutan': 'BT',
 'Bolivia, Plurinational State of': 'BO',
 'Bonaire, Sint Eustatius and Saba': 'BQ',
 'Bosnia and Herzegovina': 'BA',
 'Botswana': 'BW',
 'Bouvet Island': 'BV',
 'Brazil': 'BR',
 'British Indian Ocean Territory': 'IO',
 'Brunei Darussalam': 'BN',
 'Bulgaria': 'BG',
 'Burkina Faso': 'BF',
 'Burundi': 'BI',
 'Cambodia': 'KH',
 'Cameroon': 'CM',
 'Canada': 'CA',
 'Cape Verde': 'CV',
 'Cayman Islands': 'KY',
 'Central African Republic': 'CF',
 'Chad': 'TD',
 'Chile': 'CL',
 'China': 'CN',
 'Christmas Island': 'CX',
 'Cocos (Keeling) Islands': 'CC',
 'Colombia': 'CO',
 'Comoros': 'KM',
 'Congo': 'CG',
 'Congo, the Democratic Republic of the': 'CD',
 'Cook Islands': 'CK',
 'Costa Rica': 'CR',
 'Country name': 'Code',
 'Croatia': 'HR',
 'Cuba': 'CU',
 'Curaçao': 'CW',
 'Cyprus': 'CY',
 'Czech Republic': 'CZ',
 "Côte d'Ivoire": 'CI',
 'Denmark': 'DK',
 'Djibouti': 'DJ',
 'Dominica': 'DM',
 'Dominican Republic': 'DO',
 'Ecuador': 'EC',
 'Egypt': 'EG',
 'El Salvador': 'SV',
 'Equatorial Guinea': 'GQ',
 'Eritrea': 'ER',
 'Estonia': 'EE',
 'Ethiopia': 'ET',
 'Falkland Islands (Malvinas)': 'FK',
 'Faroe Islands': 'FO',
 'Fiji': 'FJ',
 'Finland': 'FI',
 'France': 'FR',
 'French Guiana': 'GF',
 'French Polynesia': 'PF',
 'French Southern Territories': 'TF',
 'Gabon': 'GA',
 'Gambia': 'GM',
 'Georgia': 'GE',
 'Germany': 'DE',
 'Ghana': 'GH',
 'Gibraltar': 'GI',
 'Greece': 'GR',
 'Greenland': 'GL',
 'Grenada': 'GD',
 'Guadeloupe': 'GP',
 'Guam': 'GU',
 'Guatemala': 'GT',
 'Guernsey': 'GG',
 'Guinea': 'GN',
 'Guinea-Bissau': 'GW',
 'Guyana': 'GY',
 'Haiti': 'HT',
 'Heard Island and McDonald Islands': 'HM',
 'Holy See (Vatican City State)': 'VA',
 'Honduras': 'HN',
 'Hong Kong': 'HK',
 'Hungary': 'HU',
 'ISO 3166-2:GB': '(.uk)',
 'Iceland': 'IS',
 'India': 'IN',
 'Indonesia': 'ID',
 'Iran, Islamic Republic of': 'IR',
 'Iraq': 'IQ',
 'Ireland': 'IE',
 'Isle of Man': 'IM',
 'Israel': 'IL',
 'Italy': 'IT',
 'Jamaica': 'JM',
 'Japan': 'JP',
 'Jersey': 'JE',
 'Jordan': 'JO',
 'Kazakhstan': 'KZ',
 'Kenya': 'KE',
 'Kiribati': 'KI',
 "Korea, Democratic People's Republic of": 'KP',
 'Korea, Republic of': 'KR',
 'Kuwait': 'KW',
 'Kyrgyzstan': 'KG',
 "Lao People's Democratic Republic": 'LA',
 'Latvia': 'LV',
 'Lebanon': 'LB',
 'Lesotho': 'LS',
 'Liberia': 'LR',
 'Libya': 'LY',
 'Liechtenstein': 'LI',
 'Lithuania': 'LT',
 'Luxembourg': 'LU',
 'Macao': 'MO',
 'Macedonia, the former Yugoslav Republic of': 'MK',
 'Madagascar': 'MG',
 'Malawi': 'MW',
 'Malaysia': 'MY',
 'Maldives': 'MV',
 'Mali': 'ML',
 'Malta': 'MT',
 'Marshall Islands': 'MH',
 'Martinique': 'MQ',
 'Mauritania': 'MR',
 'Mauritius': 'MU',
 'Mayotte': 'YT',
 'Mexico': 'MX',
 'Micronesia, Federated States of': 'FM',
 'Moldova, Republic of': 'MD',
 'Monaco': 'MC',
 'Mongolia': 'MN',
 'Montenegro': 'ME',
 'Montserrat': 'MS',
 'Morocco': 'MA',
 'Mozambique': 'MZ',
 'Myanmar': 'MM',
 'Namibia': 'NA',
 'Nauru': 'NR',
 'Nepal': 'NP',
 'Netherlands': 'NL',
 'New Caledonia': 'NC',
 'New Zealand': 'NZ',
 'Nicaragua': 'NI',
 'Niger': 'NE',
 'Nigeria': 'NG',
 'Niue': 'NU',
 'Norfolk Island': 'NF',
 'Northern Mariana Islands': 'MP',
 'Norway': 'NO',
 'Oman': 'OM',
 'Pakistan': 'PK',
 'Palau': 'PW',
 'Palestine, State of': 'PS',
 'Panama': 'PA',
 'Papua New Guinea': 'PG',
 'Paraguay': 'PY',
 'Peru': 'PE',
 'Philippines': 'PH',
 'Pitcairn': 'PN',
 'Poland': 'PL',
 'Portugal': 'PT',
 'Puerto Rico': 'PR',
 'Qatar': 'QA',
 'Romania': 'RO',
 'Russian Federation': 'RU',
 'Rwanda': 'RW',
 'Réunion': 'RE',
 'Saint Barthélemy': 'BL',
 'Saint Helena, Ascension and Tristan da Cunha': 'SH',
 'Saint Kitts and Nevis': 'KN',
 'Saint Lucia': 'LC',
 'Saint Martin (French part)': 'MF',
 'Saint Pierre and Miquelon': 'PM',
 'Saint Vincent and the Grenadines': 'VC',
 'Samoa': 'WS',
 'San Marino': 'SM',
 'Sao Tome and Principe': 'ST',
 'Saudi Arabia': 'SA',
 'Senegal': 'SN',
 'Serbia': 'RS',
 'Seychelles': 'SC',
 'Sierra Leone': 'SL',
 'Singapore': 'SG',
 'Sint Maarten (Dutch part)': 'SX',
 'Slovakia': 'SK',
 'Slovenia': 'SI',
 'Solomon Islands': 'SB',
 'Somalia': 'SO',
 'South Africa': 'ZA',
 'South Georgia and the South Sandwich Islands': 'GS',
 'South Sudan': 'SS',
 'Spain': 'ES',
 'Sri Lanka': 'LK',
 'Sudan': 'SD',
 'Suriname': 'SR',
 'Svalbard and Jan Mayen': 'SJ',
 'Swaziland': 'SZ',
 'Sweden': 'SE',
 'Switzerland': 'CH',
 'Syrian Arab Republic': 'SY',
 'Taiwan, Province of China': 'TW',
 'Tajikistan': 'TJ',
 'Tanzania, United Republic of': 'TZ',
 'Thailand': 'TH',
 'Timor-Leste': 'TL',
 'Togo': 'TG',
 'Tokelau': 'TK',
 'Tonga': 'TO',
 'Trinidad and Tobago': 'TT',
 'Tunisia': 'TN',
 'Turkey': 'TR',
 'Turkmenistan': 'TM',
 'Turks and Caicos Islands': 'TC',
 'Tuvalu': 'TV',
 'Uganda': 'UG',
 'Ukraine': 'UA',
 'United Arab Emirates': 'AE',
 'United Kingdom': 'GB',
 'United States': 'US',
 'United States Minor Outlying Islands': 'UM',
 'Uruguay': 'UY',
 'Uzbekistan': 'UZ',
 'Vanuatu': 'VU',
 'Venezuela, Bolivarian Republic of': 'VE',
 'Viet Nam': 'VN',
 'Virgin Islands, British': 'VG',
 'Virgin Islands, U.S.': 'VI',
 'Wallis and Futuna': 'WF',
 'Western Sahara': 'EH',
 'Yemen': 'YE',
 'Zambia': 'ZM',
 'Zimbabwe': 'ZW',
 'Åland Islands': 'AX'
 '':'None'
 }
# -----------------------------------------------------------------------------------------------
# -----------------------------------RANKING FUNCTIONS-------------------------------------------
# -----------------------------------------------------------------------------------------------


def rank_all(country,ngo_type):
    """
    DESCRIPTION: goes through all the URLs in url_rank dictionary and ranks them
    INPUT: none
    OUTPUT: none
    BEHAVIOR: expect url_rank to now contain dictionaries of rank_info as values. These
              dictionaries store information pertinent to ranking as well as composite rank score
    """
    country_name = country
    for url, _ in url_rank.items():
        rank_page(url)


def rank_page(url):
    """
    DESCRIPTION: ranks the NGO website specified by url
    INPUT: url --- absolute URL to NGO website
    OUTPUT: none
    BEHAVIOR: expect url_rank to now contain dictionary of rank_info as value. This
              dictionary stores information pertinent to ranking as well as composite rank score
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    all_visible_text = get_all_visible_text(url)

    # get all subpages
    subpages = find_subpages(url)

    # get all visible text from all subpages
    for subpage in subpages:
        all_visible_text += get_all_visible_text(subpage)
        # add a space to make sure text doesnt get jumbled together
        all_visible_text += " "

    # perform webpage analysis on all_visible_text HERE, update rank_info

    # print(all_visible_text)

    # get composite_score
    # composite_score = get_composite_score(url_rank[url])
    # store composite_score
    # url_rank[url]['composite_score'] = composite_score


def count_phone_numbers(visible_text):
    """
    DESCRIPTION: counts number of phone numbers that occur on NGO website
    INPUT: visible_text --- all the visible text of NGO website homepage and subpages
    OUTPUT: integer number of phone numbers found in visible text
    """
    code = country_code[country_name]
    for match in phonenumbers.PhoneNumberMatcher(text, code):
       num_phone_numbers += 1

    return num_phone_numbers


def count_addresses(visible_text):
    """
    DESCRIPTION: counts number of addresses that occur on NGO website
    INPUT: visible_text --- all the visible text of NGO website homepage and subpages
    OUTPUT: integer number of addresses found in visible text
    """
    visible_text = visible_text.lower()
    num_addresses = 0

    for type_ in address_keywords:
        num_addresses += visible_text.count(type_)

    return num_addresses


def get_composite_score(rank_info):
    """
    DESCRIPTION: ranks the NGO website specified by url
    INPUT: url --- URL to NGO website
    OUTPUT: none
    BEHAVIOR: expect url_rank to now contain dictionary of rank_info as value. This
              dictionary stores information pertinent to ranking as well as composite rank score
    """
    # heuristic can be altered here:
    # composite_score = rank_info['num_phone_numbers']

    # return composite_score
    pass


# -----------------------------------------------------------------------------------------------
# -----------------------------------RANKING FUNCTIONS-------------------------------------------
# -----------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------
# ------------------------------FUNCTIONS TO GET VISIBLE TEXT-------------s----------------------
# -----------------------------------------------------------------------------------------------


def get_all_visible_text(url):
    """
    DESCRIPTION: gets all the visible text of homepage and subpages one-level deep for NGO website
    INPUT: url --- absolute URL to NGO website
    OUTPUT: string of all visible text on NGO website
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    visible_text = " ".join(t.strip() for t in visible_texts)

    # print(visible_text)

    return visible_text


def tag_visible(element):
    """
    DESCRIPTION: determines if html tag is visible or not
    INPUT: element --- html tag
    OUTPUT: boolean indicating whether tag is visible or not
    """
    if element.parent.name in [
        "style",
        "script",
        "head",
        "title",
        "meta",
        "[document]",
    ]:
        return False
    if isinstance(element, Comment):
        return False
    return True


def find_subpages(url):
    """
    DESCRIPTION: scrapes website homepage for all subpages
    INPUT: url --- absolute URL denoting ngo website homepage
    OUTPUT: list of all subpage URLs
    """

    # get the domain url from homepage url
    parsed_uri = urlparse(url)
    home_url = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_uri)
    print("STRIPPED URL:")
    print(home_url)

    subpages = []
    valid_subpages = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # get all URL links on homepage
    anchors = soup.findAll("a", href=True)
    links = [anchor["href"] for anchor in anchors]
    """
    Note that homepage url could be e.g. "https://care.ca/directory" due to
    google search not taking us to true homepage
    Need to remove "/directory" for true homepage url

    Three types of links that can be found
    1) relative links for subpages (e.g. /about-us/mission)
    2) absolute links for subpages (e.g. https://care.ca/about-us/mission)
    3) irrevelant external absolute link (e.g. https://mcafee.com/blahblahblah)
    """
    home_url_length = len(home_url)
    # consider case 1) and 2) for subpage links, discard case 3)
    for link in links:
        # discard case 3)
        if link[:1] != "/" and link[:home_url_length] != home_url:
            print("LINK IS NOT SUBPAGE: " + link)
            continue
        # case 2)
        if link[:home_url_length] == home_url:
            subpages.append(link)
        # case 1)
        if link[:1] == "/":
            subpages.append(url + link)
            subpages.append(home_url + link)

    # remove duplicates in valid_subpages
    subpages = list(set(subpages))

    # remove faulty subpage links
    for link in subpages:
        # try to access subpage link
        try:
            r = requests.get(str(link))
            print(r.status_code)
            if r.status_code != 404:
                valid_subpages.append(link)
        except:
            print("exception caught!")
            continue

    print("VALID SUBPAGES: " + str(len(valid_subpages)))
    print(valid_subpages)

    # output all subpage links to text file for easier examination
    f = open("subpages.txt", "w")
    for valid_subpage in valid_subpages:
        f.write(valid_subpage + "\n")
    f.close()

    return valid_subpages


# -----------------------------------------------------------------------------------------------
# ------------------------------FUNCTIONS TO GET VISIBLE TEXT-------------s----------------------
# -----------------------------------------------------------------------------------------------
