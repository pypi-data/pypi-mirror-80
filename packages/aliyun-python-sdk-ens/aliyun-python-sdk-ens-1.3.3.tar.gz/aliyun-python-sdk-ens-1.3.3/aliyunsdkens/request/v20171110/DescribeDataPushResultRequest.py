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

class DescribeDataPushResultRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ens', '2017-11-10', 'DescribeDataPushResult','ens')
		self.set_method('POST')

	def get_MaxDate(self):
		return self.get_query_params().get('MaxDate')

	def set_MaxDate(self,MaxDate):
		self.add_query_param('MaxDate',MaxDate)

	def get_PageNumber(self):
		return self.get_query_params().get('PageNumber')

	def set_PageNumber(self,PageNumber):
		self.add_query_param('PageNumber',PageNumber)

	def get_PageSize(self):
		return self.get_query_params().get('PageSize')

	def set_PageSize(self,PageSize):
		self.add_query_param('PageSize',PageSize)

	def get_RegionIds(self):
		return self.get_query_params().get('RegionIds')

	def set_RegionIds(self,RegionIds):
		self.add_query_param('RegionIds',RegionIds)

	def get_MinDate(self):
		return self.get_query_params().get('MinDate')

	def set_MinDate(self,MinDate):
		self.add_query_param('MinDate',MinDate)

	def get_DataVersions(self):
		return self.get_query_params().get('DataVersions')

	def set_DataVersions(self,DataVersions):
		self.add_query_param('DataVersions',DataVersions)

	def get_AppId(self):
		return self.get_query_params().get('AppId')

	def set_AppId(self,AppId):
		self.add_query_param('AppId',AppId)

	def get_DataNames(self):
		return self.get_query_params().get('DataNames')

	def set_DataNames(self,DataNames):
		self.add_query_param('DataNames',DataNames)