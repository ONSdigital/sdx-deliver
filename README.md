# sdx-deliver

The SDX-Deliver service is responsible for ensuring that all SDX outputs are delivered to ONS via NIFI. This is done by
encrypting and storing data into a GCP Bucket, and then sending a message via Pub/Sub to Nifi. 
The message is in 2 different formats. Version 1 contains identifiers (such as ftp or hybrid) that Nifi
use to work out the appropriate route. For Version 2 the message defines all source and target locations explicitly
allowing SDX to be fully in control of where the files are sent.


## Implementation

SDX-Deliver is implemented as a Python microservice with endpoints for each submission type.
The process involves encrypting the files using GPG and writing them to the bucket: `ons-sdx-{project_id}-outputs`.
It then publishes a message to the Pub/sub topic with name `dap-topic` to notify Nifi that a new submission is in the bucket.
##### note:
**SEFT** submissions are already encrypted as they come through SDX and therefore require no additional encryption 
before being stored

## Getting started

Create the virtual environment:
```shell
$ python3 -m venv venv
```

Activate the virtual environment:
```shell
$ . venv/bin/activate
```

Install and Update pip
```shell
$ python3 -m pip install --upgrade pip
```

Pull the dependencies:
```shell
$ pip install -r requirements.txt
```

Pull the test dependencies:
```shell
$ pip install -r test-requirements.txt
```

Run the code:
```shell
$ python3 -m run.py
```

## GCP

### PubSub

Once a submission has been successfully encrypted and stored in the Bucket. A message is published to the `dap-topic`.

**Message Structure Example:**
```python
dap_message: Message {
  data: b'{"version": "1", "files": [{"name": "087bfc03-8698...'
  ordering_key: ''
  attributes: {
    "gcs.bucket": "ons-sdx-sandbox-outputs",
    "gcs.key": "dap|087bfc03-8698-4137-a3ac-7a596b9beb2b",
    "tx_id": "087bfc03-8698-4137-a3ac-7a596b9beb2b"
  }
}
```
**Message Data field for Version 1:**
```python
    data : {
        'version': '1',
        'files': [{
            'name': '4f1c130a-0681-442f-8195-b5fa6c57e469:ftp',
            'sizeBytes': 121144,
            'md5sum': 'be08e1e407c79507a17d1e6dcdada055'
        }],
        'sensitivity': 'High',
        'sourceName': 'ons-sdx-sandbox',
        'manifestCreated': '2021-06-16T07:47:45.481Z',
        'description': '009 survey response for period 1704 sample unit 49900108249D',
        'dataset': '009',
        'schemaversion': '1',
        'iterationL1': '1704'
    }
```

**Message Data field for Version 2:**
```python
    data : {
        "schema_version": "2",
        "sensitivity": "Low",
        "sizeBytes": 2691342,
        "md5sum": "f6e217c6f99dcf79ce54937f766f20f9",
        "context": {
          "survey_id": "141",
          "period_id": "202501",
          "ru_ref": "14100000135A"
        },
        "source": {
          "location_type": "gcs",
          "location_name": "ons-sdx-preprod-outputs",
          "path": "seft",
          "filename": "14100000135_202501_141_20250123072928.xlsx.gpg"
        },
        "actions": ["decrypt"],
        "targets": [
          {
            "input": "14100000135_202501_141_20250123072928.xlsx",
            "outputs": [
              {
                "location_type": "windows_server",
                "location_name": "NP123456",
                "path": "SDX_PREPROD/EDC_Submissions/141",
                "filename": "14100000135_202501_141_20250123072928.xlsx"
              }
            ]
          }
        ]
    },
```

### Google Storage

All submissions are stored within: `ons-sdx-{project_id}-outputs` in their respective folders.

### Secret Manager
The gpg key used to encrypt JSON surveys: `dap-public-gpg` is managed by Google Secret Manager. A single API call is 
made on program startup and stored in `ENCRYPTION_KEY`.
The location names of various servers are also stored as secrets.
They are currently:
* nifi-location-ftp
* nifi-location-spp
* nifi-location-dap


## API endpoints

Allows Survey, SEFT and Collate to send data to be stored by deliver


* `POST /deliver/dap` - Processes JSON surveys destined for DAP

* `POST /deliver/legacy` - Processes JSON surveys destined for Legacy downstream

* `POST /deliver/feedback` - Processes JSON Feedback submissions

* `POST /deliver/comments` - Processes zipped spreadsheet (.xls) of comments

* `POST /deliver/seft` - Processes SEFT submissions

* `POST /deliver/spp` - Processes submissions destined for SPP

* `POST /deliver/hybrid` - Processes submissions destined that require specific routing in Nifi (Version 1 only)


## License

Copyright © 2016, Office for National Statistics (https://www.ons.gov.uk)

Released under MIT license, see [LICENSE](LICENSE) for details.
