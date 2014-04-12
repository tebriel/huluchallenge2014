#!/usr/bin/env python

"""
Written by Chris Moultrie <chris@moultrie.org> @tebriel
Available on Github at https://github.com/tebriel/huluchallenge2014
This was a lot of fun, thanks.

Usage: python hulu.py <filename>
"""

from collections import defaultdict
from json import dumps
from sys import argv

def output(dictionary):
    """Provided Output Function"""
    print(dumps(dictionary, sort_keys=True))

def map_sources(source_list, index, sources_map):
    """Create a hashmap of individual show names to correspond with what lines
    they occur on in the file in the format:
    {"ShowTitle":[0,3,77]}
    Originally tried having sources_map[source] as a set, but .add was 3x slower
      than append and then casting to a set later
    """
    for source in source_list.split(','):
        sources_map[source].append(index)
    return sources_map

def process_file(file_name):
    """Split the file up into sources and blacklists"""
    # Array of all our lines for retrieval later
    sources = []
    # Array of all our blacklists
    blacklists = []
    # Indicate that we're done processing the sources
    sources_done = False
    # Way to map the sources to their indexes
    sources_map = defaultdict(list)
    # What index we're currently on
    current_index = 0

    with open(file_name) as groups:
        for line in groups:
            line = line.rstrip('\n')
            if line == "####":
                sources_done = True
                continue

            if sources_done:
                blacklists.append(line)
            else:
                sources.append(line)
                map_sources(line, current_index, sources_map)
                current_index += 1

    return (sources, blacklists, sources_map)

def process_blacklist_items(sources, blacklists, sources_map):
    """Figure out which lines have our required blacklist items and print them
    out"""
    for blacklist in blacklists:
        blacklist_sources = blacklist.split(',')
        to_intersect = []
        for source in blacklist_sources:
            # Verify there's something there because defaultdict will just put
            # 0 there for us when we try to access something that doesn't exist
            if len(sources_map[source]) > 0:
                to_intersect.append(set(sources_map[source]))

        # Build up how many times we see those items
        counts = defaultdict(int)
        # Just find the indices that they all have in common
        for intersect in set.intersection(*to_intersect):
            for source in sources[intersect].split(','):
                counts[source] += 1
        # We don't want to list out the blacklisted items, so kill those off
        for source in blacklist_sources:
            counts.pop(source, None)
        # Finally, output our results
        output(counts)


if __name__ == "__main__":
    process_results = process_file(argv[1])
    process_blacklist_items(*process_results)
