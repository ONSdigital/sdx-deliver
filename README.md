# sdx-deliver

![Version](https://ons-badges-752336435892.europe-west2.run.app/api/badge/custom?left=Python&right=3.13)

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

### Prerequisites

- Python 3.13
- UV (a command line tool for managing Python environments)
- make

### Installing Python 3.13

If you don't have Python 3.13 installed, you can install it via brew:

```bash
brew install python@3.13
```

### Install UV:
   - This project uses UV for dependency management. Ensure it is installed on your system.
   - If UV is not installed, you can install it using:
```bash

curl -LsSf https://astral.sh/uv/install.sh | sh

OR 

brew install uv
```
- Use the official UV installation guide for other installation methods: https://docs.astral.sh/uv/getting-started/installation/
- Verify the installation by using the following command:
```bash
uv --version
```

### Install dependencies

This command will install all the dependencies required for the project, including development dependencies:

```bash
uv sync
```

If you ever need to update the dependencies, you can run:

```bash
uv sync --upgrade
```

## Running the service

```bash
uv run run.py
```

## Linting

```bash
make lint
```

## Formatting

```bash
make format
```

## Tests

```bash
make test
```

## GCP

### PubSub

Once a submission has been successfully encrypted and stored in the Bucket. A message is published to the `dap-topic`.

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
The gpg key used to encrypt JSON surveys: `dap-public-gpg` is managed by Google Secret Manager.
The location names of various servers are also stored as secrets.
They are currently:
* nifi-location-ftp
* nifi-location-spp
* nifi-location-dap
* nifi-location-cdp
* nifi-location-ns5
* nifi-location-dap


## API endpoints

Allows Survey, SEFT and Collate to send data to be stored by deliver

* `POST /deliver/v2/survey` - Processes any survey type that originated from eQ-runner including legacy, spp, adhoc, feedback etc

* `POST /deliver/v2/coments` - Processes the comments zip

* `POST /deliver/v2/seft` - Processes SEFT submissions


## License

Copyright © 2016, Office for National Statistics (https://www.ons.gov.uk)

Released under MIT license, see [LICENSE](LICENSE) for details.
