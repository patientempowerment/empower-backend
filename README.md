# EMPOWER

This is the server-side part of the Empower platform.

## Requirements

* Python3
* Pip3 to install dependencies
* A MongoDB server with a clean collection (No empty fields or documents)

## Installation
If running this on a non-dedicated system, consider using a `venv` for installation and usage of this project.

    sudo apt install python3 pip3
    pip3 install scikit-learn=0.21.2 flask=1.0.3 pymongo=3.8.0 pandas=0.24.2 joblib=0.13.2 matplotlib=3.1.0 pandas_profiling=1.4.2 numpy=1.16.4 odo=0.5.0 
    git clone git@github.com:patientempowerment/patientEmpowerment.git

## Usage

The main functionalities are placed in the `rest_server` directory:
* `empower_cli.py`, giving access to the functions through the command-line, and
* `empower_server.py`, providing a REST-API for access through the web.

In the `useful_scripts` directory you can find some data cleaning utilities used in the project.


### CLI
`python3 empower_cli.py --help`

In short: 
* `--database`, `--collection`, and `--labels` are mandatory
* --database expects the name of a mongo db
* --collection is a collection in that db
* --labels expects names of columns to predict on, like "something somethingElse"
* Label-Columns' fields should contain exclusively 0 or 1

For example, if you want to predict if people have *dogs*, *cats*, and/or *birds*. You have a mongoDB
called **Citizens12**, which has a collection called **livingSituation**. You would call:

`python3 empower_cli.py -db Citizens12 -c livingSituation -l "has_cat has_dog has_bird"`

Optionals are `--output` and `--correlator`.

--output generates a confusion matrix in /tmp/, where you can find a visual classification report.

--correlator superimposes the values of a column onto the graphs that are generated at each execution. 
For example, if you wanted visualize not only pet-distribution, but also get an idea for correlating house-size
 you could call `-corr house-size-in-sqm`.

### Flask-Server
Runs a flask server offering a REST-API for the Empower application. All requests expect a JSON document.

Start the server by calling

    python3 empower_server.py

The API currently provides 4 endpoints:

`/predict` (POST):

Allows for server-side prediction of different labels. Currently, Logistic Regression is used as a predictor.
All fields used by the model during training need to be in the request body.

The request body should be formatted like this:
    
    {
        "user_data": {
  	        <feature1>: <value1>,
  	        <feature2>: <value2>,
  	        ...
        },
        "labels": [
            <label1>,
            <label2>,
            ...
        ]
    }

The server's response will look like this:

    {
        <label1>: <prediction1>,
        <label2>: <prediction2>,
        ...
    }

`/models` (POST):

Asks the server for its precomputed models to allow for on-device predictions. Currently, we use logistical regression,
for which only 

The request body should be formatted like this:

    {
        "labels": [
            <label1>,
            <label2>,
            ...
        ]
    }
    
The server's response will look like this:

    {
        <label1>: {
            "features": {
                <feature1>: {
                    "coef": <feature1-coef>,
                    "mean": <feature1-mean>
                },
                <feature2>: {
                    "coef": <feature2-coef>,
                    "mean": <feature2-mean>
                },
                ...
            },
            "intercept": <label1-intercept>
        }
        ...
    }

                

`/retrain` (POST):

Asks the server to retrain its models on a given database and collection and for a given set of labels contained in the
collection.

The request body should be formatted like this:

    {
        "db": <mongo db name>,
        "collection": <mongo collection name>,
        "labels": [
            <label1>,
            <label2>,
            ...
        ]
    }
    
The server's response will look like this:

    {
        <label1>: <prediction1>,
        <label2>: <prediction2>,
        ...
    }
    

`feature-config` (POST):

Requests a configuration JSON for the user-facing data input fields. This JSON gets auto-generated from the fields in
the collection specified by the user. By default, every field with values between 0 and 1 becomes a 'choice' field,
represented by radio buttons in the application, every other field becomes a slider.

The request should be formatted like this, specifying the DB and collection the user wants the configuration JSON for:

    {
      "db": <mongo db name>,
      "collection": <mongo collection name>
    }

The response will look as follows, with `<featureX>` being the name of the feature in the collection and
`<featureX_title>` being the human readable name to be displayed on the GUI of the requesting application.


    {
        <feature1>: {
            "choices": {
                "No": 0,
                "Yes": 1
            },
            "title": <feature1_title>,
            "mean": <float>
        },
        <feature2>: {
            "slider_max": <value>,
            "slider_min": <value>,
            "title": <feature2_title>,
            "mean": <float>
        },
        ...
    }

## Contributing

## License
[MIT](https://choosealicense.com/licenses/mit/)