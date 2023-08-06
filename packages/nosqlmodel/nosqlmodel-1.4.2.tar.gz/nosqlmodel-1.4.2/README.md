# NoSQLModel

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nosqlmodel)](https://img.shields.io/pypi/pyversions/nosqlmodel)
[![PyPI - License](https://img.shields.io/pypi/l/nosqlmodel)](https://img.shields.io/pypi/l/nosqlmodel)
[![PyPI version](https://img.shields.io/pypi/v/nosqlmodel)](https://pypi.org/project/nosqlmodel/)
[![PyPI - Downloads](https://pepy.tech/badge/nosqlmodel)](https://pepy.tech/project/nosqlmodel)
[![pipeline status](https://gitlab.com/mozgurbayhan/nosqlmodel/badges/master/pipeline.svg)](https://gitlab.com/mozgurbayhan/nosqlmodel/commits/master)
[![pylint status](https://gitlab.com/mozgurbayhan/nosqlmodel/-/jobs/artifacts/master/raw/pylint/pylint.svg?job=pylint)](https://gitlab.com/mozgurbayhan/nosqlmodel/commits/master)
[![coverage report](https://gitlab.com/mozgurbayhan/nosqlmodel/badges/master/coverage.svg)](https://gitlab.com/mozgurbayhan/nosqlmodel/commits/master)


***

# Defination

nosqlmodel is a first non-relational NoSql ORM framework. Easy way to create models with a nosql backend. 

Our Motto is simple :

***Speed, Speed Speed!***

So there is unneccesarry relations, object convertions, heavy queries are out of our scope!

Currently Redis and Dynamodb supported.


[https://gitlab.com/mozgurbayhan/nosqlmodel/blob/master/CHANGELOG](https://gitlab.com/mozgurbayhan/nosqlmodel/blob/master/CHANGELOG)

# Help Us

We need contrbutors to add MemCache and MongoDB backends! 

Feel free to send us pull requests about them or any contributions about our N-ORM. 

We will grow together.

PS: Please vote up our project in [https://github.com/vinta/awesome-python/pull/1448](https://github.com/vinta/awesome-python/pull/1448) if you like (:


# Tutorial

## Declaration and Configuration

nosqlmodel declaration is simple class declaration. 

Dont forget to extend **BaseNosqlModel** and **Meta** declaration

**WARNING:** All declared fields must return false in if check. Possible values: *False* , *0* , *None* , *""* , *[]*, *{}* or `save_to_cache(compress=False)` must take compress=False. Otherwise it will cause a problem in stripping False values in compressed save.


```python
from nosqlmodel.basenosql import BaseNoSqlModel
from nosqlmodel.connectors import dynamoconnector
from nosqlmodel.connectors import redisconnector
from nosqlmodel.connectors.redisconnector import RedisConnector

# Configuration

redisconnector.RHOST = REDIS_HOST
redisconnector.RPORT = REDIS_PORT
dynamoconnector.D_AWS_ACCESS_KEY_ID = DYNAMO_AWS_ACCESS_KEY_ID
dynamoconnector.D_AWS_SECRET_ACCESS_KEY = DYNAMO_AWS_SECRET_ACCESS_KEY
dynamoconnector.D_REGION_NAME = DYNAMO_REGION_NAME

# Declaration

class TestCar(BaseNoSqlModel):
    def __init__(self):
        super().__init__()
        self.plate_number = ""
        self.top_speed = 0
        self.z_to_h = 0

    class Meta:
        # connector = DynamoConnector("Test") # Or you can us a redis connector too:
        connector = RedisConnector(0) # 0 is dbnum
        # or you can set table source to a different redis db
        # connector = RedisConnector(0,"192.168.1.1",6666)
        # think that as a primary key, index key is one of the keys which declared in class
        indexkey = "plate_number" 

```

## DB Operations

```python

tc = TestCar()
tc.delete_table() # You can delete db--dynamo
tc.create_table() # You can create db--dynamo
tc.flush() # Flushes related db
dbsize = tc.dbsize() # Returns item count in db

```

**Note:** you can override create_table, delete_table in class declaration

## CRUD

You can simply make CRUD operations in objects. There is no seperate insert or update operation. All is **upsert** executed by *save_to_cache* 

```python
# Create
tc = TestCar() # There is no copy of object in db yet
tc.plate_number = "35 PLATE 35"
tc.save_to_cache() # now saved in db

# Read
tc = TestCar()
tc.get_by_id("666 PLATE 666") # Satan brings us the car with the idkey= 666 PLATE 666

# In below satan brings us the car with the idkey= 666 PLATE 666 if not exists, creates a new one in the memory 
# If it cant find in hell creates a new one in memory ( :  Still doesnt exists in db!!!
tc.get_or_create_by_id("666 PLATE 666") 

# Update
tc.top_speed = 666
tc.save_to_cache() # Put it in the db again!

# Delete
tc.delete() # i dont want it anymore!

# Populate

#You can populate your cars from another dict:
satans_car = TestCar()
stans_car.get_by_id("666 PLATE 666")

angel_car = TestCar()
angel_car.from_dict(satans_car.to_dict()) # we clone stan's car and all its attributes
angel_car.plate_number = "7 PLATE 7" # we turn it into new car
angel_car.save_to_cache() # And save it to db as a new car!

```

## Bulk Operations

```python
tc = TestCar() 
keys = tc.get_keys() # returns all keys in db

# Assume we have 3 test cars
updict = {
    "1 TEST 35": tcl35.to_dict(),
    "1 TEST 36": tcl36.to_dict(),
    "1 TEST 37": tcl37.to_dict()
}

TestCar.save_multi(updict)  # bulk insert 

dict_of_dicts = tc.get_multi(["666 PLATE 666","666 PLATE 667"]) # returns selected cars in db as as dictionary dict

car_list = tc.get_all_as_objectlist() # returns all cars in db # Be careful memory usage could be a problem in big sizes !
list_of_dicts = tc.get_all_as_list() # returns all cars in db  as dictionary list, More speeder, more effective memory usage!

car_dict = tc.get_all_as_objectdict() # returns all cars in db as dict instead of list # Be careful memory usage could be a problem in big sizes
dict_of_dicts = tc.get_all_as_dict() # returns all cars in db  as dictionary of dictionaries, More speeder, more effective memory usage!

```

## Tagging

Tagging is supported even your backend doesnt supports it too!!

But beware while using tags. All is in your responsibility.

For example you have to remove an object from tag if you removed object because tags and objects are not directly releated.

```python
# returns all tag names in db
taglist = TestCar.get_tags()

# returns all items's keys tagged by satan
itemkeylist = TestCar.get_tag_keys("Satan")

# returns all items tagged by Satan
itemlist = TestCar.get_by_tag("Satan")

tc = TestCar() 
tc.get_by_id("666 PLATE 666")

# adds "Satan","Super car", "Red" tags to item
tc.add_tags_to_item(["Satan","Super car", "Red"])

# we added "Super car" by mistake and now will remove it from object
tc.remove_item_from_tag("Super car")

# oh we forget to add tag "Favorite" now adding it to the item while save
tc.save_to_cache(["Favorite"])

```

## Backup And Restore

There is also backup tools to keep things safe. In the below scenario we want to backup all the table,
and restore back again.

```python
# ###############
# EXPORT

exportlist =  TestCar.get_all_as_list()

# exports the exportlist into compressed, None fields cleaned, new line markers removes jsontext
export_text = TestCar.export_to_json_text(exportdict, compress_data=True)

# or we can export it into a json file
TestCar.export_to_json_file("export.json", exportlist)

# or we can export it into a zip file
TestCar.export_to_json_zip("export.zip", exportlist)

# ###############
# IMPORT

TestCar.import_from_json_zip("export.zip")
# or
TestCar.import_from_json_file("export.json")
# or
TestCar.import_from_json_text("export_text")

```
