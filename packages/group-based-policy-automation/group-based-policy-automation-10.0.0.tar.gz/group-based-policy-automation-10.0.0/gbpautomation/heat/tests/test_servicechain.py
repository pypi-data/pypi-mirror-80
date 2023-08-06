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

import copy

import mock
import six

from gbpautomation.heat.engine.resources import servicechain
from gbpclient.v2_0 import client as gbpclient
from heat.common import exception
from heat.common import template_format
from heat.tests.common import HeatTestCase

from heat.engine import scheduler
from heat.tests import utils


servicechain_node_template = '''
{
  "AWSTemplateFormatVersion" : "2010-09-09",
  "Description" : "Template to test GBP service chain node",
  "Parameters" : {},
  "Resources" : {
    "servicechain_node": {
      "Type": "OS::GroupBasedPolicy::ServiceChainNode",
      "Properties": {
        "name": "test-sc-node",
        "description": "test service chain node resource",
        "shared": True,
        "service_profile_id": "profile-id",
        "config": "{'name': 'sc_node_config'}"
      }
    }
  }
}
'''

servicechain_spec_template = '''
{
  "AWSTemplateFormatVersion" : "2010-09-09",
  "Description" : "Template to test GBP service chain spec",
  "Parameters" : {},
  "Resources" : {
    "servicechain_spec": {
      "Type": "OS::GroupBasedPolicy::ServiceChainSpec",
      "Properties": {
        "name": "test-sc-spec",
        "description": "test service chain spec resource",
        "shared": True,
        "nodes": ["1234", "7890"]
      }
    }
  }
}
'''

service_profile_template = '''
{
  "AWSTemplateFormatVersion" : "2010-09-09",
  "Description" : "Template to test GBP service profile",
  "Parameters" : {},
  "Resources" : {
    "service_profile": {
      "Type": "OS::GroupBasedPolicy::ServiceProfile",
      "Properties": {
        "name": "test-svc-profile",
        "description": "test service profile resource",
        "vendor": "test vendor",
        "service_type": "test type",
        "insertion_mode": "l2",
        "service_flavor": "test flavor",
        "shared": True
      }
    }
  }
}
'''


