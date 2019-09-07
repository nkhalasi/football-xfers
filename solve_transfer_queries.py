import json
from collections import namedtuple
from typing import NamedTuple
from itertools import groupby

Player = namedtuple(
    "Player", ["href", "name", "position", "age", "image", "nationality"])
Team = namedtuple("Team", ("href", "name", "country",
                           "countryImage", "league", "leagueHref", "image"))


class Transfer():
    href: str
    value: float
    timestamp: int

    def __init__(self, _href: str = None, _value: str = None, _timestamp: str = None):
        self.href = _href
        _val = "0" if _value.strip() in (
            "?", "-", "", "0", "draft") else _value[1:]

        if _val[-1] == "m":
            self.value = float(_val[:-1]) * 1000 * 1000
        elif _val[-1] == "k":
            self.value = float(_val[:-1]) * 1000
        else:
            self.value = float(_val)
        self.timestamp = _timestamp

    @classmethod
    def from_dict(cls, data_dict):
        return cls(_href=data_dict["href"], _value=data_dict["value"], _timestamp=data_dict["timestamp"])

    def __repr__(self):
        return "Transfer(href={}, value={}, timestamp={})".format(self.href, self.value, self.timestamp)


class GameSeason(NamedTuple):
    season: str
    player: dict
    fromTeam: dict
    toTeam: dict
    transfer: dict

    @classmethod
    def from_dict(cls, data_dict):
        return cls(data_dict["season"],
                   Player(**data_dict["player"]),
                   Team(**data_dict["from"]),
                   Team(**data_dict["to"]),
                   Transfer.from_dict(data_dict["transfer"]))


def load_data(data_fpath: str):
    seasons_data = list()
    with (open(data_fpath, "rb")) as f:
        seasons_data.extend(
            [GameSeason.from_dict(json.loads(data_line))
             for data_line in f.readlines()]
        )
    return seasons_data


def top10_transfers_by_value(data: list):
    return sorted(data, key=lambda gs: gs.transfer.value, reverse=True)[:10]


def transfer_in_filter_fn(gs): return gs.toTeam.name.strip() != ""


def transfer_in_key_fn(gs): return gs.toTeam.name


def team_with_max_transfers_in(data):
    return _team_with_max_transfers(data, transfer_in_filter_fn, transfer_in_key_fn)


def transfer_out_filter_fn(gs): return gs.fromTeam.name.strip() != ""


def transfer_out_key_fn(gs): return gs.fromTeam.name


def team_with_max_transfers_out(data):
    return _team_with_max_transfers(data, transfer_out_filter_fn, transfer_out_key_fn)


def _team_with_max_transfers(data: list, filter_fn, key_fn):
    teams_with_names = filter(filter_fn, data)
    teams_sorted_by_transfer_teams = \
        sorted(teams_with_names, key=key_fn)

    teams_grouped_by_transfers = \
        groupby(teams_sorted_by_transfer_teams,
                key=key_fn)

    teams_with_transfer_counts = \
        [(team_name, len(list(xfers)))
         for team_name, xfers in teams_grouped_by_transfers]

    return sorted(teams_with_transfer_counts, key=lambda x: x[1], reverse=True)[0]


if __name__ == "__main__":
    data = load_data("transfers.json")
    for d in top10_transfers_by_value(data):
        print("{} ** {} ** {} ** {}".format(d.player.name,
                                            d.fromTeam.name, d.toTeam.name, d.transfer.value))

    print("--*--" * 25)
    print(team_with_max_transfers_in(data))

    print("--*--" * 25)
    print(team_with_max_transfers_out(data))
