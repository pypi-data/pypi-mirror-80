###############################################################################
# Copyright 2020 ScPA StarLine Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

import setuptools

with open("README.md", "r") as file_with_description:
    long_description = file_with_description.read()

with open('requirements.txt') as file_with_requirements:
    requirements = file_with_requirements.read().splitlines()

setuptools.setup(
    name="oscar_vehicle_api",
    version="1.0b1",
    author="Nikolay Dema",
    author_email="ndema2301@gmail.com",
    description="OSCAR Vehicle API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords = ['oscar', 'vehicle', 'api'],
    url="https://gitlab.com/starline/oscar_vehicle_api",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
)
