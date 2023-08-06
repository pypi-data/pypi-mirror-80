# Copyright (c) 2014-2020 GeoSpock Ltd.

import json
import keyring
import os
import socket
from pathlib import Path
from time import time

import click
from pkg_resources import resource_string
from typing import Optional
from geospock_cli.exceptions import CLIError


class ConfigReaderAndWriter:
    GEOSPOCK_DIR = Path.home().joinpath(".geospock")
    GEOSPOCK_FILE = GEOSPOCK_DIR.joinpath("credentials")
    CONFIG_FILE = GEOSPOCK_DIR.joinpath("config.json")
    MESSAGES = json.loads(resource_string('geospock_cli', "messages.json").decode("utf-8"))
    KEY = socket.gethostname()

    def __init__(self, profile: str, show_browser: bool):
        self.profile = profile
        self.show_browser = show_browser
        self.config = None
        self.credentials = None

    def write_login(self, username: str, password: str, request_address: str):
        Path(self.GEOSPOCK_DIR).mkdir(parents=True, exist_ok=True)

        if os.path.exists(self.CONFIG_FILE) and os.path.getsize(self.CONFIG_FILE) > 0:
            with open(self.CONFIG_FILE) as json_file:
                try:
                    current_config = json.load(json_file)
                except json.JSONDecodeError:
                    raise CLIError(ConfigReaderAndWriter.MESSAGES["invalidConfig"])
        else:
            current_config = dict()
        try:
            current_config[self.profile] = dict(request_address=request_address)
        except Exception:
            raise CLIError("Could not generate configuration entry from provided request address.")
        with open(self.CONFIG_FILE, "w") as config_file_write:
            config_file_write.write(json.dumps(current_config, indent=4))
        keyring.set_password("geospock", self.profile + "-username", username)
        keyring.set_password("geospock", self.profile + "-password", password)

    def write_logout(self):
        if os.path.exists(self.CONFIG_FILE) and os.path.getsize(self.CONFIG_FILE) > 0:
            current_config = dict()
            with open(self.CONFIG_FILE) as json_file:
                try:
                    current_config = json.load(json_file)
                    current_config.pop(self.profile, None)
                except json.JSONDecodeError:
                    raise CLIError(ConfigReaderAndWriter.MESSAGES["invalidConfig"])
            with open(self.CONFIG_FILE, "w") as config_file_write:
                config_file_write.write(json.dumps(current_config, indent=4))
        try:
            keyring.delete_password("geospock", self.profile + "-username")
            keyring.delete_password("geospock", self.profile + "-password")
        except keyring.errors.PasswordDeleteError:
            pass

    def decode(self):
        user = keyring.get_password("geospock", self.profile + "-username")
        password = keyring.get_password("geospock", self.profile + "-password")
        return user, password

    def write_to_config(self, client_id: str, audience: str, auth0url: str, request_address: str) -> None:
        Path(self.GEOSPOCK_DIR).mkdir(parents=True, exist_ok=True)

        if os.path.exists(self.CONFIG_FILE) and os.path.getsize(self.CONFIG_FILE) > 0:
            with open(self.CONFIG_FILE) as json_file:
                try:
                    current_config = json.load(json_file)
                except json.JSONDecodeError:
                    raise CLIError(ConfigReaderAndWriter.MESSAGES["invalidConfig"])
                if self.profile in current_config and "client_id" in current_config[self.profile]:
                    if current_config[self.profile]["client_id"] == client_id and \
                            current_config[self.profile]["audience"] == audience and \
                            current_config[self.profile]["auth0_url"] == auth0url and \
                            current_config[self.profile]["request_address"] == request_address:
                        click.echo("No change to configuration")
                    else:
                        click.echo("Change in configuration - please rerun 'geospock get-credentials{}'"
                                   .format(" --profile " + self.profile if self.profile != "default" else ""))

                        if os.path.exists(self.GEOSPOCK_FILE) and os.path.getsize(self.GEOSPOCK_FILE) > 0:
                            with open(self.GEOSPOCK_FILE, "r") as current_geospock_file:
                                try:
                                    credentials = json.load(current_geospock_file)
                                    credentials.pop(self.profile, None)
                                except json.JSONDecodeError:
                                    raise CLIError(ConfigReaderAndWriter.MESSAGES["invalidConfig"])
                            with open(self.GEOSPOCK_FILE, "w+") as current_geospock_file:
                                current_geospock_file.write(json.dumps(credentials, indent=4))

        else:
            current_config = dict()

        current_config[self.profile] = dict(client_id=client_id, audience=audience, auth0_url=auth0url,
                                            request_address=request_address)

        with open(self.CONFIG_FILE, "w") as config_file_write:
            config_file_write.write(json.dumps(current_config, indent=4))

    def save_tokens(self, tokens: dict, refresh_token=None) -> None:
        if tokens is None:
            click.secho("Failed to authenticate", fg="red")
            return
        if not os.path.exists(self.GEOSPOCK_DIR):
            raise CLIError(ConfigReaderAndWriter.MESSAGES["credentialsDirectory"])
        tokens["creation_time"] = int(time())
        if refresh_token is not None:
            tokens["refresh_token"] = refresh_token

        if os.path.exists(self.GEOSPOCK_FILE) and os.path.getsize(self.GEOSPOCK_FILE) > 0:
            with open(self.GEOSPOCK_FILE) as json_file:
                try:
                    current_geospock_file = json.load(json_file)
                except json.JSONDecodeError:
                    raise CLIError(ConfigReaderAndWriter.MESSAGES["invalidCredentials"])
        else:
            current_geospock_file = dict()
        current_geospock_file[self.profile] = tokens
        with open(self.GEOSPOCK_FILE, "w+") as output_file:
            output_file.write(json.dumps(current_geospock_file, indent=4))

    def get_config(self) -> dict:
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE) as json_file:
                try:
                    config_all = json.load(json_file)
                except json.JSONDecodeError:
                    raise CLIError(ConfigReaderAndWriter.MESSAGES["invalidConfig"])
            if self.profile in config_all:
                self.config = config_all[self.profile]
            return config_all
        else:
            raise CLIError("Error opening config file")

    def get_all_credentials_from_file(self) -> Optional[dict]:
        if not self.config:
            raise CLIError("Error opening config file")
        elif os.path.exists(self.GEOSPOCK_FILE) and os.path.getsize(self.GEOSPOCK_FILE) > 0:
            with open(self.GEOSPOCK_FILE) as file:
                try:
                    all_credentials = json.load(file)
                except json.JSONDecodeError:
                    raise CLIError(ConfigReaderAndWriter.MESSAGES["invalidCredentials"])
                return all_credentials
        else:
            return None
