# AWS Lambda Layer with Pandas

* Python 3.6
* pandas
* s3fs
* fsspec

You can download the [provided zip](pandas_layer.zip) or run the following commands to create your own:

````bash
source ./v-env/bin/activate
pip install pandas
pip install fsspec
pip install s3fs
deactivate
mkdir python
cd python
````

Run the following command based on your python version
````bash
cp -r ../v-env/lib64/python3.6/dist-packages/* .
zip -r panda_layer.zip python
````

To use pandas on your Lambda function:
````python
import pandas as pd
df = pd.read_csv('s3://bucket...')
df.to_csv('s3://bucket...')
````