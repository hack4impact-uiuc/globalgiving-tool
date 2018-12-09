from globalgiving.crawler.resources.country_codes import country_codes
from globalgiving.crawler.resources.address_keywords import address_keywords
import phonenumbers


def count_phone_numbers(country_name, visible_text):
    """
    DESCRIPTION: counts number of phone numbers that occur on NGO website
    INPUT: visible_text --- all the visible text of NGO website homepage and subpages
    OUTPUT: integer number of phone numbers found in visible text
    """
    if country_name not in country_codes:
        code = "None"
    else:
        code = country_codes[country_name]
        print(code)
    num_phone_numbers = 0
    for match in phonenumbers.PhoneNumberMatcher(visible_text, code):
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


def count_ngo_related_words(visible_text):
    """
    DESCRIPTION: counts number of instances of 'ngo'
    INPUT: visible_text --- all the visible text of NGO website homepage and subpages
    OUTPUT: integer number of instances of 'ngo'
    """
    ngo_related_words_count = 0
    visible_text = visible_text.lower()
    ngo_related_words_count += visible_text.count("ngo")
    ngo_related_words_count += visible_text.count("directory")
    ngo_related_words_count += visible_text.count("nonprofit")
    return ngo_related_words_count


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
    composite_score = rank_info["num_phone_numbers"] + rank_info["num_addresses"]
    rank_info["composite_score"] = composite_score
    # url = rank_info["url"]
    # url_rank[url] = rank_info
    # return composite_score
    return rank_info["composite_score"]
