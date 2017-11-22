from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class MAASProvides(Endpoint):

    @when('endpoint.{endpoint_name}.joined')
    def joined(self):
        set_flag(self.flag('{endpoint_name}.available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def broken(self):
        clear_flag(self.flag('{endpoint_name}.available'))

    def configure(self, maas_url, secret):
        for relation in self.relations:
            relation.to_publish_raw.update({
                'maas_url': maas_url,
                'secret': secret,
            })
