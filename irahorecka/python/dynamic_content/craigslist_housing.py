"""
This module will gather almost every sf bay area housing posts and write to a json file
This module will then have options to:
    1. return all posts in json format
    2. return posts queried against json format
Get zip codes for alameda, contra costa, santa clara, san francisco, santa cruz, sonoma, and san mateo

NOTE: eventually, we want to transition data storage and fetching from a database
"""

import pycraigslist
