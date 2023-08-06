# Copyright 2020 Scale Plan Yazılım A.Ş.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Union

__all__ = "CloudEvent",


class CloudEvent:

    __slots__ = "_attributes", "_has_binary_data"

    def __init__(self, *,
                 type: str,
                 source: str,
                 id: str,
                 specversion="1.0",
                 subject: Union[str, None] = None,
                 data: Union[str, bytes, None] = None,
                 datacontenttype: Union[str, None] = None,
                 dataschema: Union[str, None] = None,
                 time: Union[str, None] = None,
                 **attributes
                 ):
        self._attributes = {
            "type": type,
            "source": source,
            "id": id,
            "specversion": specversion,
            "subject": subject,
            "data": data,
            "datacontenttype": datacontenttype,
            "dataschema": dataschema,
            "time": time,
        }

        # TODO: validation

        self._attributes.update(attributes)
        self._has_binary_data = isinstance(data, bytes)

    type = property(lambda self: self._attributes.get("type"))
    source = property(lambda self: self._attributes.get("source"))
    id = property(lambda self: self._attributes.get("id"))
    specversion = property(lambda self: self._attributes.get("specversion"))
    data = property(lambda self: self._attributes.get("data"))
    datacontenttype = property(lambda self: self._attributes.get("datacontenttype"))
    dataschema = property(lambda self: self._attributes.get("dataschema"))
    subject = property(lambda self: self._attributes.get("subject"))
    time = property(lambda self: self._attributes.get("time"))

    def attribute(self, name):
        return self._attributes.get(name)

    def __str__(self):
        return str(self._attributes)

    def __repr__(self):
        return repr(self._attributes)

    def __eq__(self, other):
        if not isinstance(other, CloudEvent):
            return False
        return self._attributes.__eq__(other._attributes)

    def __hash__(self):
        return hash(self._attributes)