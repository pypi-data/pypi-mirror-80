# Copyright 2019 Intel, Inc.
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

from cyborg_tempest_plugin.services import cyborg_data
from cyborg_tempest_plugin.tests.api import base


class TestDeviceProfileController(base.BaseAPITest):

    credentials = ['admin']

    def test_create_device_profile(self):
        dp = cyborg_data.NORMAL_DEVICE_PROFILE_DATA1
        response = self.os_admin.cyborg_client.create_device_profile(dp)
        self.assertEqual(dp[0]['name'], response['name'])
        self.addCleanup(self.os_admin.cyborg_client.delete_device_profile,
                        dp[0]['name'])

    @classmethod
    def resource_cleanup(cls):
        super(TestDeviceProfileController, cls).resource_cleanup()
