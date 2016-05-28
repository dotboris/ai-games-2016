Works with python2 and python3.

Install deps:

    pip install -r requirements.txt

Run with:

    python client.py <apiKey> <[training|competition]> [gameId]

Examples:

    python client.py mySecretKey competition myGameId
    python client.py mySecretKey training 


Gotchas:
- `x` represents `ROWS`, `y` represents `COLUMNS`. Yes, it's counter-intuitive.
- Be careful with types when comparing! E.g. don't assume that all IDs are ints.
  IDs that come directly from the JSON are ints, while IDs in `mines_locs` are
  strings. Doing a quick sanity check with debug logs may save you a lot of
  debugging time.
