"""For generating fake fixture data."""

from typing import Tuple, Union, List, Optional
from datetime import date, datetime, timedelta
import itertools
import math
from functools import partial

from faker import Faker
from mypy_extensions import TypedDict
import numpy as np
import pandas as pd


SeasonRange = Tuple[int, int]

FixtureData = TypedDict(
    "FixtureData",
    {
        "date": str,
        "season": int,
        "season_game": int,
        "round": int,
        "home_team": str,
        "away_team": str,
        "venue": str,
    },
)

BettingData = TypedDict(
    "BettingData",
    {
        "date": datetime,
        "season": int,
        "round_number": int,
        "round": str,
        "home_team": str,
        "away_team": str,
        "home_score": int,
        "away_score": int,
        "home_margin": int,
        "away_margin": int,
        "home_win_odds": float,
        "away_win_odds": float,
        "home_win_paid": float,
        "away_win_paid": float,
        "home_line_odds": float,
        "away_line_odds": float,
        "home_line_paid": float,
        "away_line_paid": float,
        "venue": str,
    },
)

MatchData = TypedDict(
    "MatchData",
    {
        "date": str,
        "game": int,
        "season": int,
        "round": str,
        "round_number": int,
        "round_type": str,
        "home_team": str,
        "home_goals": int,
        "home_behinds": int,
        "home_points": int,
        "away_team": str,
        "away_goals": int,
        "away_behinds": int,
        "away_points": int,
        "margin": int,
        "venue": str,
    },
)

PlayerData = TypedDict(
    "PlayerData",
    {
        "season": int,
        "round": int,
        "date": str,
        "local_start_time": str,
        "venue": str,
        "attendance": int,
        "home_team": str,
        "hq1g": int,
        "hq1b": int,
        "hq2g": int,
        "hq2b": int,
        "hq3g": int,
        "hq3b": int,
        "hq4g": int,
        "hq4b": int,
        "home_score": int,
        "away_team": str,
        "aw1g": int,
        "aw1b": int,
        "aw2g": int,
        "aw2b": int,
        "aw3g": int,
        "aw3b": int,
        "aw4g": int,
        "aw4b": int,
        "away_score": int,
        "first_name": str,
        "surname": str,
        "id": int,
        "jumper_no": int,
        "playing_for": str,
        "kicks": int,
        "marks": int,
        "handballs": int,
        "goals": int,
        "behinds": int,
        "hit_outs": int,
        "tackles": int,
        "rebounds": int,
        "inside_50s": int,
        "clearances": int,
        "clangers": int,
        "frees_for": int,
        "frees_against": int,
        "brownlow_votes": int,
        "contested_possessions": int,
        "uncontested_possessions": int,
        "contested_marks": int,
        "marks_inside_50": int,
        "one_percenters": int,
        "bounces": int,
        "goal_assists": int,
        "time_on_ground": int,
        "substitute": int,
        "umpire_1": str,
        "umpire_2": str,
        "umpire_3": str,
        "umpire_4": str,
        "group_id": int,
    },
)

BaseMatchData = TypedDict(
    "BaseMatchData",
    {
        "date": datetime,
        "season": int,
        "round": int,
        "home_team": str,
        "away_team": str,
        "venue": str,
    },
)
DateRange = TypedDict(
    "DateRange", {"datetime_start": datetime, "datetime_end": datetime}
)


FAKE = Faker()

FIRST_AFL_SEASON = 1897
MAR = 3
FIFTEENTH = 15
SEP = 9
THIRTIETH = 30
WEDNESDAY = 2
# About as early as matches ever start
MIN_MATCH_HOUR = 12
# About as late as matches ever start
MAX_MATCH_HOUR = 20

WEEK_IN_DAYS = 7
DAY_IN_HOURS = 24

# Reasonable ranges are two standard deviations plus/minus from the means
# for all recorded AFL matches
REASONABLE_SCORE_RANGE = (23, 148)
REASONABLE_MARGIN_RANGE = (0, 89)
REASONABLE_GOAL_RANGE = (2, 23)
REASONABLE_BEHIND_RANGE = (3, 22)
# Uses minimum attendance, because standard deviation was too large
REASONABLE_ATTENDANCE_RANGE = (1071, 61120)

