<img src="docs/assets/mlpipe_icon_full.png" width="500">

# MLPipe-Trainer

Manage your Data Pipline and Tensorflow & Keras models with MLPipe. It is NOT another "wrapper" around Tensorflow, but rather adds utilities to setup an environment to control data flow and managed trained models (weights & results) with the help of MongoDB.</br>

```bash
>> pip install mlpipe-trainer
```

## Setup - install MongoDB
MongoDB database is used to store trained Models including their weights and results. Additionally there is also a data reader for MongoDB implemented (basically just a generator as you know and love from using keras). Currenlty that is the only implemented data reader working "out of the box".</br>
Follow the instructions on the MongoDB website for installation e.g. for Linux: https://docs.mongodb.com/manual/administration/install-on-linux/

## Code Examples

#### Config
```python
# The config is used to specify the localhost connections
# for saving trained models to the mongoDB as well as fetching training data
from mlpipe.utils import Config
Config.add_config('./path_to/config.ini')
```
Each Connection config consists of these fields in the .ini file
```ini
[example_mongo_db_connection]
db_type=MongoDB
url=localhost
port=27017
user=read_write
pwd=rw
```

#### Data Pipline
```python
from mlpipe.processors.i_processor import IPreProcessor
from mlpipe.data_reader.mongodb import MongoDBGenerator

class PreProcessData(IPreProcessor):
    def process(self, raw_data, input_data, ground_truth, piped_params=None):
        # Process raw_data to output input_data and ground_truth
        # which will be the input for the model
        ...
        return raw_data, input_data, ground_truth, piped_params

train_data = [...]  # consists of MongoDB ObjectIds that are used for training
processors = [PreProcessData()]  # Chain of Processors (in our case its just one)
# Generator that can be used e.g. with keras' fit_generator()
train_gen = MongoDBGenerator(
    ("connection_name", "cifar10", "train"),  # specify data source from a MongoDB
    train_data,
    batch_size=128,
    processors=processors
)
```
Data generators inherit from `tf.keras.utils.Sequence`. Check out this [tensorflow docu](https://www.tensorflow.org/api_docs/python/tf/keras/utils/Sequence) to find out how you can write your custom generators (e.g. for other data sources than MongoDB).

#### Model
As long as there is a keras (tensorflow.keras) model in the end, there are no restrictions on this step
```python
model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same', input_shape=(32, 32, 3)))
...
model.add(Dense(10, activation='softmax'))

opt = optimizers.RMSprop(lr=0.0001, decay=1e-6)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=["accuracy"])
```

#### Training and Callbacks
```python
from mlpipe.callbacks import SaveToMongoDB

save_to_mongodb_cb = SaveToMongoDB(("localhost_mongo_db", "models"), "test", model)

model.fit_generator(
    generator=train_gen,
    validation_data=val_gen,
    epochs=10,
    verbose=1,
    callbacks=[save_to_mongodb_cb],
    initial_epoch=0,
)
```
`SaveToMongoDB` is a custom keras callback class as described in the [tensorflow docu](https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/Callback). Again, feel free to create custom callbacks for any specific needs.</br>
If, instead of `fit_generator()`, each batch is trained one-by-one e.g. with a native tensorflow model, you can still loop over the generator. Just remember to call the callback methods at the specific steps e.g. `on_batch_end()`.

A full Cifar10 example can be found in the example folder [here](https://github.com/j-o-d-o/MLPipe-Trainer/tree/master/examples/cifar10)

## Road Map
- Create and generat MkDocs documentation & host documentation
- Add tests
- Set Up CI
