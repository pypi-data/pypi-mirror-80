[![PyPI version](https://badge.fury.io/py/playment.svg)](https://badge.fury.io/py/playment)
## Installation
You don't need this source code unless you want to modify the package. If you just want to use the package, just run:

```
pip install --upgrade playment
```

Install from source with:

```
python setup.py install
```

Requirements:

```
Python 3.5+
```

## Documentation
Please visit the [Docs](https://docs.playment.io) to know more about Playment APIs.

## Using x-client-key [Deprecated]
* Using `x-client-key` is only supported till 30th October 2020, please use updated sdk and `x-api-key` to use Playment APIs after the aforementioned date.
* `x-api-key` is supported in latest SDK versions > 1.0.4 


#### X-Client-Key Usage instructions
Uninstall the sdk (Only required if you upgraded to sdk version > 1.0.4, run ` pip show playment` to check).
```
pip uninstall playment
``` 

Install the latest version supporting `x-client-key`
```
pip install -Iv playment==1.0.4
```

Pass your `x-client-key` as shown below, and use as demonstrated in further examples. 
```
import playment
client = playment.Client(client_key="your-x-client-key-here")
```
Please reach out to [dev@playment.in](mailto:dev.playment.io) if you face any issues.


## Usage
```
import playment
client = playment.Client(api_key="your-x-api-key-here")
```
It is a secret key required to call Playment APIs. The secret x-api-key ensures that only you are able to access your projects.
The x-api-key can be accessed from the ***Settings*** -> ***API Keys*** in your Playment Dashboard.

#### Usage Instructions



#### [Summary](https://github.com/crowdflux/playment-sdk-python/blob/master/examples/summary.py)
* Project Overview
* Batch Summary
* Project's batches Summary


#### Creating a [Batch](https://github.com/crowdflux/playment-sdk-python/blob/master/examples/batch_creation.py)
* Consist collection of jobs with similar characteristics.


#### Creating a Single-Image Based [Job](https://github.com/crowdflux/playment-sdk-python/blob/master/examples/image_job_creation.py).
* A single image based job can be used for classification/annotation/segmentation.


#### Creating a Sensor Based Job with Multiple Images with only camera sensor or multiple image based [Job](https://github.com/crowdflux/playment-sdk-python/blob/master/examples/video_job_creation.py).
* A multiple image based job can be used for classification/annotation, where all the images of the job are from a single camera and objects are needed to be tracked.


#### Creating a Sensor Based Job with Multiple Images/PCDs or Sensor Fusion [Job](https://github.com/crowdflux/playment-sdk-python/blob/master/examples/sensor_job_creation.py).
* This can also be used for only LiDAR based jobs.

#### Creating a [Job with metadata](https://github.com/crowdflux/playment-sdk-python/blob/master/examples/job_creation_with_metadata.py).
* metadata: You can send any type of data in metadata which can be useful in the task or record of any other data related to               that job. metadata should be a type `dict`.


#### Get [Job Result](https://github.com/crowdflux/playment-sdk-python/blob/master/examples/job_result.py).
* Job result will only populate if the job is completed else it will be empty.


#### Create Jobs with High Priority and associating them with a batch.
```
image_url = "https://example.com/image_url"
image_data = playment.ImageData(image_url=image_url)

try:
    job = client.create_job(reference_id="55", tag='image',
                            data=image_data, project_id="project_id",
                            priority_weight=10, batch_id="batch_id")
except playment.PlaymentException as e:
    print(e.code, e.message, e.data)
```