# The following are ranges for per-player, per-match stats since 1965
REASONABLE_KICK_RANGE = (0, 21)
REASONABLE_MARK_RANGE = (0, 10)
REASONABLE_HANDBALL_RANGE = (0, 14)
REASONABLE_PLAYER_GOAL_RANGE = (0, 4)
REASONABLE_PLAYER_BEHIND_RANGE = (0, 3)
REASONABLE_HIT_OUT_RANGE = (0, 12)
REASONABLE_TACKLE_RANGE = (0, 6)
REASONABLE_REBOUND_RANGE = (0, 5)
REASONABLE_INSIDE_50_RANGE = (0, 6)
REASONABLE_CLEARANCE_RANGE = (0, 5)
REASONABLE_CLANGER_RANGE = (0, 5)
REASONABLE_FREE_FOR_RANGE = (0, 5)
REASONABLE_FREE_AGAINST_RANGE = (0, 5)
REASONABLE_CONTESTED_POSSESSION_RANGE = (0, 11)
REASONABLE_UNCONTESTED_POSSESSION_RANGE = (0, 17)
REASONABLE_CONTESTED_MARK_RANGE = (0, 3)
REASONABLE_MARK_INSIDE_50_RANGE = (0, 3)
REASONABLE_ONE_PERCENTER_RANGE = (0, 5)
REASONABLE_BOUNCE_RANGE = (0, 3)
REASONABLE_GOAL_ASSIST_RANGE = (0, 2)
REASONABLE_TIME_ON_GROUND_RANGE = (0, 116)

SUBSTITUTE_RANGE = (0, 3)
BROWNLOW_VOTES_RANGE = (0, 4)

# Roughly the payout when win odds are even
BASELINE_BET_PAYOUT = 1.92
# Hand-wavy math to get vaguely realistic win odds
WIN_ODDS_MULTIPLIER = 0.8

N_PLAYERS_PER_TEAM = 22

NON_BRISBANE_TEAMS = [
    "Richmond",
    "Carlton",
    "Melbourne",
    "Greater Western Sydney",
    "Essendon",
    "Sydney",
    "Collingwood",
    "North Melbourne",
    "Western Bulldogs",
    "Fremantle",
    "Port Adelaide",
    "St Kilda",
    "Hawthorn",
    "Adelaide",
    "Gold Coast",
    "Geelong",
    "West Coast",
    "Fitzroy",
    "University",
]
BRISBANE_TEAMS = [
    "Brisbane Bears",
    "Brisbane Lions",
]

VENUES = [
    # AFL Tables venues
    "Football Park",
    "S.C.G.",
    "Windy Hill",
    "Subiaco",
    "Moorabbin Oval",
    "M.C.G.",
    "Kardinia Park",
    "Victoria Park",
    "Waverley Park",
    "Princes Park",
    "Western Oval",
    "W.A.C.A.",
    "Carrara",
    "Gabba",
    "Docklands",
    "York Park",
    "Manuka Oval",
    "Sydney Showground",
    "Adelaide Oval",
    "Bellerive Oval",
    "Marrara Oval",
    "Traeger Park",
    "Perth Stadium",
    "Stadium Australia",
    "Wellington",
    "Lake Oval",
    "East Melbourne",
    "Corio Oval",
    "Junction Oval",
    "Brunswick St",
    "Punt Rd",
    "Glenferrie Oval",
    "Arden St",
    "Olympic Park",
    "Yarraville Oval",
    "Toorak Park",
    "Euroa",
    "Coburg Oval",
    "Brisbane Exhibition",
    "North Hobart",
    "Bruce Stadium",
    "Yallourn",
    "Cazaly's Stadium",
    "Eureka Stadium",
    "Blacktown",
    "Jiangwan Stadium",
    "Albury",
    "Riverway Stadium",
    # Footywire venues
    "AAMI Stadium",
    "ANZ Stadium",
    "UTAS Stadium",
    "Blacktown International",
    "Blundstone Arena",
    "Domain Stadium",
    "Etihad Stadium",
    "GMHBA Stadium",
    "MCG",
    "Mars Stadium",
    "Metricon Stadium",
    "Optus Stadium",
    "SCG",
    "Spotless Stadium",
    "TIO Stadium",
    "Westpac Stadium",
    "Marvel Stadium",
    "Canberra Oval",
    # Correct spelling is 'Traeger', but footywire.com is spelling it 'Traegar' in its
    # fixtures
    "TIO Traegar Park",
]


