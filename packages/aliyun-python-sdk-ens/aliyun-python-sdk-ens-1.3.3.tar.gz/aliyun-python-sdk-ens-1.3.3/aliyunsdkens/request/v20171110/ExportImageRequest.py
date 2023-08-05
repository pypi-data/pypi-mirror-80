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

class ExportImageRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Ens', '2017-11-10', 'ExportImage','ens')
		self.set_method('POST')

	def get_ImageId(self):
		return self.get_query_params().get('ImageId')

	def set_ImageId(self,ImageId):
		self.add_query_param('ImageId',ImageId)

	def get_OSSRegionId(self):
		return self.get_query_params().get('OSSRegionId')

	def set_OSSRegionId(self,OSSRegionId):
		self.add_query_param('OSSRegionId',OSSRegionId)

	def get_OSSBucket(self):
		return self.get_query_params().get('OSSBucket')

	def set_OSSBucket(self,OSSBucket):
		self.add_query_param('OSSBucket',OSSBucket)

	def get_RoleName(self):
		return self.get_query_params().get('RoleName')

	def set_RoleName(self,RoleName):
		self.add_query_param('RoleName',RoleName)

	def get_Version(self):
		return self.get_query_params().get('Version')

	def set_Version(self,Version):
		self.add_query_param('Version',Version)

	def get_OSSPrefix(self):
		return self.get_query_params().get('OSSPrefix')

	def set_OSSPrefix(self,OSSPrefix):
		self.add_query_param('OSSPrefix',OSSPrefix)