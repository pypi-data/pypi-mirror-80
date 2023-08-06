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

import json
from base64 import b64encode, b64decode

from .cloudevents import CloudEvent

__all__ = "Encoder", "Decoder"


class _JsonEncoder:

    ATTRIBUTES = [
        "type", "source", "id", "specversion", # required attributes
        "datacontenttype", "subject",  # optional attributes, note that 'data' is missing
        "dataschema", "time"
    ]

    def __init__(self):
        self.encoder = json.JSONEncoder()

    def encode(self, event: CloudEvent):
        kvs = []
        event_attrs = event._attributes
        encoder = self.encoder
        for attr in _JsonEncoder.ATTRIBUTES:
            value = event_attrs.get(attr)
            if value is not None:
                kvs.append('"%s":%s' % (attr, encoder.encode(value)))
        data = event_attrs.get("data")
        if data is not None:
            if event._has_binary_data:
                kvs.append('"data_b64":%s'% encoder.encode(b64encode(data).decode()))
            else:
                kvs.append('"data":%s'% encoder.encode(data))
        return "{%s}" % ",".join(kvs)


class _JsonDecoder:

    def decode(self, text: str) -> CloudEvent:
        d = json.loads(text)
        if "data_b64" in d:
            d["data"] = b64decode(d["data_b64"])
            del d["data_b64"]

        return CloudEvent(**d)


Encoder = _JsonEncoder()
Decoder = _JsonDecoder()