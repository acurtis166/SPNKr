"""
https://settings.svc.halowaypoint.com/settings/hipc/e2a0a7c6-6efe-42af-9283-c2ab73250c48
"""

import json
import pathlib

SCHEMES = {
    2: 'Https',
    8: 'SecureAmqpWebSocket',
    9: 'GameCms',
}

AUTHENTICATION_METHODS = {
    0: None,
    1: 'SpartanToken',
    4: 'XSTSv3HaloAudience',
    9: 'XSTSv3XboxAudience',
    10: 'ClientCertificate',
    15: 'SpartanTokenV4',
}

def main():
    # load endpoints file
    with open('resources/endpoints.json') as fp:
        data = json.load(fp)

    authorities = data['Authorities']

    for name, auth in authorities.items():
        module_name = name.replace('-', '_').lower()
        module_dir = pathlib.Path(module_name)
        module_dir.mkdir(exist_ok=True)
        scheme = SCHEMES[auth['Scheme']]
        auth_methods = [AUTHENTICATION_METHODS[a] for a in auth['AuthenticationMethods']]
        host = auth['Hostname']
        port = auth['Port']
        url = f'https://{host}:{port}'
        endpoints = filter(lambda ep: ep[1]['AuthorityId'] == name, data['Endpoints'].items())

        with open(module_name + '/__init__.py', 'w') as fp:
            fp.write('""""""\n\n')
            fp.write('from halo_infinite_api.api import util\n')
            fp.write('from halo_infinite_api.api.authorities import base\n')
            fp.write(f'from halo_infinite_api.api.authorities.{module_name} import models\n\n\n')
            fp.write(f'class {module_name}Authority(base.BaseAuthority):\n\n')
            fp.write(f"    URL = '{url}'\n")
            fp.write(f'    AUTHENTICATION_METHODS = {auth_methods}\n')
            fp.write(f"    SCHEME = '{scheme}'\n\n")
            for ep_name, ep in endpoints:
                func_name = ep_name.split('_')[-1].lower()
                fp.write(f'    def {func_name}(self):\n')
                fp.write(f"        url = self.URL + '{ep['Path']}'\n")
                fp.write(f"        params = '{ep['QueryString']}'\n")
                fp.write('        resp = self._session.get(url, params=params)\n\n\n')

        with open(module_name + '/models.py', 'w') as fp:
            fp.write('')


if __name__ == '__main__':
    main()

