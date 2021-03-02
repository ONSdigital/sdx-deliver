# sdx-deliver

The SDX-Deliver service is responsible for encrypting and storing all data processed by SDX and notifying DAP of its 
location and metadata.

## Process

The sdx-deliver is flask application made up of **five** endpoints. As a request is made to the service, metadata 
is extracted and the data is then stored within the google bucket. The metadata is used to 
construct a PubSub message to: `dap-topic` to notify DAP that a new submission is in the bucket.
#####NOTE:
deliver runs within the kubernetes cluster and utilises a `kubernetes service`.This assigns the service with an IP 
address and DNS name exposing it to the other services.

## Getting started
Install requirements:
```shell
$ make build
```

**Testing**:
ensure you have installed all requirements with above `make build` command then:
```shell
$ make test
```

**Running**:
ensure you have installed all requirements with above `make build` command then:
```shell
$ make start
```

## GCP

#### PubSub

Once a submission has been successfully encrypted and stored in the Bucket. A message is published to the `dap-topic`.
Message attributes specify location and name of the data.

**Message Structure Example:**
```python
dap_message: Message {
  data: b'{"version": "1", "files": [{"name": "087bfc03-8698...'
  ordering_key: ''
  attributes: {
    "gcs.bucket": "ons-sdx-sandbox-outputs",
    "gcs.key": "dap/087bfc03-8698-4137-a3ac-7a596b9beb2b",
    "tx_id": "087bfc03-8698-4137-a3ac-7a596b9beb2b"
  }
}
```
**Message Data field Example:**
```python
    data : {
        'version': '1',
        'files': [{
            'name': meta_data.filename,
            'sizeBytes': meta_data.sizeBytes,
            'md5sum': meta_data.md5sum
        }],
        'sensitivity': 'High',
        'sourceName': CONFIG.PROJECT_ID,
        'manifestCreated': get_formatted_current_utc(),
        'description': meta_data.get_description(),
        'dataset': dataset,
        'schemaversion': '1'
    }
```

#### Google Storage

All submissions are stored within: `ons-sdx-{project_id}-outputs` in their respective folders. The file-path is
specified in `attributes."gcs.key"`.

## API endpoints

Allows Survey, SEFT and Collate to send data to be stored by deliver

#### 
* `POST /deliver/dap` - Dap surveys

* `POST /deliver/legacy` - Legacy surveys

* `POST /deliver/feedback` - Feedback submissions

* `POST /deliver/comments` - comments endpoint called by sdx-collate

* `POST /deliver/seft` - seft endpoint called by sdx-seft

## Configuration
| Environment Variable    | Description
|-------------------------|------------------------------------
| PROJECT_ID              | Name of project
| BUCKET_NAME             | Name of the bucket: `ons-sdx-{project_id}-outputs`
| BUCKET                  | Bucket client to GCP
| DAP_TOPIC_PATH          | Name of the dap topic: `dap-topic`
| DAP_PUBLISHER           | PubSub publisher client to GCP
| ENCRYPTION_KEY          | Key to encrypt all data
| GPG                     | System GPG key import

## License

Copyright © 2016, Office for National Statistics (https://www.ons.gov.uk)

Released under MIT license, see [LICENSE](LICENSE) for details.
