from __future__ import annotations

import pwd
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Union

from yaml import dump, load

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader


def load_config(discoset):
    with open(discoset, "rb") as f:
        raw_config = load(f, Loader=Loader)

    # The only supported top-level key for now is "hosts"
    raw_config = raw_config["hosts"]
    return Config.build(raw_config)


@dataclass
class Item:
    source: Path
    target: Path
    permissions: str

    @classmethod
    def build(cls, data: Union[str, dict]) -> Item:
        if isinstance(data, str):
            source = Path(data)
            target = Path(data)
            item = cls(source=source, target=target, permissions=None)
        elif isinstance(data, dict):
            source = Path(data["source"])
            target = Path(data["target"])
            item = cls(
                source=source, target=target, permissions=data.get("permissions", None)
            )
        else:
            raise Exception("Config error: Unknown data type")
        return item

    def __str__(self):
        return f"{self.source} -> {self.target}"


@dataclass
class User:
    items: List[Union[str, dict]] = field(default_factory=list)

    @classmethod
    def build(cls, data) -> User:
        user = cls()
        for item_data in data:
            user.items.append(Item.build(item_data))
        return user

    def __iter__(self):
        return iter(self.items)


@dataclass
class Host:
    users: Dict[str, User] = field(default_factory=dict)

    @classmethod
    def build(cls, data) -> Host:
        host = cls()
        for user_name, user_data in data.items():
            host.users[user_name] = User.build(user_data)
        return host

    def get_user(self, username: str) -> User:
        return self.users[username]


@dataclass
class Config:
    hosts: Dict[str, Host] = field(default_factory=dict)

    @classmethod
    def build(cls, data) -> Config:
        config = cls()
        for host_name, host_data in data.items():
            config.hosts[host_name] = Host.build(host_data)
        return config

    def get_host(self, hostname: str) -> Host:
        return self.hosts[hostname]
