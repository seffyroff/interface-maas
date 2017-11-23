from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class MAASRequires(Endpoint):

    @when('endpoint.{endpoint_name}.changed')
    def changed(self):
        if any(unit.received['secret'] for unit in self.all_units):
            set_flag(self.flag('{endpoint_name}.available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.flag('{endpoint_name}.available'))

    def services(self):
        """
        Returns a list of available HTTP services and their associated hosts
        and ports.
        The return value is a list of dicts of the following form::
            [
                {
                    'service_name': name_of_service,
                    'hosts': [
                        {
                            'secret': secret,
                            'maas_url': maas_url,
                        },
                        # ...
                    ],
                },
                # ...
            ]
        """
        services = {}
        for relation in self.relations:
            service_name = relation.application_name
            service = services.setdefault(service_name, {
                'service_name': service_name,
                'hosts': [],
            })
            for unit in relation.units:
                secret = unit.received_raw['secret']
                maas_url = unit.received_raw['maas_url']
                if maas_url and secret:
                    service['hosts'].append({
                        'secret': secret,
                        'maas_url': maas_url,
                    })
        return [s for s in services.values() if s['hosts']]
