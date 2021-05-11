import os
import urllib.request
import json
import argparse
from datetime import datetime


'''
Roadmap:
Output to database (?)
Save all results data
Save/display results 'description'
Allow other search options (seller/developer)
'''

'''
Change Log
alpha 0.1 : Initial GitHub release
'''

'''
Notes
'''


def set_key_list(set_key_items=None):

    temp_key_list = []

    if set_key_items:
        try:
            with open(set_key_items, 'r') as key_f:
                while True:
                    key_line = (key_f.readline()).replace("\n", "")
                    if not key_line:
                        break
                    else:
                        temp_key_list.append(key_line)

            key_f.close()

        except Exception as key_e:
            print(f"error: {key_e}")

    else:  # default keys to parse from iTunes lookup results
        temp_key_list = ["trackCensoredName", "sellerUrl", "trackViewUrl", "trackName", "releaseDate", "sellerName",
                         "currentVersionReleaseDate", "artistName", "primaryGenreName", "bundleId", "trackId"]

    return temp_key_list


def get_itunes_data(search_term, search_type):

    response_json_data = None

    try:
        if search_type == "bundleID":
            search_string = f"http://itunes.apple.com/lookup?bundleId={search_term}"
        elif search_type == "iTunesID":
            search_string = f"http://itunes.apple.com/lookup?id={search_term}"
        else:
            search_string = f"https://itunes.apple.com/search?term={search_term.replace(' ', '+')}" \
                            f"&media=software&limit=10"
        with urllib.request.urlopen(search_string) as response:
            response_data = response.read()
            response_json_data = json.loads(response_data)
    except Exception as get_e:
        print(f"\nERROR: {get_e}")

    return response_json_data


def parse_itunes_results(json_data):

    if "resultCount" in json_data:
        if json_data["resultCount"] == 0:
            report_results(f"No results found at itunes.apple.com for {search_item}")
        else:
            for results_item in json_data["results"]:
                parse_results_data(results_item)


def parse_results_data(results_item_data):

    for k, v in results_item_data.items():
        if k in parse_key_list:
            report_results(f"{k}: {v}")


def report_results(report_data):

    print(f"{report_data}")
    if report_file:
        report_file.write(f"\n{report_data}")


if __name__ == '__main__':

    script = "itunes_lookup"
    friendly_name = "iTunes Lookup"
    version = "alpha0.1 (2021)"
    email = "pug4n6@gmail.com"
    github = "https://github.com/pug4n6"

    key_list_input = None
    search_list_input = None
    time_format_filename = "%Y%m%d_%H%M%S"
    start_time = datetime.now()
    output_filename = f"{script}_output_{start_time.strftime(time_format_filename)}.txt"

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=f"{friendly_name} {version}\n{github} | {email}"
                    f"\n\nDESCRIPTION: Queries data from itunes.apple.com for bundleIDs, iTunesIDs, "
                    f"and search terms (top 10 results)"
                    f"\nAccepts -i as a single item, examples: com.apple.tv, 1174078549 (iTunesID), \"apple tv\" "
                    f"\n-- Also accepts -i as an input file with one entry per line"
                    f"\n-- Search Term queries displays the first 10 results "
                    f"and only specific keys to help identify relevant content"
                    f"\nAccepts -k as a find containing keys/tags to parse from iTunes query (one key per line) "
                    f"\n-- Omit -k to uses the default key list"
                    f"\nAccepts -s or --save to save the results to a text file")
    parser.add_argument("-k", dest="keys_input", required=False, action="store",
                        help="File containing list of keys to parse (one key per line)")
    parser.add_argument("-i", dest="search_input", required=True, action="store",
                        help="Single search criteria or file containing a list (one per line)")
    parser.add_argument("-s", "--save", dest="output_results", action="store_true", required=False, default=False,
                        help=f"Save lookup results to a text file")

    args = parser.parse_args()

    if args.keys_input:
        key_list_input = args.keys_input

    input_data = args.search_input

    if args.output_results:
        report_file = open(output_filename, "w+")
        report_file.write(f"{friendly_name} {version} results\n")
    else:
        report_file = None

    if key_list_input:
        if os.path.exists(key_list_input):
            key_list = set_key_list(key_list_input)
        else:
            print(f"Key list file {key_list_input} could not be found. Will proceed with default list.")
            key_list = set_key_list()
    else:
        key_list = set_key_list()

    search_list = []

    if os.path.exists(input_data):
        try:
            with open(input_data, 'r') as f:
                while True:
                    line = (f.readline()).replace("\n", "")
                    if not line:
                        break
                    else:
                        search_list.append(line)
            f.close()

        except Exception as e:
            print(f"error: {e}")

    else:
        search_list = [input_data]

    for search_item in search_list:

        if "." in search_item:
            input_type = "bundleID"
            parse_key_list = key_list
        elif search_item.isdigit():
            input_type = "iTunesID"
            parse_key_list = key_list
        else:
            input_type = "Search Term"
            parse_key_list = ["trackName", "sellerName", "trackViewUrl", "bundleId", ]

        report_results(f"\nResults for search criteria '{search_item}' identified as a {input_type}:")

        itunes_search_results = get_itunes_data(search_item, input_type)
        parse_itunes_results(itunes_search_results)

    if report_file:
        report_file.close()
