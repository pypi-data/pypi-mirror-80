# candystore

![tests](https://github.com/tipresias/candystore/workflows/tests/badge.svg)

Factories for randomised AFL data sets, selling candy to your unit tests.

The shape and content of the data is based on what's returned by the R package `fitzRoy`, which gets most of its data from the sites [Footywire](https://www.footywire.com/) and [AFLTables](https://afltables.com/afl/afl_index.html). The column names are converted to `snake_case` for convenience.

Data is randomised as much as is reasonably possible, with the following exceptions intended to make the data realistic:

- Teams are all real, using the naming conventions of AFLTables.
- Venues are all real, using the naming conventions of AFLTables.
- Seasons can range from 1897 to the current year (inclusive).
- Matches take place from 15th March to 30th September (inclusive), starting no earlier than 12pm and no later than 8pm.
- There's one round per week, and it lasts from Wednesday to Tuesday (inclusive).
- Each team only plays once per round.

## Installation

```bash
pip3 install candystore
```

```python
from candystore import CandyStore

afl_data = CandyStore()
```

## Usage

All functions for generating data accept a `seasons` argument for defining which years to use.

- An integer indicates the number of seasons to build, but permits them to start in any valid year (all seasons will still be sequential).
- A tuple of two integers indicates the specific range of years for which to build seasons.

### Fixtures

```python

afl_data.fixtures()

[
    {
        'date': '1967-03-16 12:37:19',
        'season': 1967,
        'season_game': 1,
        'round': 1,
        'home_team': 'Melbourne',
        'away_team': 'Brisbane Lions',
        'venue': 'Sydney Showground'
    },
    ...
    {
        'date': '1967-09-26 18:06:32',
        'season': 1967,
        'season_game': 280,
        'round': 28,
        'home_team': 'University',
        'away_team': 'Brisbane Lions',
        'venue': 'Brunswick St'
    }
]
```

### Betting Odds

```python

afl_data.betting_odds()

[
    {
        'date': '1967-03-21 18:40:59',
        'season': 1967,
        'round': 'Round 1',
        'home_team': 'Sydney',
        'away_team': 'Fremantle',
        'venue': 'Wellington',
        'round_number': 1,
        'home_score': 26,
        'away_score': 89,
        'home_margin': -63,
        'away_margin': 63,
        'home_win_odds': 2.71,
        'away_win_odds': 1.13,
        'home_win_paid': 0.0,
        'away_win_paid': 1.13,
        'home_line_odds': 33,
        'away_line_odds': -33,
        'home_line_paid': 0.0,
        'away_line_paid': 1.92
    },
    ...
    {
        'date': '1967-09-24 18:43:35',
        'season': 1967,
        'round': 'Round 28',
        'home_team': 'Hawthorn',
        'away_team': 'Greater Western Sydney',
        'venue': 'Marvel Stadium',
        'round_number': 28,
        'home_score': 26,
        'away_score': 89,
        'home_margin': -63,
        'away_margin': 63,
        'home_win_odds': 2.71,
        'away_win_odds': 1.13,
        'home_win_paid': 0.0,
        'away_win_paid': 1.13,
        'home_line_odds': 33,
        'away_line_odds': -33,
        'home_line_paid': 0.0,
        'away_line_paid': 1.92
    }
]
```