class ServiceChainNodeTest(HeatTestCase):

    def setUp(self):
        super(ServiceChainNodeTest, self).setUp()
        self.mock_create = mock.patch(
            'gbpclient.v2_0.client.Client.create_servicechain_node')
        self.mock_delete = mock.patch(
            'gbpclient.v2_0.client.Client.delete_servicechain_node')
        self.mock_show = mock.patch(
            'gbpclient.v2_0.client.Client.show_servicechain_node')
        self.mock_update = mock.patch(
            'gbpclient.v2_0.client.Client.update_servicechain_node')
        self.mock_create.start()
        self.mock_delete.start()
        self.mock_show.start()
        self.mock_update.start()
        self.stub_keystoneclient()

    def tearDown(self):
        self.mock_create.stop()
        self.mock_delete.stop()
        self.mock_show.stop()
        self.mock_update.stop()
        super(ServiceChainNodeTest, self).tearDown()

    def create_servicechain_node(self):
        call_dict = {
            'servicechain_node': {
                "name": "test-sc-node",
                "description": "test service chain node resource",
                "service_profile_id": "profile-id",
                "shared": True,
                "config": "{'name': 'sc_node_config'}"
            }
        }
        tdict = {'servicechain_node': {'id': '5678'}}
        gbpclient.Client.create_servicechain_node.return_value = tdict

        ret_val = gbpclient.Client.create_servicechain_node(call_dict)
        expected = mock.call(call_dict)
        _mocked_create = self.mock_create.get_original()[0]
        _mocked_create.assert_has_calls([expected])
        self.assertEqual(tdict, ret_val)

        snippet = template_format.parse(servicechain_node_template)
        self.stack = utils.parse_stack(snippet)
        resource_defns = self.stack.t.resource_definitions(self.stack)
        return servicechain.ServiceChainNode(
            'servicechain_node', resource_defns['servicechain_node'],
            self.stack)

    def test_create(self):
        rsrc = self.create_servicechain_node()
        scheduler.TaskRunner(rsrc.create)()
        self.assertEqual((rsrc.CREATE, rsrc.COMPLETE), rsrc.state)

    def test_create_failed(self):
        call_dict = {
            'servicechain_node': {
                "name": "test-sc-node",
                "description": "test service chain node resource",
                "service_profile_id": "profile-id",
                "shared": True,
                "config": "{'name': 'sc_node_config'}"
            }
        }
        exc = servicechain.NeutronClientException()
        gbpclient.Client.create_servicechain_node.side_effect = exc

        snippet = template_format.parse(servicechain_node_template)
        self.stack = utils.parse_stack(snippet)
        resource_defns = self.stack.t.resource_definitions(self.stack)
        rsrc = servicechain.ServiceChainNode(
            'servicechain_node', resource_defns['servicechain_node'],
            self.stack)

        error = self.assertRaises(exception.ResourceFailure,
                                  scheduler.TaskRunner(rsrc.create))
        self.assertEqual(
            'NeutronClientException: resources.servicechain_node: '
            'An unknown exception occurred.',
            six.text_type(error))
        self.assertEqual((rsrc.CREATE, rsrc.FAILED), rsrc.state)

        expected = mock.call(call_dict)
        _mocked_create = self.mock_create.get_original()[0]
        _mocked_create.assert_has_calls([expected])

    def test_delete(self):
        exc = servicechain.NeutronClientException(status_code=404)
        gbpclient.Client.show_servicechain_node.side_effect = exc

        rsrc = self.create_servicechain_node()
        scheduler.TaskRunner(rsrc.create)()
        scheduler.TaskRunner(rsrc.delete)()
        self.assertEqual((rsrc.DELETE, rsrc.COMPLETE), rsrc.state)

        expected = mock.call('5678')
        _mocked_show = self.mock_show.get_original()[0]
        _mocked_show.assert_has_calls([expected])

    def test_delete_already_gone(self):
        exc = servicechain.NeutronClientException(status_code=404)
        gbpclient.Client.delete_servicechain_node.side_effect = exc

        rsrc = self.create_servicechain_node()
        scheduler.TaskRunner(rsrc.create)()
        scheduler.TaskRunner(rsrc.delete)()
        self.assertEqual((rsrc.DELETE, rsrc.COMPLETE), rsrc.state)

        expected = mock.call('5678')
        _mocked_delete = self.mock_delete.get_original()[0]
        _mocked_delete.assert_has_calls([expected])

    def test_delete_failed(self):
        exc = servicechain.NeutronClientException(status_code=400)
        gbpclient.Client.delete_servicechain_node.side_effect = exc

        rsrc = self.create_servicechain_node()
        scheduler.TaskRunner(rsrc.create)()
        error = self.assertRaises(exception.ResourceFailure,
                                  scheduler.TaskRunner(rsrc.delete))
        self.assertEqual(
            'NeutronClientException: resources.servicechain_node: '
            'An unknown exception occurred.',
            six.text_type(error))
        self.assertEqual((rsrc.DELETE, rsrc.FAILED), rsrc.state)

        expected = mock.call('5678')
        _mocked_delete = self.mock_delete.get_original()[0]
        _mocked_delete.assert_has_calls([expected])

    def test_update(self):
        rsrc = self.create_servicechain_node()
        call_dict = {'servicechain_node': {'name': 'node_update'}}
        scheduler.TaskRunner(rsrc.create)()

        update_template = copy.deepcopy(rsrc.t)
        update_template._properties['name'] = 'node_update'
        scheduler.TaskRunner(rsrc.update, update_template)()

        expected = mock.call('5678', call_dict)
        _mocked_update = self.mock_update.get_original()[0]
        _mocked_update.assert_has_calls([expected])


