#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from setuptools import setup

setup(name='singa-easy',
      version='0.4.3',
      description='The SINGA-EASY',
      url='https://github.com/nusdbsystem/singa-easy.git',
      author='Naili',
      author_email='xingnaili14@gmail.com',
      license='Apache',
      packages=["singa_easy"],

      install_requires=[
                        'torch==1.3.1',
                        'torchvision==0.4.2',
                        'matplotlib==3.2.1',
                        'lime==0.2.0.0',
                        'tqdm==4.45.0',
                        'numpy==1.14.5'
                        ],

      include_package_data=True,
      zip_safe=False)
