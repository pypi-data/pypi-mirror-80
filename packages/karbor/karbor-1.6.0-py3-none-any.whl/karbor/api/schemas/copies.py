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

"""
Schema for Karbor V1 Copies API.

"""

from karbor.api.validation import parameter_types


create = {
    'type': 'object',
    'properties': {
        'type': 'object',
        'copy': {
            'type': 'object',
            'properties': {
                'plan_id': parameter_types.uuid,
                'parameters': parameter_types.parameters,
            },
            'required': ['plan_id'],
            'additionalProperties': False,
        },
    },
    'required': ['copy'],
    'additionalProperties': False,
}
