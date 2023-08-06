import attr
import json
import os
import logging


@attr.s(frozen=True)
class RootServersFile:
    """
    The repository for RootServers
    """

    _file = attr.ib()
    _logger = attr.ib(default=attr.Factory(lambda: logging.getLogger("sakia")))
    filename = "root_servers.yml"

    @classmethod
    def in_config_path(cls, config_path, profile_name):
        if not os.path.exists(os.path.join(config_path, profile_name)):
            os.makedirs(os.path.join(config_path, profile_name))
        return cls(os.path.join(config_path, profile_name, RootServersFile.filename))

    def load_or_init(self, profile_name):
        """
        Update root_servers constant

        :param sakia.data.entities.UserParameters user_parameters: the user_parameters to update
        """
        try:
            with open(self._file, "r") as json_data:
                user_parameters = UserParameters(**json.load(json_data))
                user_parameters.profile_name = profile_name
        except (OSError, json.decoder.JSONDecodeError):
            user_parameters = UserParameters(profile_name=profile_name)
        return user_parameters
