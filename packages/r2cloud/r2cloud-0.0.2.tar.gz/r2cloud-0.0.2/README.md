## About
r2cloud python sdk makes it easier for you to work with your r2cloud server using the python programming language. The SDK uses an object-oriented design and tries to look like r2cloud API.

## Installation 

#### with pip3

```sh
pip install r2cloud
```

#### from repo

```sh
make install
make doc # for generate documentation
```

## Quick start

```python
import r2cloud.api
import r2cloud.tools.common

# init api
station = r2cloud.api('https://192.168.0.10')
# login to r2cloud
station.login("myemail@example.org", "my_password")

# get all observations
obs = station.observationList()

# filter observation of "NOAA 19", "NOAA 18" and "NOAA 15"
obs = r2cloud.tools.common.filterSat(obs, ["NOAA 19", "NOAA 18", "NOAA 15"])

# filter observation with data only
obs = r2cloud.tools.common.filterHasData(obs)

# print all filtred observations ids
for ob in obs:
    print("Observation " + str(ob.id) + " by " + ob.name)

```

more examples you can find in `/examples` dir on github

## Examples Screenshots

<img src="https://raw.githubusercontent.com/Lukas0025/r2cloud-python-sdk/master/examples_images/Figure_1.png" width="30%">&nbsp;<img src="https://raw.githubusercontent.com/Lukas0025/r2cloud-python-sdk/master/examples_images/Figure_2.png" width="30%">&nbsp;<img src="https://raw.githubusercontent.com/Lukas0025/r2cloud-python-sdk/master/examples_images/Figure_3.png" width="30%">&nbsp;<img src="https://raw.githubusercontent.com/Lukas0025/r2cloud-python-sdk/master/examples_images/Figure_4.png" width="30%">&nbsp;<img src="https://raw.githubusercontent.com/Lukas0025/r2cloud-python-sdk/master/examples_images/Figure_5.jpg" width="30%">