class ServiceChainSpecTest(HeatTestCase):

    def setUp(self):
        super(ServiceChainSpecTest, self).setUp()
        self.mock_create = mock.patch(
            'gbpclient.v2_0.client.Client.create_servicechain_spec')
        self.mock_delete = mock.patch(
            'gbpclient.v2_0.client.Client.delete_servicechain_spec')
        self.mock_show = mock.patch(
            'gbpclient.v2_0.client.Client.show_servicechain_spec')
        self.mock_update = mock.patch(
            'gbpclient.v2_0.client.Client.update_servicechain_spec')
        self.mock_create.start()
        self.mock_delete.start()
        self.mock_show.start()
        self.mock_update.start()
        self.stub_keystoneclient()

    def tearDown(self):
        self.mock_create.stop()
        self.mock_delete.stop()
        self.mock_show.stop()
        self.mock_update.stop()
        super(ServiceChainSpecTest, self).tearDown()

    def create_servicechain_spec(self):
        call_dict = {
            "servicechain_spec": {
                "name": "test-sc-spec",
                "description": "test service chain spec resource",
                "shared": True,
                "nodes": ["1234", "7890"]
            }
        }
        tdict = {'servicechain_spec': {'id': '5678'}}
        gbpclient.Client.create_servicechain_spec.return_value = tdict

        ret_val = gbpclient.Client.create_servicechain_spec(call_dict)
        expected = mock.call(call_dict)
        _mocked_create = self.mock_create.get_original()[0]
        _mocked_create.assert_has_calls([expected])
        self.assertEqual(tdict, ret_val)

        snippet = template_format.parse(servicechain_spec_template)
        self.stack = utils.parse_stack(snippet)
        resource_defns = self.stack.t.resource_definitions(self.stack)
        return servicechain.ServiceChainSpec(
            'servicechain_spec', resource_defns['servicechain_spec'],
            self.stack)

    def test_create(self):
        rsrc = self.create_servicechain_spec()
        scheduler.TaskRunner(rsrc.create)()
        self.assertEqual((rsrc.CREATE, rsrc.COMPLETE), rsrc.state)

    def test_create_failed(self):
        call_dict = {
            'servicechain_spec': {
                "name": "test-sc-spec",
                "description": "test service chain spec resource",
                "shared": True,
                "nodes": ["1234", "7890"]
            }
        }
        exc = servicechain.NeutronClientException()
        gbpclient.Client.create_servicechain_spec.side_effect = exc

        snippet = template_format.parse(servicechain_spec_template)
        self.stack = utils.parse_stack(snippet)
        resource_defns = self.stack.t.resource_definitions(self.stack)
        rsrc = servicechain.ServiceChainSpec(
            'servicechain_spec', resource_defns['servicechain_spec'],
            self.stack)

        error = self.assertRaises(exception.ResourceFailure,
                                  scheduler.TaskRunner(rsrc.create))
        self.assertEqual(
            'NeutronClientException: resources.servicechain_spec: '
            'An unknown exception occurred.',
            six.text_type(error))
        self.assertEqual((rsrc.CREATE, rsrc.FAILED), rsrc.state)

        expected = mock.call(call_dict)
        _mocked_create = self.mock_create.get_original()[0]
        _mocked_create.assert_has_calls([expected])

    def test_delete(self):
        exc = servicechain.NeutronClientException(status_code=404)
        gbpclient.Client.show_servicechain_spec.side_effect = exc

        rsrc = self.create_servicechain_spec()
        scheduler.TaskRunner(rsrc.create)()
        scheduler.TaskRunner(rsrc.delete)()
        self.assertEqual((rsrc.DELETE, rsrc.COMPLETE), rsrc.state)

        expected = mock.call('5678')
        _mocked_show = self.mock_show.get_original()[0]
        _mocked_show.assert_has_calls([expected])

    def test_delete_already_gone(self):
        exc = servicechain.NeutronClientException(status_code=404)
        gbpclient.Client.delete_servicechain_spec.side_effect = exc

        rsrc = self.create_servicechain_spec()
        scheduler.TaskRunner(rsrc.create)()
        scheduler.TaskRunner(rsrc.delete)()
        self.assertEqual((rsrc.DELETE, rsrc.COMPLETE), rsrc.state)

        expected = mock.call('5678')
        _mocked_delete = self.mock_delete.get_original()[0]
        _mocked_delete.assert_has_calls([expected])

    def test_delete_failed(self):
        exc = servicechain.NeutronClientException(status_code=400)
        gbpclient.Client.delete_servicechain_spec.side_effect = exc

        rsrc = self.create_servicechain_spec()
        scheduler.TaskRunner(rsrc.create)()
        error = self.assertRaises(exception.ResourceFailure,
                                  scheduler.TaskRunner(rsrc.delete))
        self.assertEqual(
            'NeutronClientException: resources.servicechain_spec: '
            'An unknown exception occurred.',
            six.text_type(error))
        self.assertEqual((rsrc.DELETE, rsrc.FAILED), rsrc.state)

        expected = mock.call('5678')
        _mocked_delete = self.mock_delete.get_original()[0]
        _mocked_delete.assert_has_calls([expected])

    def test_update(self):
        rsrc = self.create_servicechain_spec()
        call_dict = {'servicechain_spec': {'name': 'spec_update'}}
        scheduler.TaskRunner(rsrc.create)()

        update_template = copy.deepcopy(rsrc.t)
        update_template._properties['name'] = 'spec_update'
        scheduler.TaskRunner(rsrc.update, update_template)()

        expected = mock.call('5678', call_dict)
        _mocked_update = self.mock_update.get_original()[0]
        _mocked_update.assert_has_calls([expected])


