import requests
from utils.config import USAJOBS_API_KEY


def fetch_usajobs(keyword, location="remote", results_per_page=5):

    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": "mayurijoshi1706@gmail.com",
        "Authorization-Key": USAJOBS_API_KEY
    }

    params = {
        "Keyword": keyword,
        "LocationName": location,
        "ResultsPerPage": results_per_page
    }

    url = "https://data.usajobs.gov/api/search"

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        return response.json().get(
            "SearchResult", {}
        ).get(
            "SearchResultItems", []
        )

    print("USAJobs API Error:", response.status_code)
    print(response.text)

    return []


if __name__ == "__main__":

    jobs = fetch_usajobs(
        "business analyst",
        location="New York",
        results_per_page=10
    )

    for job in jobs:
        title = job["MatchedObjectDescriptor"]["PositionTitle"]
        agency = job["MatchedObjectDescriptor"]["OrganizationName"]

        print(f"{title} at {agency}")