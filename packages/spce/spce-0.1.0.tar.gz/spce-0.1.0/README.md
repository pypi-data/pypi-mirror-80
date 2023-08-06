# ScalePlan CloudEvents for Python

Unofficial Python implementation for [CloudEvents](https://cloudevents.io/) v1.0.
Check out the [CloudEvents spec](https://github.com/cloudevents/spec/blob/v1.0/spec.md). 

## Install

Requirements:

* Python 3.6 or above

Install using:
    
    pip install spce
    
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

Encode an event in JSON:

```python
from spce import JsonEncoder

encoded_event = JsonEncoder.encode(event)
```

 
## License

(c) 2020 Scale Plan Yazılım A.Ş.

Licensed under [Apache 2.0](LICENSE). See the [LICENSE](LICENSE).

