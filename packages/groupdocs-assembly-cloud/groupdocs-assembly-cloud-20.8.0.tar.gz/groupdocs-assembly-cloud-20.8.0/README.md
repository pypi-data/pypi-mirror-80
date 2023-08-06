This repository contains GroupDocs.Assembly Cloud SDK for Python source code. This SDK allows you to work with GroupDocs.Assembly Cloud REST APIs in your Python applications quickly and easily, with zero initial cost.

See [API Reference](https://apireference.groupdocs.cloud/) for full API specification.

## How to use the SDK?
The complete source code is available in this repository folder. You can either directly use it in your project via source code or get [PyPi](https://pypi.org/project/groupdocsassemblycloud) (recommended). For more details, please visit our [documentation website](https://docs.groupdocs.cloud/display/assemblycloud/Available+SDKs).

### Prerequisites

To use GroupDocs.Assembly for Cloud Python SDK you need to register an account with [GroupDocs Cloud](https://www.groupdocs.cloud/) and lookup/create App Key and SID at [Cloud Dashboard](https://dashboard.groupdocs.cloud/#/apps). There is free quota available. For more details, see [GroupDocs Cloud Pricing](https://purchase.groupdocs.cloud/pricing).

### Installation
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install groupdocsassemblycloud
```
(you may need to run `pip` with root permission: `sudo pip install groupdocsassemblycloud`)

Then import the package:
```python
import groupdocsassemblycloud
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import groupdocsassemblycloud
```

### Sample usage
```python
import groupdocsassemblycloud
import groupdocsassemblycloud.models.requests
api_client = groupdocsassemblycloud.ApiClient()
api_client.configuration.host = 'https://api.groupdocs.cloud'
api_client.configuration.api_key['api_key'] = '' # Put your appKey here
api_client.configuration.api_key['app_sid'] = '' # Put your appSid here
storage_api = asposestoragecloud.StorageApi(asposestoragecloud.ApiClient('', '')) # Same credentials for storage
storage_api.api_client.configuration.base_url = 'https://api.groupdocs.cloud/v1.1'
assembly_api = groupdocsassemblycloud.AssemblyApi(api_client)

with open(os.path.join(self.local_test_folder, filename), 'rb') as f:
    file = f.read()
self.storage_api.put_create(os.path.join(self.remote_test_folder, self.test_folder, remote_name), file)

request = groupdocsassemblycloud.models.requests.PostAssembleDocumentRequest(remote_name, os.path.join(self.local_test_folder, "Teams.json"), groupdocsassemblycloud.LoadSaveOptionsData('docx'), os.path.join(self.remote_test_folder, self.test_folder),)
result = self.assembly_api.post_assemble_document(request)
self.assertTrue(len(result) > 0, 'Error has occurred while building document')
```
      
[Tests](tests/) contain various examples of using the SDK.
Please put your credentials into [Configuration](Settings/servercreds.json).

# Dependencies
- Python 2.7 and 3.4+
- referenced packages (see [here](setup.py) for more details)

## Contact Us
Your feedback is very important to us. Please feel free to contact us using our [Support Forums](https://forum.groupdocs.cloud/c/words).
