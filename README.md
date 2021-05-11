# iTunes_lookup
A Python script to querie data from itunes.apple.com for bundleIDs, iTunesIDs, and search terms (top 10 results)

An improvement on the previous bundleID_lookup, this one can query for multiple types of information to help identify and gather details about an application.

Accepts -i as a single item, examples: com.apple.tv, 1174078549 (iTunesID), "apple tv"
-- Also accepts -i as an input file with one entry per line
-- Search Term queries displays the first 10 results and only specific keys to help identify relevant content
Accepts -k as a find containing keys/tags to parse from iTunes query (one key per line)
-- Omit -k to uses the default key list
Accepts -s or --save to save the results to a text file
