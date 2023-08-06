# Copyright 2019 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron_lib import constants
from neutron_lib.utils import test
from oslo_log import log
from tempest.lib.common.utils import data_utils
from tempest.lib import decorators
from tempest.lib import exceptions as lib_exc

from neutron_tempest_plugin.common import ssh
from neutron_tempest_plugin.common import utils
from neutron_tempest_plugin import config
from neutron_tempest_plugin.scenario import base

CONF = config.CONF

LOG = log.getLogger(__name__)


class PortForwardingTestJSON(base.BaseTempestTestCase):

    required_extensions = ['router', 'floating-ip-port-forwarding']

    @classmethod
    def resource_setup(cls):
        super(PortForwardingTestJSON, cls).resource_setup()
        cls.network = cls.create_network()
        cls.subnet = cls.create_subnet(cls.network)
        cls.router = cls.create_router_by_client()
        cls.create_router_interface(cls.router['id'], cls.subnet['id'])
        cls.fip = cls.create_floatingip()
        cls.secgroup = cls.create_security_group(
            name=data_utils.rand_name("test_port_secgroup"))
        cls.create_loginable_secgroup_rule(secgroup_id=cls.secgroup['id'])
        cls.keypair = cls.create_keypair()

    def _prepare_resources(self, num_servers, internal_tcp_port, protocol,
                           external_port_base=1025):
        servers = []
        for i in range(1, num_servers + 1):
            internal_udp_port = internal_tcp_port + 10
            external_tcp_port = external_port_base + i
            external_udp_port = external_tcp_port + 10
            name = data_utils.rand_name("server-%s" % i)
            port = self.create_port(
                self.network,
                security_groups=[self.secgroup['id']])
            server = self.create_server(
                flavor_ref=CONF.compute.flavor_ref,
                image_ref=CONF.compute.image_ref,
                key_name=self.keypair['name'], name=name,
                networks=[{'port': port['id']}])['server']
            server['name'] = name
            self.wait_for_server_active(server)
            server['port_forwarding_tcp'] = self.create_port_forwarding(
                self.fip['id'],
                internal_port_id=port['id'],
                internal_ip_address=port['fixed_ips'][0]['ip_address'],
                internal_port=internal_tcp_port,
                external_port=external_tcp_port,
                protocol=constants.PROTO_NAME_TCP)
            server['port_forwarding_udp'] = self.create_port_forwarding(
                self.fip['id'],
                internal_port_id=port['id'],
                internal_ip_address=port['fixed_ips'][0]['ip_address'],
                internal_port=internal_udp_port,
                external_port=external_udp_port,
                protocol=constants.PROTO_NAME_UDP)
            servers.append(server)
        return servers

    def _test_udp_port_forwarding(self, servers):

        def _message_received(server, ssh_client, expected_msg):
            self.nc_listen(ssh_client,
                           server['port_forwarding_udp']['internal_port'],
                           constants.PROTO_NAME_UDP,
                           expected_msg,
                           [server])
            received_msg = self.nc_client(
                self.fip['floating_ip_address'],
                server['port_forwarding_udp']['external_port'],
                constants.PROTO_NAME_UDP)
            return expected_msg in received_msg

        for server in servers:
            expected_msg = "%s-UDP-test" % server['name']
            ssh_client = ssh.Client(
                self.fip['floating_ip_address'],
                CONF.validation.image_ssh_user,
                pkey=self.keypair['private_key'],
                port=server['port_forwarding_tcp']['external_port'])
            utils.wait_until_true(
                lambda: _message_received(server, ssh_client, expected_msg),
                exception=RuntimeError(
                    "Timed out waiting for message from server {!r} ".format(
                        server['id'])))

    @test.unstable_test("bug 1896735")
    @decorators.idempotent_id('ab40fc48-ca8d-41a0-b2a3-f6679c847bfe')
    def test_port_forwarding_to_2_servers(self):
        udp_sg_rule = {'protocol': constants.PROTO_NAME_UDP,
                       'direction': constants.INGRESS_DIRECTION,
                       'remote_ip_prefix': '0.0.0.0/0'}
        self.create_secgroup_rules(
            [udp_sg_rule], secgroup_id=self.secgroup['id'])
        servers = self._prepare_resources(
            num_servers=2, internal_tcp_port=22,
            protocol=constants.PROTO_NAME_TCP)
        # Test TCP port forwarding by SSH to each server
        self.check_servers_hostnames(servers)
        # And now test UDP port forwarding using nc
        self._test_udp_port_forwarding(servers)

    @test.unstable_test("bug 1896735")
    @decorators.idempotent_id('aa19d46c-a4a6-11ea-bb37-0242ac130002')
    def test_port_forwarding_editing_and_deleting_tcp_rule(self):
        server = self._prepare_resources(
            num_servers=1, internal_tcp_port=22,
            protocol=constants.PROTO_NAME_TCP,
            external_port_base=1035)
        fip_id = server[0]['port_forwarding_tcp']['floatingip_id']
        pf_id = server[0]['port_forwarding_tcp']['id']

        # Check connectivity with the original parameters
        self.check_servers_hostnames(server)

        # Use a reasonable timeout to verify that connections will not
        # happen. Default would be 196 seconds, which is an overkill.
        test_ssh_connect_timeout = 6

        # Update external port and check connectivity with original parameters
        # Port under server[0]['port_forwarding_tcp']['external_port'] should
        # not answer at this point.

        def fip_pf_connectivity():
            try:
                self.check_servers_hostnames(
                    server, timeout=test_ssh_connect_timeout)
                return True
            except (AssertionError, lib_exc.SSHTimeout):
                return False

        def no_fip_pf_connectivity():
            return not fip_pf_connectivity()

        self.client.update_port_forwarding(fip_id, pf_id, external_port=3333)
        utils.wait_until_true(
            no_fip_pf_connectivity,
            exception=RuntimeError(
                "Connection to the server {!r} through "
                "port {!r} is still possible.".format(
                    server[0]['id'],
                    server[0]['port_forwarding_tcp']['external_port'])))

        # Check connectivity with the new parameters
        server[0]['port_forwarding_tcp']['external_port'] = 3333
        utils.wait_until_true(
            fip_pf_connectivity,
            exception=RuntimeError(
                "Connection to the server {!r} through "
                "port {!r} is not possible.".format(
                    server[0]['id'],
                    server[0]['port_forwarding_tcp']['external_port'])))

        # Remove port forwarding and ensure connection stops working.
        self.client.delete_port_forwarding(fip_id, pf_id)
        self.assertRaises(lib_exc.NotFound, self.client.get_port_forwarding,
                          fip_id, pf_id)
        utils.wait_until_true(
            no_fip_pf_connectivity,
            exception=RuntimeError(
                "Connection to the server {!r} through "
                "port {!r} is still possible.".format(
                    server[0]['id'],
                    server[0]['port_forwarding_tcp']['external_port'])))