class ServiceProfileTest(HeatTestCase):

    def setUp(self):
        super(ServiceProfileTest, self).setUp()
        self.mock_create = mock.patch(
            'gbpclient.v2_0.client.Client.create_service_profile')
        self.mock_delete = mock.patch(
            'gbpclient.v2_0.client.Client.delete_service_profile')
        self.mock_show = mock.patch(
            'gbpclient.v2_0.client.Client.show_service_profile')
        self.mock_update = mock.patch(
            'gbpclient.v2_0.client.Client.update_service_profile')
        self.mock_create.start()
        self.mock_delete.start()
        self.mock_show.start()
        self.mock_update.start()
        self.stub_keystoneclient()

    def tearDown(self):
        self.mock_create.stop()
        self.mock_delete.stop()
        self.mock_show.stop()
        self.mock_update.stop()
        super(ServiceProfileTest, self).tearDown()

    def create_service_profile(self):
        call_dict = {
            'service_profile': {
                "name": "test-svc-profile",
                "description": "test service profile resource",
                "vendor": "test vendor",
                "service_type": "test type",
                "insertion_mode": "l2",
                "service_flavor": "test flavor",
                "shared": True
            }
        }
        tdict = {'service_profile': {'id': '5678'}}
        gbpclient.Client.create_service_profile.return_value = tdict

        ret_val = gbpclient.Client.create_service_profile(call_dict)
        expected = mock.call(call_dict)
        _mocked_create = self.mock_create.get_original()[0]
        _mocked_create.assert_has_calls([expected])
        self.assertEqual(tdict, ret_val)

        snippet = template_format.parse(service_profile_template)
        self.stack = utils.parse_stack(snippet)
        resource_defns = self.stack.t.resource_definitions(self.stack)
        return servicechain.ServiceProfile(
            'service_profile', resource_defns['service_profile'], self.stack)

    def test_create(self):
        rsrc = self.create_service_profile()
        scheduler.TaskRunner(rsrc.create)()
        self.assertEqual((rsrc.CREATE, rsrc.COMPLETE), rsrc.state)

    def test_create_failed(self):
        call_dict = {
            'service_profile': {
                "name": "test-svc-profile",
                "description": "test service profile resource",
                "vendor": "test vendor",
                "service_type": "test type",
                "insertion_mode": "l2",
                "service_flavor": "test flavor",
                "shared": True
            }
        }
        exc = servicechain.NeutronClientException()
        gbpclient.Client.create_service_profile.side_effect = exc

        snippet = template_format.parse(service_profile_template)
        self.stack = utils.parse_stack(snippet)
        resource_defns = self.stack.t.resource_definitions(self.stack)
        rsrc = servicechain.ServiceProfile(
            'service_profile', resource_defns['service_profile'],
            self.stack)

        error = self.assertRaises(exception.ResourceFailure,
                                  scheduler.TaskRunner(rsrc.create))
        self.assertEqual(
            'NeutronClientException: resources.service_profile: '
            'An unknown exception occurred.',
            six.text_type(error))
        self.assertEqual((rsrc.CREATE, rsrc.FAILED), rsrc.state)

        expected = mock.call(call_dict)
        _mocked_create = self.mock_create.get_original()[0]
        _mocked_create.assert_has_calls([expected])

    def test_delete(self):
        exc = servicechain.NeutronClientException(status_code=404)
        gbpclient.Client.show_service_profile.side_effect = exc

        rsrc = self.create_service_profile()
        scheduler.TaskRunner(rsrc.create)()
        scheduler.TaskRunner(rsrc.delete)()
        self.assertEqual((rsrc.DELETE, rsrc.COMPLETE), rsrc.state)

        expected = mock.call('5678')
        _mocked_show = self.mock_show.get_original()[0]
        _mocked_show.assert_has_calls([expected])

    def test_delete_already_gone(self):
        exc = servicechain.NeutronClientException(status_code=404)
        gbpclient.Client.delete_service_profile.side_effect = exc

        rsrc = self.create_service_profile()
        scheduler.TaskRunner(rsrc.create)()
        scheduler.TaskRunner(rsrc.delete)()
        self.assertEqual((rsrc.DELETE, rsrc.COMPLETE), rsrc.state)

        expected = mock.call('5678')
        _mocked_delete = self.mock_delete.get_original()[0]
        _mocked_delete.assert_has_calls([expected])

    def test_delete_failed(self):
        exc = servicechain.NeutronClientException(status_code=400)
        gbpclient.Client.delete_service_profile.side_effect = exc

        rsrc = self.create_service_profile()
        scheduler.TaskRunner(rsrc.create)()
        error = self.assertRaises(exception.ResourceFailure,
                                  scheduler.TaskRunner(rsrc.delete))
        self.assertEqual(
            'NeutronClientException: resources.service_profile: '
            'An unknown exception occurred.',
            six.text_type(error))
        self.assertEqual((rsrc.DELETE, rsrc.FAILED), rsrc.state)

        expected = mock.call('5678')
        _mocked_delete = self.mock_delete.get_original()[0]
        _mocked_delete.assert_has_calls([expected])

    def test_update(self):
        rsrc = self.create_service_profile()
        call_dict = {'service_profile': {'name': 'profile_update'}}
        scheduler.TaskRunner(rsrc.create)()

        update_template = copy.deepcopy(rsrc.t)
        update_template._properties['name'] = 'profile_update'
        scheduler.TaskRunner(rsrc.update, update_template)()

        expected = mock.call('5678', call_dict)
        _mocked_update = self.mock_update.get_original()[0]
        _mocked_update.assert_has_calls([expected])
