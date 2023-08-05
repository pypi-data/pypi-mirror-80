# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest

class CreateVSwitchRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ens', '2017-11-10', 'CreateVSwitch','ens')
		self.set_method('POST')

	def get_EnsRegionId(self):
		return self.get_query_params().get('EnsRegionId')

	def set_EnsRegionId(self,EnsRegionId):
		self.add_query_param('EnsRegionId',EnsRegionId)

	def get_Version(self):
		return self.get_query_params().get('Version')

	def set_Version(self,Version):
		self.add_query_param('Version',Version)

	def get_VSwitchName(self):
		return self.get_query_params().get('VSwitchName')

	def set_VSwitchName(self,VSwitchName):
		self.add_query_param('VSwitchName',VSwitchName)

	def get_CidrBlock(self):
		return self.get_query_params().get('CidrBlock')

	def set_CidrBlock(self,CidrBlock):
		self.add_query_param('CidrBlock',CidrBlock)