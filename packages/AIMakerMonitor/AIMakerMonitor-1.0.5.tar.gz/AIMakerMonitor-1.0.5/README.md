## About upload to lib pypi

1. The account and password was saved in .pypic.
2. Please update lib version in setup.py before upload to pypi.
3. Please do not upload unnessary file (ex: egg.info, pycache...etc).
4. `Web` : <https://pypi.org/project/AIMakerMonitor/>

## If this is the first time to upload, please execute the following
Please copy .pypic to your home directory.

`$ cp .pypic ~`

Register account info.

`$ python setup.py register -r pypi`

## Upload lib to pypi
In current directory use the following command:

`$ python setup.py sdist upload -r pypi`


## Usage
`$ pip install AIMakerMonitor`

```python
import AIMakerMonitor as aim
aim.api_count_inc()
aim.counter_inc(chartName, labelName)
aim.gauge_set(chartName, labelName, score)
```