class CandyStore:
    """Data factory for different data sets related to AFL matches."""

    def __init__(self, seasons: Union[int, SeasonRange] = 1):
        """
        Instantiate the data generator.

        Params:
        -------
        seasons: The seasons to generate data for.
            If an integer, will start from a random year for which AFL data exists
            and increment for the given number of years.
            If a tuple of integers, will generate fixtures for the given range of years
            (same rules as Python's `range`).
        """
        self.seasons = seasons
        self._base_matches = pd.DataFrame(self._generate_seasons())

    def fixtures(
        self, to_dict: Optional[str] = "records"
    ) -> Union[pd.DataFrame, List[FixtureData]]:
        """
        Generate fixture data for the given seasons.

        Returns:
        --------
        List of fixture dictionaries that replicate fitzRoy's `get_fixture` function,
            but with Pythonic conventions (e.g. snake_case keys)
        """
        fixtures_data_frame = self._base_matches.pipe(self._convert_to_fixtures)

        return (
            fixtures_data_frame
            if to_dict is None
            else fixtures_data_frame.to_dict(to_dict)
        )

    def betting_odds(
        self, to_dict: Optional[str] = "records"
    ) -> Union[pd.DataFrame, List[BettingData]]:
        """
        Generate betting odds data for the given seasons.

        Returns:
        --------
        List of betting odds dictionaries that replicate fitzRoy's
            `get_footywire_betting_odds` function, but with Pythonic conventions
            (e.g. snake_case keys)
        """
        betting_odds_data_frame = self._base_matches.pipe(self._convert_to_betting_odds)

        return (
            betting_odds_data_frame
            if to_dict is None
            else betting_odds_data_frame.to_dict(to_dict)
        )

    def match_results(
        self, to_dict: Optional[str] = "records"
    ) -> Union[pd.DataFrame, List[MatchData]]:
        """
        Generate match results data data for the given seasons.

        Returns:
        --------
        Match data that replicate fitzRoy's `get_match_results` function,
            but with Pythonic conventions (e.g. snake_case keys)
        """
        match_data_frame = self._base_matches.pipe(self._convert_to_matches)

        return (
            match_data_frame if to_dict is None else match_data_frame.to_dict(to_dict)
        )

    def players(
        self, to_dict: Optional[str] = "records"
    ) -> Union[pd.DataFrame, List[PlayerData]]:
        """
        Generate player data data for the given seasons.

        Returns:
        --------
        Player data that replicate fitzRoy's `get_afltables_stats` function,
            but with Pythonic conventions (e.g. snake_case keys)
        """
        player_data_frame = self._base_matches.pipe(self._convert_to_players)

        return (
            player_data_frame if to_dict is None else player_data_frame.to_dict(to_dict)
        )

    @staticmethod
    def _convert_to_fixtures(base_match_data_frame: pd.DataFrame) -> List[FixtureData]:
        return base_match_data_frame.assign(
            season_game=lambda df: df.groupby("season").cumcount()
        ).astype({"date": str})

    @staticmethod
    def _convert_to_betting_odds(
        base_match_data_frame: pd.DataFrame,
    ) -> List[BettingData]:
        home_score, away_score = (
            np.random.randint(*REASONABLE_SCORE_RANGE, size=len(base_match_data_frame)),
            np.random.randint(*REASONABLE_SCORE_RANGE, size=len(base_match_data_frame)),
        )
        home_line_odds = np.random.randint(
            *REASONABLE_MARGIN_RANGE, size=len(base_match_data_frame)
        )
        win_odds_diff = np.round(
            (np.random.rand(len(base_match_data_frame)) * WIN_ODDS_MULTIPLIER),
            decimals=2,
        )
        home_win_odds_diff = np.where(
            home_line_odds > 0, win_odds_diff, -1 * win_odds_diff
        )
        home_win_odds = BASELINE_BET_PAYOUT + home_win_odds_diff
        away_win_odds = BASELINE_BET_PAYOUT - home_win_odds_diff

        return base_match_data_frame.assign(
            round_number=lambda df: df["round"],
            round=lambda df: "Round " + df["round"].astype(str),
            home_score=home_score,
            away_score=away_score,
            home_margin=home_score - away_score,
            away_margin=away_score - home_score,
            home_win_odds=home_win_odds,
            away_win_odds=away_win_odds,
            home_win_paid=home_win_odds * (home_score > away_score).astype(int),
            away_win_paid=away_win_odds * (away_score > home_score).astype(int),
            home_line_odds=home_line_odds,
            away_line_odds=-1 * home_line_odds,
            home_line_paid=BASELINE_BET_PAYOUT * (home_score > away_score).astype(int),
            away_line_paid=BASELINE_BET_PAYOUT * (away_score > home_score).astype(int),
        ).astype({"date": str})

    @staticmethod
    def _convert_to_matches(base_match_data_frame: pd.DataFrame) -> List[MatchData]:
        match_count = len(base_match_data_frame)

        home_goals, away_goals = (
            np.random.randint(*REASONABLE_GOAL_RANGE, size=match_count),
            np.random.randint(*REASONABLE_GOAL_RANGE, size=match_count),
        )
        home_behinds, away_behinds = (
            np.random.randint(*REASONABLE_BEHIND_RANGE, size=match_count),
            np.random.randint(*REASONABLE_BEHIND_RANGE, size=match_count),
        )
        home_points, away_points = (home_goals * 6) + home_behinds, (
            away_goals * 6
        ) + away_behinds

        return base_match_data_frame.assign(
            date=lambda df: df["date"].dt.date.astype(str),
            game=lambda df: df.groupby("season").cumcount(),
            round_number=lambda df: df["round"],
            round=lambda df: "R" + df["round"].astype(str),
            round_type="Regular",
            home_goals=home_goals,
            home_behinds=home_behinds,
            home_points=home_points,
            away_goals=away_goals,
            away_behinds=away_behinds,
            away_points=away_points,
            # fitzRoy gets the margin by always subtracting away points from home points
            margin=home_points - away_points,
        )

    def _convert_to_players(self, base_match_data_frame: pd.DataFrame) -> pd.DataFrame:
        match_count = len(base_match_data_frame)

        home_quarter_goals = self._calculate_quarter_values(
            REASONABLE_GOAL_RANGE, match_count
        )
        home_quarter_behinds = self._calculate_quarter_values(
            REASONABLE_BEHIND_RANGE, match_count
        )
        away_quarter_goals = self._calculate_quarter_values(
            REASONABLE_GOAL_RANGE, match_count
        )
        away_quarter_behinds = self._calculate_quarter_values(
            REASONABLE_BEHIND_RANGE, match_count
        )

        player_match_data = (
            base_match_data_frame.assign(
                local_start_time=self._parse_player_start_time,
                date=lambda df: df["date"].dt.date.astype(str),
                attendance=np.random.randint(
                    *REASONABLE_ATTENDANCE_RANGE, size=match_count
                ),
                hq1g=home_quarter_goals[0],
                hq1b=home_quarter_behinds[0],
                hq2g=home_quarter_goals[1],
                hq2b=home_quarter_behinds[1],
                hq3g=home_quarter_goals[2],
                hq3b=home_quarter_behinds[2],
                hq4g=home_quarter_goals[3],
                hq4b=home_quarter_behinds[3],
                home_score=(np.sum(home_quarter_goals, axis=0) * 6)
                + np.sum(home_quarter_behinds, axis=0),
                aw1g=away_quarter_goals[0],
                aw1b=away_quarter_behinds[0],
                aw2g=away_quarter_goals[1],
                aw2b=away_quarter_behinds[1],
                aw3g=away_quarter_goals[2],
                aw3b=away_quarter_behinds[2],
                aw4g=away_quarter_goals[3],
                aw4b=away_quarter_behinds[3],
                away_score=(np.sum(home_quarter_goals, axis=0) * 6)
                + np.sum(home_quarter_behinds, axis=0),
                umpire_1=np.array([FAKE.name() for _ in range(match_count)]),
                umpire_2=np.array([FAKE.name() for _ in range(match_count)]),
                umpire_3=np.array([FAKE.name() for _ in range(match_count)]),
                umpire_4=np.array([FAKE.name() for _ in range(match_count)]),
                # Not totally sure what this is for, so a random integer
                # should be good enough
                group_id=np.random.randint(1000, size=match_count),
            )
            .reset_index()
            .rename(columns={"index": "match_id"})
        )

        player_data = pd.concat(
            list(
                itertools.chain.from_iterable(
                    [
                        self._generate_match_players(idx, row)
                        for idx, row in player_match_data.iterrows()
                    ]
                )
            )
        )

        return player_match_data.merge(player_data, how="right", on="match_id").drop(
            "match_id", axis=1
        )

    def _generate_match_players(
        self, player_match_index: int, player_match_row: pd.Series
    ) -> List[pd.DataFrame]:
        return [
            self._generate_players(player_match_index, player_match_row, team_column)
            for team_column in ["home_team", "away_team"]
        ]

    @staticmethod
    def _generate_players(
        player_match_index: int, player_match_row: pd.Series, team_column: str
    ) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "match_id": player_match_index,
                "first_name": np.array(
                    [FAKE.first_name() for _ in range(N_PLAYERS_PER_TEAM)]
                ),
                "surname": np.array(
                    [FAKE.last_name() for _ in range(N_PLAYERS_PER_TEAM)]
                ),
                "id": np.array(range(N_PLAYERS_PER_TEAM))
                + (player_match_index * N_PLAYERS_PER_TEAM * 2),
                "jumper_no": np.random.randint(0, 100, size=N_PLAYERS_PER_TEAM),
                "playing_for": player_match_row[team_column],
                "kicks": np.random.randint(
                    *REASONABLE_KICK_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "marks": np.random.randint(
                    *REASONABLE_MARK_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "handballs": np.random.randint(
                    *REASONABLE_HANDBALL_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                # Acknowledging that this means that the sum of player goals
                # is unlikely to equal the sum of team quarter goals,
                # but no point in over-complicating calculations until we need to.
                "goals": np.random.randint(
                    *REASONABLE_PLAYER_GOAL_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "behinds": np.random.randint(
                    *REASONABLE_PLAYER_BEHIND_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "hit_outs": np.random.randint(
                    *REASONABLE_HIT_OUT_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "tackles": np.random.randint(
                    *REASONABLE_TACKLE_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "rebounds": np.random.randint(
                    *REASONABLE_REBOUND_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "inside_50s": np.random.randint(
                    *REASONABLE_INSIDE_50_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "clearances": np.random.randint(
                    *REASONABLE_CLEARANCE_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "clangers": np.random.randint(
                    *REASONABLE_CLANGER_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "frees_for": np.random.randint(
                    *REASONABLE_FREE_FOR_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "frees_against": np.random.randint(
                    *REASONABLE_FREE_AGAINST_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                # Acknowledging that this won't restrict brownlow votes to 3 players
                # per match, but no point in over-complicating calculations
                # until we need to.
                "brownlow_votes": np.random.randint(
                    *BROWNLOW_VOTES_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "contested_possessions": np.random.randint(
                    *REASONABLE_CONTESTED_POSSESSION_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "uncontested_possessions": np.random.randint(
                    *REASONABLE_UNCONTESTED_POSSESSION_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "contested_marks": np.random.randint(
                    *REASONABLE_CONTESTED_MARK_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "marks_inside_50": np.random.randint(
                    *REASONABLE_MARK_INSIDE_50_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "one_percenters": np.random.randint(
                    *REASONABLE_ONE_PERCENTER_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "bounces": np.random.randint(
                    *REASONABLE_BOUNCE_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "goal_assists": np.random.randint(
                    *REASONABLE_GOAL_ASSIST_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "time_on_ground": np.random.randint(
                    *REASONABLE_TIME_ON_GROUND_RANGE, size=N_PLAYERS_PER_TEAM
                ),
                "substitute": np.random.randint(
                    *SUBSTITUTE_RANGE, size=N_PLAYERS_PER_TEAM
                ),
            }
        )

    @staticmethod
    def _parse_player_start_time(player_data_frame: pd.DataFrame) -> int:
        # It's a little wonky, but for player data, fitzRoy returns match times
        # in the form of 'hhmm' as an integer
        return (
            player_data_frame["date"].dt.hour.astype(str)
            + player_data_frame["date"].dt.minute.astype(str)
        ).astype(int)

    @staticmethod
    def _calculate_quarter_values(
        value_range: Tuple[int, int], size: int
    ) -> List[np.array]:
        return [
            (np.random.randint(*value_range, size=size) / 4).astype(int)
            for _ in range(4)
        ]

    def _generate_seasons(self) -> List[BaseMatchData]:
        return list(
            itertools.chain.from_iterable(
                [self._generate_season(season) for season in self._season_range]
            )
        )

    def _generate_season(self, season: int) -> List[BaseMatchData]:
        # Seasons have typically started in mid-to-late March since the 70s
        start_date = datetime(season, MAR, FIFTEENTH)
        # Typically, rounds start on Thursday or Friday and end on Sunday,
        # but can range from Wednesday to Tuesday, with a few exceptions.
        difference_from_wed = WEDNESDAY - start_date.weekday()
        season_start = start_date + timedelta(days=difference_from_wed)

        # Seasons typically end somewhere between mid September and mid October,
        # so we split the difference.
        season_end = datetime(season, SEP, THIRTIETH)
        week_count = math.floor((season_end - season_start).days / WEEK_IN_DAYS)

        return list(
            itertools.chain.from_iterable(
                [self._generate_round(season_start, week) for week in range(week_count)]
            )
        )

    def _generate_round(self, season_start: datetime, week: int) -> List[BaseMatchData]:
        round_start = season_start + timedelta(days=(WEEK_IN_DAYS * week))
        round_number = week + 1

        team_count = len(NON_BRISBANE_TEAMS) + 1
        match_count = math.floor(team_count / 2)
        min_match_number = (week * match_count) + 1
        max_match_number = min_match_number + match_count

        teams = self._generate_teams()
        venues = (venue for venue in np.random.permutation(VENUES))

        match_data_func = partial(
            self._generate_match,
            round_number,
            round_start,
        )

        return [
            match_data_func(teams=(next(teams), next(teams)), venue=next(venues))
            for _ in range(min_match_number, max_match_number)
        ]

    def _generate_match(
        self,
        round_number: int,
        round_start_date: datetime,
        teams: Tuple[str, str],
        venue: str,
    ) -> BaseMatchData:
        match_date_time = self._match_date_time(round_start_date)
        home_team, away_team = teams

        return {
            "date": match_date_time,
            "season": match_date_time.year,
            "round": round_number,
            "home_team": home_team,
            "away_team": away_team,
            "venue": venue,
        }

    @staticmethod
    def _match_date_time(round_start_date: datetime) -> datetime:
        raw_match_date_time = FAKE.date_time_between_dates(
            datetime_start=round_start_date,
            datetime_end=(round_start_date + timedelta(days=WEEK_IN_DAYS)),
        )
        # We need to generate the time separately to make sure we have
        # a realistic start time for the match on the randomly-generated day.
        raw_match_time = FAKE.date_time_between_dates(
            datetime_start=raw_match_date_time.replace(
                hour=MIN_MATCH_HOUR, minute=0, second=0
            ),
            datetime_end=raw_match_date_time.replace(
                hour=MAX_MATCH_HOUR, minute=0, second=0
            ),
        ).time()

        return raw_match_date_time.replace(
            hour=raw_match_time.hour,
            minute=raw_match_time.minute,
            second=raw_match_time.second,
        )

    @staticmethod
    def _generate_teams():
        # We only want one Brisbane team per round, because depending on how team names
        # are normalised we can end up with duplicate teams, which is invalid.
        # It seems that there's more consensus on how to handle other teams that moved
        # or folded.
        valid_teams = NON_BRISBANE_TEAMS + [np.random.choice(BRISBANE_TEAMS)]
        return (team for team in np.random.permutation(valid_teams))

    @property
    def _season_range(self) -> range:
        current_year = date.today().year

        if isinstance(self.seasons, int):
            return self._int_season_range(self.seasons, current_year)

        if isinstance(self.seasons, tuple):
            return self._tuple_season_range(self.seasons, current_year)

        raise TypeError(
            "seasons argument must be either an integer or a tuple of two integers"
        )

    @staticmethod
    def _int_season_range(seasons: int, current_year: int) -> range:
        assert seasons > 0, "Must generate fixture data for at least one season."

        # We add 2, because we are open to the possibility of including matches
        # from the current year in the data.
        max_start_season = current_year - seasons + 2
        start_season = np.random.choice(np.arange(FIRST_AFL_SEASON, max_start_season))
        end_season = start_season + seasons

        return range(start_season, end_season)

    @staticmethod
    def _tuple_season_range(seasons: Tuple[int, int], current_year: int) -> range:
        assert (
            len(seasons) == 2
        ), f"Must provide two seasons to have a valid range, but {seasons} was given."

        assert min(seasons) >= FIRST_AFL_SEASON and max(seasons) <= current_year + 1, (
            f"Provided seasons must be in the range of {FIRST_AFL_SEASON} to "
            f"{current_year + 1} (inclusive) to generate valid data."
        )

        assert (
            seasons[0] < seasons[1]
        ), "First season must be less than second to create a valid range."

        return range(*seasons)
