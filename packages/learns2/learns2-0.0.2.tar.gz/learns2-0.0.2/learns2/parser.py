from s2protocol import versions
from mpyq import MPQArchive
import os

from typing import List


class SC2ReplayParser(object):
    def __init__(self, replay: str):
        assert os.path.isfile(replay), f'{replay} is not a file'
        self.archive = MPQArchive(replay)
        self.protocol = self.read_protocol(self.archive)
        self._initdata = None
        self._details = None

    @staticmethod
    def read_protocol(archive: MPQArchive):
        content = archive.header['user_data_header']['content']
        header = versions.latest().decode_replay_header(content)
        base_build = header['m_version']['m_baseBuild']
        return versions.build(base_build)

    @staticmethod
    def read_initdata(protocol, archive: MPQArchive) -> dict:
        init_file = archive.read_file('replay.initData')
        return protocol.decode_replay_initdata(init_file)

    @staticmethod
    def read_details(protocol, archive: MPQArchive) -> dict:
        detail_file = archive.read_file('replay.details')
        return protocol.decode_replay_details(detail_file)

    def initdata(self) -> dict:
        if self._initdata is None:
            self._initdata = self.read_initdata(self.protocol, self.archive)
        return self._initdata

    def details(self) -> dict:
        """https://github.com/Blizzard/s2protocol/blob/master/docs/flags/details.md"""
        if self._details is None:
            self._details = self.read_details(self.protocol, self.archive)
        return self._details

    def players(self) -> List[dict]:
        slots = self.initdata()['m_syncLobbyState']['m_lobbyState']['m_slots']
        slot_id_to_user_id = {}
        for slot in slots:
            if slot['m_observe'] == 0:
                slot_id, user_id = slot['m_workingSetSlotId'], slot['m_userId']
                slot_id_to_user_id[slot_id] = user_id
        player_list = self.details()['m_playerList']
        player_objects = []
        for player in player_list:
            slot_id = player['m_workingSetSlotId']
            if slot_id in slot_id_to_user_id:
                player['m_userId'] = slot_id_to_user_id[slot_id]
                player['m_userInitialData'] = self.initdata()['m_syncLobbyState']['m_userInitialData'][slot_id]
                player_objects.append(player)
        return player_objects

    def small_details(self):
        details = self.details()
        description = self.initdata()['m_syncLobbyState']['m_gameDescription']
        return {
            'm_title': details['m_title'],
            'm_isBlizzardMap': details['m_isBlizzardMap'],
            'm_timeUTC': details['m_timeUTC'],
            'm_timeLocalOffset': details['m_timeLocalOffset'],
            'm_mapSizeX': description['m_mapSizeX'],
            'm_mapSizeY': description['m_mapSizeY']
        }

    def to_dict(self):
        return {
            'details': self.small_details(),
            'players': self.players()
        }
