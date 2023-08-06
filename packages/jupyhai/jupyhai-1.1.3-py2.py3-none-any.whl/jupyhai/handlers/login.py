import os

from valohai_cli.api import request
from valohai_cli.exceptions import APIError, CLIException, APINotFoundError

from jupyhai.api_urls import ME_URL, SERVER_INFO_URL
from jupyhai.consts import NOTEBOOK_INSTANCE_ID, HOST
from jupyhai.handlers.base import JupyhaiHandler
from jupyhai.utils.auth import get_current_username, login_status, login_with_credentials, verify_and_save_token


class LoginHandler(JupyhaiHandler):
    def get(self):
        flavor = None
        logged_in = login_status()
        if logged_in:
            try:
                request('GET', ME_URL).json()
            except APIError as ae:
                # TODO: this is a terrible hack :(
                if 'token_expired' in str(ae):
                    logged_in = False

            try:
                response = request('GET', SERVER_INFO_URL)
                flavor = response.json()['flavor']
            except APINotFoundError:
                flavor = "valohai"

        username = get_current_username()
        self.finish(
            {
                "logged_in": logged_in,
                "username": username,
                "notebook_instance_id": NOTEBOOK_INSTANCE_ID,
                "host_flavor": flavor
            }
        )

    def post(self):
        args = self.get_json_body()
        try:
            if args.get('token'):
                self.log.info("Logging in with token...")
                verify_and_save_token(args['token'])
            else:
                host = args.get('hostUrl', HOST)
                if not host.startswith('http://') and not host.startswith('https://'):
                    host = 'http://' + host

                self.log.info(f"Logging in with username + password into {host}...")
                login_with_credentials(
                    username=args['username'],
                    password=args['password'],
                    host=host,
                )
        except CLIException as e:
            self.log.error(e)
        finally:
            self.finish({'success': login_status()})
