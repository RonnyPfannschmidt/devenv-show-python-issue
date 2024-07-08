# from https://www.minecraftforum.net/forums/mapping-and-modding-java-edition/minecraft-tools/3026007-java-edition-convert-offline-mode-server-to-an
# this file is a incomplete rewrite to show the issue

import os
from uuid import UUID
import nbt #type: ignore[import-untyped]
import requests
import argparse
from pathlib import Path

from shutil import copyfile
from json.decoder import JSONDecodeError

parser = argparse.ArgumentParser()

parser.add_argument("input")
parser.add_argument("output")


UIDMap = dict[UUID, UUID]

def get_online_uuid(name: str) -> UUID | None:
    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"

    response = requests.get(url=url)

    try:
        data = response.json()

        data_uuid = data["id"]
        parsed_uuid = UUID(data_uuid)

        print(f"{name=} {parsed_uuid=}")

        return parsed_uuid
    except JSONDecodeError as error:
        print(f"{name=} {error=}")

        return None


def get_old_uuids(input: Path) -> list[UUID]:
    player_dot_dats = input.glob("playerdata/*.dat")
    return [UUID(p.stem) for p in player_dot_dats]


def get_lastknown_name(input: Path, user: UUID) -> str:
    nbt_path = input.joinpath(f"playerdata/{user}.dat")
    nbtfile = nbt.nbt.NBTFile(os.fspath(nbt_path))
    return str(nbtfile["bukkit"]["lastKnownName"])



def get_new_uuids(input: Path, uuids: list[UUID]) -> UIDMap:
    return {uuid: ouid for uuid in uuids if (ouid := get_online_uuid(get_lastknown_name(input, uuid))) is not None}


def convert_player_dat(original: UUID, new: UUID ) -> None:

    copyfile(
        f"input/playerdata/{original}.dat", f"output/playerdata/{new}.dat"
    )


def convert_advancements(original: UUID, new: UUID) -> None:
    copyfile(
        f"input/advancements/{original}.json",
        f"output/advancements/{new}.json",
    )


def convert_files(conversions: UIDMap) -> None:
    for conversion in conversions.items():
        convert_player_dat(conversion[0], conversion[1])
        convert_advancements(conversion[0], conversion[1])



if __name__ == "__main__":
    input = Path("input")
    output = Path("output")
    convert_files(get_new_uuids(input, get_old_uuids(input)))
