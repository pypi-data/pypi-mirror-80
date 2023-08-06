# PyUnleashed

PyUnleashed is a Python library for interacting with the Unleashed Software (www.unleashedsoftware.com) API in a Pythonic manner.  This is a work in progress

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyUnleashed.

```bash
pip install pyunleashed
```

Then install the requests library if it isn't already.

```bash
pip install requests
```

## Usage

```python
from PyUnleashed import API

unlapi =  API(
            url = 'https://api.unleashedsoftware.com/',
            api_id = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
)


# GET a product
r = unlapi.get("Products", ProductCode="TESTSKU")

# You can also optionally include filters as additional arguments for example
r = unlapi.get("Products", includeAttributes="True", pageSize=5)

# Some results could need pagination and you can request using
r = unlapi.get("Products", includeAttributes="True", pageSize=5)
string_r = json.dumps(r)
json_r = json.loads(string_r)

# Total items, pages etc are available
print(json_r['Pagination']['NumberOfItems'])
print(json_r['Pagination']['NumberOfPages'])
print(json_r['Pagination']['PageNumber'])
print(json_r['Pagination']['PageSize'])

# POST a product (remember to include the uuid in the URL, in this case it's the order number, data_payload is a valid Python dict)
r = unlapi.post("SalesOrders/{0}".format(order_number), data=data_payload)

# There are also two help functions to convert between date formats

# Create a Python datetime from UNL date string
print(unlapi.dateFromUnl('/Date(1550573963258)/'))

# Create a timestamp from datetime either leave blank for now or enter your own date
print(unlapi.dateToUnl())

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
