# ScalePlan CloudEvents for Python

Unofficial Python implementation for [CloudEvents](https://cloudevents.io/) v1.0.
Check out the [CloudEvents spec](https://github.com/cloudevents/spec/blob/v1.0/spec.md).

This package has no dependencies beyond the Python standard library with the base install.
Optionally depends on the `avro` package for Avro encode/decode functionality. 

## Install

Requirements:

* Python 3.6 or above

Install with JSON codec:
    
    pip install spce
    
Install with JSON and Avro codecs:

    pip install spce[avro]
    
## Usage:

Create a CloudEvent with required attributes:

```python
from spce import CloudEvent

event = CloudEvent(
    type="OximeterMeasured",
    source="oximeter/123",
    id="1000"
)
```

Create a CloudEvent with optional attributes:

```python
event = CloudEvent(
    type="OximeterMeasured",
    source="oximeter/123",
    id="1000",
    subject="subject1",
    dataschema="https://particlemetrics.com/schema",
    time="2020-09-28T21:33:21Z",
    data='{\"spo2\": 99})',
    datacontenttype="application/json"
)
```

Required and optional attributes can be directly accessed:

```python
assert event.type == "OximeterMeasured" 
assert event.subject == "subject1" 
```

Create a CloudEvent with extension attributes:

```python
event = CloudEvent(
    type="OximeterMeasured",
    source="oximeter/123",
    id="1000",
    external1="foo/bar"
)
```

Extension attributes can be accessed using the `attribute` method:

```python
assert event.attribute("external1") == "foo/bar" 
```

Encode an event in JSON:

```python
from spce import Json

encoded_event = Json.encode(event)
```

Decode an event in JSON:

```python
from spce import Json

text = """
    {
      "type": "OximeterMeasured",
      "source": "oximeter/123",
      "id": "1000",
      "specversion": "1.0",
      "datacontenttype": "application/json",
      "subject": "subject1",
      "dataschema": "https://particlemetrics.com/schema",
      "time": "2020-09-28T21:33:21Z",
      "data": "{\"spo2\": 99})"
    }
"""
decoded_event = Json.decode(text) 
```

Encode an event in Avro:

```python
from spce import Avro

encoded_event = Avro.encode(event)
```

Decode an event in Avro:

```python
from spce import Avro

text = """
    {
      "type": "OximeterMeasured",
      "source": "oximeter/123",
      "id": "1000",
      "specversion": "1.0",
      "datacontenttype": "application/json",
      "subject": "subject1",
      "dataschema": "https://particlemetrics.com/schema",
      "time": "2020-09-28T21:33:21Z",
      "data": "{\"spo2\": 99})"
    }
"""
decoded_event = Avro.decode(text) 
```

## License

(c) 2020 Scale Plan Yazılım A.Ş.

Licensed under [Apache 2.0](LICENSE). See the [LICENSE](LICENSE).

