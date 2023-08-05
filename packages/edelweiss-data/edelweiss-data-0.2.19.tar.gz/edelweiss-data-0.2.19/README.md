This python client library allows easy access to [Edelweiss Data](https://www.saferworldbydesign.com/edelweissdata) servers.

# Table of Contents

- [Overview](#overview)
- [Getting started](#getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)
- [Common use cases](#common-use-cases)
  - [Initialization](#initialization)
  - [Authentication](#authentication)
  - [Create a new dataset](#create-a-new-dataset)
  - [Search for datasets](#search-for-datasets)
  - [Filter and retrieve data](#filter-and-retrieve-data)
  - [Delete a new dataset](#delete-a-dataset)
- [API reference](#api-reference)

# Overview

The core concept of Edelweiss Data is that of a **Dataset**. A Dataset is a single table of data (usually originating from a csv file) and carries the following additional pieces of information:
* a **schema** describing the structure of the tabular data (data types, explanatory text for each column etc)
* a human readable **description text** (markdown formatted - like the readme of a repository on github)
* a **metadata json** structure (of arbitrary complexity - this can be used to store things like author information, instrument settings used to generate the data, ...).

Datasets are **versioned** through a processes called publishing. Once a version of a dataset is published, it is "frozen" and becomes immutable. Any change to it has to be done by creating a new version. Users of Edelweiss Data will always see the version history of a dataset and be able to ask for the latest version or specific earlier version.

Datasets can be public or **access restricted**. Public datasets can be accessed without any access restrictions. To access restricted datasets or to upload/edit your own dataset OpenIDConnect/OAuth is used - in the python client this process is done by calling the authenticate method on the Api instance that triggers a web based login at the end of which a token is confirmed.

When retrieving the tabular data of a dataset, the data can be **filtered and ordered** and only specific columns requested - this makes request for subsets of data much faster than if all filtering happened only on the client. Conditions for filtering and ordering are created by constructing QueryExpression instances using classmethods on the QueryExpression class to create specific Expressions. You can access the data either in it's raw form (as json data) or, more conveniently, as a Pandas Dataframe.

Just like the tabular data of one particular dataset can be retrieved as a **Pandas DataFrame**, you can also query for datasets using the same filtering and ordering capabilities - i.e. you can retrieve a DataFrame where each row represents a Dataset with it's name, description and optionally metadata and schema (not including the data though).

When you are searching for Datasets, a lot of the interesting information that you may want to filter by is hidden in the **metadata** (e.g. maybe most of your datasets have a metadata field "Species" at the top level of the metadata json that indicates from what kind of animal cells the data in this dataset originate from). To make such filtering easy, our Datasets query function take an optional list of "column mappings" that allow you to specify a **JsonPath expression** to extract a field from the metadata and include it with a given name in the resulting DataFrame. In the Species example, you could pass the list of column mappings [("Species from Metadata", "$.Species")] and the resulting DataFrame would contain an additional column "Species from Metadata" and for every row the result of evaluating the JsonPath $.Species would be included in this column and you could filter on it using conditions to e.g. only retrieve Datasets where the Species is set to "Mouse".

Edelweiss Data servers provide a rich **User Interface** as well that let's you visually browse and filter datasets and the data (and associated information) of each dataset. This UI is built to integrate nicely with the python client. The DataExplorer that is used to explore a dataset has a button in the upper right corner to generate the python code to get the exact same filtering and ordering you see in the UI into a Pandas DataFrame using the Edelweiss Data library for your convenience.

# More information and examples

The [official EdelweissData documentation](https://edelweissdata.com/docs/about) has more in-depth information about the various parts of EdelweissData.

In the [examples directory of this libraries Github page](https://github.com/DouglasConnect/edelweiss-data-python/tree/master/examples) you can find several Jupyter notebooks which repeat the walkthroughs from the official EdelweissData documentation but using the edelweiss_data library instead of direct HTTP calls shown with JavaScript.

# Getting started

## Requirements

Python 3.6+

## Installation

```bash
pip install edelweiss_data
```

# Common use cases

In addition to the brief overview below, do check out the [examples directory of this libraries Github page](https://github.com/DouglasConnect/edelweiss-data-python/tree/master/examples) that contains several Jupyter notebooks demonstrating common operations and showing e.g. all possible filter operators in use.

## Initialization

You interact with the Edelweiss Data API mainly via the API class of the edelweiss_data python library. Import it, point it at the Edelweiss Data instance you want to interact with and instantiate it like this:

```python
from edelweiss_data import API, QueryExpression as Q

# Set this to the url of the Edelweiss Data server you want to interact with
edelweiss_api_url = 'https://api.develop.edelweiss.douglasconnect.com'

api = API(edelweiss_api_url)

```

## Authentication

Some operations in Edelweiss Data are accessible without authentication (e.g. retrieving public datasets). For others (e.g. to create datasets), you need to be authenticated. Authentication is done with the authenticate call. Be aware that this call is currently built for interactive use like in a Jupyter environment - it will block execution for a up to a few minutes while it waits for you to log in to your account and confirm the access to the API on your behalf. Once accepted the python client will store the authentication token so that you will not have to enter it again for a few days (the token is stored in your home directory in the .edelweiss directory).

```python
api.authenticate()
```

## Create a new dataset

Creating and publishing a new dataset form a csv file can be done in one quick operation like so:

```python
metadata = {"metadata-dummy-string": "string value", "metadata-dummy-number": 42.0}
with open ('FILENAME') as f:
    dataset = api.create_published_dataset_from_csv_file("DATASETNAME", f, metadata)
```

This creates a new dataset form the file FILENAME with the name DATASETNAME. A trivial example metadata is used here as well.

When creating and publishing datasets like this you don't have a lot of control over details of the schema or to set a more elaborate dataset description. If you need more control, you can create a dataset like so:

```python
datafile = '../../tests/Serialization/data/small1.csv'
name = 'My dataset'
schemafile = None # if none, schema will be inferred below
metadata = None # dict object that will be serialized to json or None
metadatafile = None # path to the metadata file or None
description = "This is a *markdown* description that can use [hyperlinks](https://edelweissconnect.com)"

dataset1 = api.create_in_progress_dataset(name)
print('DATASET:', dataset1)
try:
    with open(datafile) as f:
        dataset1.upload_data(f)
    if schemafile is not None:
        print('uploading schema from file ...')
        with open(schemafile) as f:
            dataset1.upload_schema_file(f)
    else:
        print('inferring schema from file ...')
        dataset1.infer_schema()
    if metadata is not None:
        print('uploading metadata ...')
        dataset1.upload_metadata(metadata)
    elif metadatafile is not None:
        print('uploading metadata from file ...')
        with open(metadatafile) as f:
            dataset1.upload_metadata_file(f)

    dataset1.set_description(description)

    published_dataset = dataset1.publish('My first commit')
    print('DATASET published:',published_dataset)
except requests.HTTPError as err:
    print('not published: ', err.response.text)
```

## Filter and retrieve data

The tabular data of an individual dataset can be retrieved into a pandas dataframe easily like this:

```python
dataframe = dataset.get_data()
```

You can also filter and order data with QueryExpressions, often aliased to Q in the import statement. In the following example we assume the data to have a column "Species" which we want to filter to the value "Mouse" with fuzzy text matching and "Chemical name" which we want to order by ascending:

```python
dataframe = dataset.get_data(condition=Q.fuzzy_search(Q.column("Species"), "Mouse"), order_by=[Q.column("Chemical name")])
```

In this example you can see how to do a chemical substructure search so that only molecules with the fragment "CC=O" are returned and the results are sorted descending by similarity to the molecule "C(C(CO)(CO)N)O". Chemical similarity for ordering is calculated using the rdkit library using tanimoto distance between rdkit fingerprints (other fingerprints or distance metrics could be supported in the future)

```python
dataframe = dataset.get_data(condition=Q.substructure_search("CC=O", Q.column("SMILES")), order_by=[Q.tanimoto_similarity("C(C(CO)(CO)N)O", Q.column("SMILES"))], ascending=False)
```

## Search for datasets

To just retrieve a pandas dataframe with all published datasets that you are allowed to see use get_published_datasets(). This will return a pandas dataframe with a multiindex of the dataset id and version and then a single object column for the dataset class instance. This class instance can be used to retrieve e.g. the name property of the dataset or it can be used to retrieve the data for this dataset by calling the .get_data() method or similar operations.

```python
datasets = api.get_published_datasets()
dataset = datasets.iloc[0].dataset
print("Found {} datasets. The name of the first is: ".format(len(datasets), dataset.name))
```

To retrieve a single dataset by index value rather than based on numerical position use the pandas multiindex functionality passing in tuples:

```python
datasetid = '49fd99ee-ec6f-44df-a8cd-73f0f8bbcd76' # example dataset ID
version = 1
dataset = datasets.loc[(datasetid, version)]
```

Just like above with data you can use QueryExpressions to filter to only find datasets matching certain predicates. Below we filter on datasets that have the string "LTKB" somewhere in them (name etc)

```python
datasets_filter = Q.search_anywhere("LTKB")
datasets = api.get_published_datasets(condition=datasets_filter)
```

Since very often the most interesting filter and sort critieria will be in the metadata (which is a Json of arbitrary structure), the Api gives you a way to add additional columns by extracting pieces from the metadata json with JsonPath expressions. Below we attempt to treat the metadata json of each dataset as an object with a key "Species" and if it is present we extract it and map it into the "Species from metadata json" column:

```python
columns = [("Species from metadata json", "$.Species")]
datasets = api.get_published_datasets(columns=columns)
```

The result of such a query will always be a column containing lists of results as the jsonpath query could return not just a single primitive value or null or an object but also json arrays. Working with columns that contain lists in Pandas can be a bit awkward as some operations like filtering default to operating on series instead of individual cells. For cases like these, working with the Pandas apply method usually makes things easier - e.g. if you want to extract the first element if any from the above column this an easy way to do it that also extends well to more complex operations:

```python
datasets['first_species_or_none'] = datasets.apply(lambda row: row['Species from metadata json'][0] if len(row['Species from metadata json']) > 0 else None, axis=1)
```

## Delete a dataset

To delete a dataset and all versions call delete_all_versions:

```python
dataset.delete_all_versions()
```

# API reference

## `API`

The central interaction point with EdelweissData. You instantiate this class with the base url of the

EdelweissData server you want to interact with. The __init__ method will verify that the server is reachable
and speaks a compatible API version, then you can use instance methods to interact with the API server.

### `add_dataset_group_permission`

Add a group to a dataset

**dataset_id**  : *the id of the dataset*

**group**  : *the Group to add*

### `add_dataset_user_permission`

Add a user to a dataset

**dataset_id**  : *the id of the dataset*

**user**  : *the User to add*

### `authenticate`

### `change_dataset_visibility`

Set if the dataset should be public or access protected when published

**dataset_id**  : *the id of the dataset*

**is_public**  : *boolean to indicate if the dataset should be public*

### `create_in_progress_dataset`

Creates a new in-progress dataset on the server and returns it.

**Returns:** The InProgressDataset that was created.

**name**  : *the name of the dataset to create*

### `create_in_progress_dataset_from_csv_file`

Creates a new in-progress dataset from a CSV file on the server.

**Returns:** the updated dataset

**name**  : *the name of the dataset*

**file**  : *opened text file to read the csv data from*

**metadata**  : *dict of the metadata to store as json together with the dataset*

**description**  : *description text for the dataset (markdown formatted)*

**is_public**  : *flag to indicate if the dataset should be public or access restricted after publishing*

### `create_published_dataset_from_csv_file`

Creates a new published dataset from a CSV file on the server.

**Returns:** the published dataset

**name**  : *the name of the dataset*

**file**  : *opened text file to read the csv data from*

**metadata**  : *dict of the metadata to store as json together with the dataset*

**changelog**  : *Publishing message to store for the first version*

**description**  : *description text for the dataset (markdown formatted)*

**is_public**  : *flag to indicate if the dataset should be public or access restricted after publishing*

### `delete`

Sends a DELETE request to a server.

**Returns:** dict with the JSON response.

**route**  : *route to which the request will be sent*

### `get`

Sends a GET request to a server.

**Returns:** dict with the JSON response.

**route**  : *route to which the request will be sent*

**json**  : *dict with the JSON body to send*

### `get_dataset_permissions`

Get the permissions for the given dataset id

**Returns:** the DatasetPermissions instance for this dataset

**dataset_id**  : *the id of the dataset*

### `get_in_progress_dataset`

Returns an in-progress datasets with a given id.

**Returns:** an InProgressDataset

**id**  : *the id of the dataset to retrieve*

### `get_in_progress_datasets`

Returns a list of all in-progress datasets you are allowed to access (needs authentication).

**Returns:** a list of InProgressDatasets

**limit**  : *Number of datasets to retrieve - if None (default) it will retrieve all.*

**offset**  : *Starting offset from which to retrieve the datasets*

### `get_published_dataset`

Returns a published dataset with a given id and version.

**Returns:** the PublishedDataset

**id**  : *id of the dataset to retrieve*

**version**  : *version of the dataset to retrieve. Defaults to LATEST if none specified.*

### `get_published_dataset_aggregations`

Returns aggregation buckets and their sizes for each column.

**Returns:** aggregations as a Series with an index of buckets and terms, for example
bucket     term
organ      liver          10
           kidney         20
species    mouse           5
           elephant       30

**columns**  : *same as in self.get_published_datasets*

**condition**  : *same as in self.get_published_datasets*

**aggregation_filters**  : *same as in self.get_published_datasets*

### `get_published_dataset_versions`

Returns all published versions of dataset with a given id.

**Returns:** a list of PublishedDatasets

**id**  : *id of the dataset*

### `get_published_datasets`

Returns a dataframe of all published datasets that match query.

**Returns:** a dataframe indexed by the id and version, which in addition
to user-specified columns, contains a column with a PublishedDataset
object for each dataset. Unless included explicitly, description, schema,
and metadata are omitted from the datasets and the corresponding
attributes are set to None. On the first access to any of the missing
attributes of a given dataset, all three them are fetched from the server
and set to the actual values, resulting in a single request for each dataset.
If there are many datasets for which the attributes are required, it makes
sense to include the content in the bulk request.

**columns**  : *a list of pairs (column_name, json_path) describing
the name of the new column to generate and which jsonpath to use to
extract the values from the metadata to fill this column.*

**condition**  : *a QueryExpression object limiting the fetched datasets.*

**include_description**  : *a boolean specifying if the datasets in
the response should include the description*

**include_schema**  : *a boolean specifying if the datasets in
the response should include the schema*

**include_metadata**  : *a boolean specifying if the datasets in
the response should include the metadata*

**aggregation_filters**  : *a dict limiting the fetched datasets to ones
where column values fall into one of the selected aggregation buckets.
For example, using the dict
  {'organ': ['liver', 'kidney'], 'species': ['mouse', 'elephant']}
would return the datasets where both organ is either liver or kidney,
AND species is either mouse or elephant.*

**limit**  : *the number of rows to return.
Returns all rows if set to None (default).*

**offset**  : *the initial offset (default 0).*

**order_by**  : *a list of QueryExpression objects by which to order
the resulting datasets.*

**ascending**  : *a boolean or list of booleans to select the ordering.
If the single boolean is True (the default), the list is ascending
according to order_by, if False, it is descending. If given as a list,
it must be of the same length as the order_by list, and the order is
the ascending/descending for each particular component.*

**dataset_column_name**  : *the name of the dataframe column in which
the corresponding PublishedDataset objects are available.*

**latest_only**  : *a boolean specifying whether to return only the latest
version of each dataset*

### `get_raw_datasets`

Get the published datasets. Unlike the more high-level get_published_datasets this method

does not create a dataframe but returns the raw list of dicts representing the json response.
     Unless explicity included the fields schema, metadata and description will not be included
     in the response.

**Returns:** The published datasets as a list of dicts (raw json response)

**columns**  : *a list of pairs (column_name, json_path) describing
columns in the dataframe.*

**condition**  : *a QueryExpression object limiting the fetched datasets.*

**include_description**  : *a boolean specifying if the datasets in
the response should include the description*

**include_schema**  : *a boolean specifying if the datasets in
the response should include the schema*

**include_metadata**  : *a boolean specifying if the datasets in
the response should include the metadata*

**aggregation_filters**  : *a dict limiting the fetched datasets to ones
where column values fall into one of the selected aggregation buckets.
For example, using the dict
  {'organ': ['liver', 'kidney'], 'species': ['mouse', 'elephant']}
would return the datasets where both organ is either liver or kidney,
AND species is either mouse or elephant.*

**limit**  : *the number of rows to return (default 100).
Returns all rows if set to None.*

**offset**  : *the initial offset (default 0).*

**order_by**  : *a list of QueryExpression objects by which to order
the resulting datasets.*

**ascending**  : *a boolean or list of booleans to select the ordering.
If the single boolean is True (the default), the list is ascending
according to order_by, if False, it is descending. If given as a list,
it must be of the same length as the order_by list, and the order is
the ascending/descending for each particular component.*

**latest_only**  : *a boolean specifying whether to return only the latest
version of each dataset*

### `oidc_config`

Returns the OpenID Connect configuration.

### `openapi`

Returns the OpenAPI definition of the entire EdelweissData REST API.

**Returns:** The OpenAPI definition as a dict

### `openapi_documents`

Returns a list of all dataset specific openapi descriptions (i.e. one openapi document for each dataset with the

precise Json Schema of the particular datasets data endpoint).

**Returns:** A list of url strings at which to retrieve the openapi.json documents for the documents

### `post`

Sends a POST request to a server.

**Returns:** dict with the JSON response.

**route**  : *route to which the request will be sent*

**json**  : *dict with the JSON body to send*

### `post_raw`

Sends a POST request with a given body to a server.

**Returns:** dict with the JSON response.

**route**  : *route to which the request will be sent*

**body**  : *raw body to send (a bytes object or a string that will be encoded as UTF-8)*

### `remove_dataset_group_permission`

Remove a group from a dataset

**dataset_id**  : *the id of the dataset*

**name**  : *the name of the group to remove*

### `remove_dataset_user_permission`

Remove a user from a dataset

**dataset_id**  : *the id of the dataset*

**user**  : *the email of the user to remove*

### `upload`

Uploads a POST request that uploads files to a server.

**Returns:** dict with the JSON response.

**route**  : *route to which the request will be sent*

**files**  : *a dictionary of files in which the keys are filenames
and corresponding values are file objects*

## `DatasetPermissions`

The permission information for a dataset. A list of users (email + flag if they can write), groups (name + flag if they can write) and

an is_public field that indicates whether unauthenticated users can see this dataset when published.

### `Group`

#### `decode`

#### `encode`

### `User`

#### `decode`

#### `encode`

### `decode`

### `encode`

## `InProgressDataset`

InProgressDataset - datasets that are not yet published and for which data can be uploaded, the schema modified, metadata changed etc.

### `copy_from`

Copies all content from a PublishedDataset to this InProgressDataset. Useful to create new versions.

This is a lightweight operation, which works by re-using the same underlying data source.

### `decode`

### `delete`

Deletes the InProgressDataset

### `encode`

### `get_permissions`

### `infer_schema`

Triggers schema inference from uploaded data (this creates a schema on the server and sets it on the InProgressDataset)

### `publish`

Attempts to publish the dataset. This means that a new version of a PublishedDataset will be created (and returned by this call)

and this InProgressDataset is no longer useable.

### `sample`

Retrieve a list of lists representing a sample of the tabular data of this dataset. This

includes only a sample (e.g. the first N rows) of the data so that they can be displayed to a
user as an example or similar.

### `set_data_source`

Set the data source for an in-progress dataset. This allows you to efficiently re-use the data of a PublishedDataset

to create a new dataset without re-uploading the data. It is also useful if you want to create a new version of a
    PublishedDataset to fix a mistake in the metadata or description.

**dataset**  : *the PublishedDataset to copy data from when publishing*

### `set_description`

Set the description of the dataset. The description is assumed to be markdown formatted text, similar to a Github README.md

### `set_name`

Set the name of the dataset.

### `update`

Update various attributes of a in-progress dataset. All parameters are options; those that are

None will not have their values changed.

**name**  : *A new name for the dataset*

**description**  : *A new description for the dataset*

**data_source**  : *A new data_source for the dataset. See set_data_source for a description of a data source.*

**schema**  : *A new schema for the dataset.*

**metadata**  : *A new metadata object for the dataset.*

### `upload_data`

Upload tabular data (a CSV file)

**data**  : *An open text file containing the csv data to upload*

### `upload_dataframe_data`

Upload a pandas dataframe as the data content into an InProgress dataset

**dataframe**  : *A Pandas dataframe containing the data to upload*

### `upload_metadata`

Upload metadata (as a dict, not a file).

**schema**  : *The metadata to upload*

### `upload_metadata_file`

Upload a metadata file (an open text file containing the metadata in Json form).

**file**  : *The open text file to upload the metadata from*

### `upload_schema`

Upload a Schema (an instance of the class, not a file).

**schema**  : *The schema to upload*

### `upload_schema_file`

Upload a schema file (an open text file containing the schema in Json form).

**file**  : *The open text file to upload the schema from*

## `PublishedDataset`

Represents a published dataset

### `decode`

### `delete_all_versions`

Deletes all versions of a published dataset

### `encode`

### `get_data`

Gets the (tabular) data of a PublishedDataset as a pandas Dataframe. The data can be filtered so that only required columns or rows

are retrieved.

**Returns:** A pandas DataFrame with the tabular data

**columns**  : *a list of column names that should appear in the result.
If None, all columns are included.*

**condition**  : *a QueryExpression object limiting the fetched datasets.*

**aggregation_filters**  : *a dict limiting the fetched datasets to ones
where column values fall into one of the selected aggregation buckets.
For example, using the dict
  {'organ': ['liver', 'kidney'], 'species': ['mouse', 'elephant']}
would return the datasets where both organ is either liver or kidney,
AND species is either mouse or elephant.*

**limit**  : *the number of rows to return.
Returns all rows if set to None (default).*

**offset**  : *the initial offset (default 0).*

**order_by**  : *a list of QueryExpression objects by which to order
the resulting datasets.*

**ascending**  : *a boolean or list of booleans to select the ordering.
If the single boolean is True (the default), the list is ascending
according to order_by, if False, it is descending. If given as a list,
it must be of the same length as the order_by list, and the order is
the ascending/descending for each particular component.*

### `get_data_aggregations`

Returns aggregation buckets and their sizes for each column.

**Returns:** aggregations as a Series with an index of buckets and terms, for example
bucket     term
organ      liver          10
           kidney         20
species    mouse           5
           elephant       30

**columns**  : *a list of column names that should appear in the result.
If None, all columns are included.*

**condition**  : *a QueryExpression object limiting the fetched datasets.*

**aggregation_filters**  : *a dict limiting the fetched datasets to ones
where column values fall into one of the selected aggregation buckets.
For example, using the dict
  {'organ': ['liver', 'kidney'], 'species': ['mouse', 'elephant']}
would return the datasets where both organ is either liver or kidney,
AND species is either mouse or elephant.*

### `get_permissions`

Returns the Permissions object of this PublishedDataset

### `get_raw_data`

Gets the raw tabular data JSON response for a PublishedDataset. The data can be filtered so that only required columns or rows

are retrieved.

**Returns:** A dict representing the JSON response

**columns**  : *a list of column names that should appear in the result.
If None, all columns are included.*

**condition**  : *a QueryExpression object limiting the fetched datasets.*

**aggregation_filters**  : *a dict limiting the fetched datasets to ones
where column values fall into one of the selected aggregation buckets.
For example, using the dict
  {'organ': ['liver', 'kidney'], 'species': ['mouse', 'elephant']}
would return the datasets where both organ is either liver or kidney,
AND species is either mouse or elephant.*

**limit**  : *the number of rows to return.
Returns all rows if set to None (default).*

**offset**  : *the initial offset (default 0).*

**order_by**  : *a list of QueryExpression objects by which to order
the resulting datasets.*

**ascending**  : *a boolean or list of booleans to select the ordering.
If the single boolean is True (the default), the list is ascending
according to order_by, if False, it is descending. If given as a list,
it must be of the same length as the order_by list, and the order is
the ascending/descending for each particular component.*

### `new_version`

Create a new version of this PublishedDataset. This will create and return a new InProgressDataset

that can be filled with content by uploading new files or copying data from a PublishedDataset

**Returns:** The InProgressDataset

### `openapi`

Returns a OpenAPI descriptions for the data endpoint of this PublishedDataset, taking the schema

and thus the precise JSON structure of the response into account.

**Returns:** A dict respresenting the JSON decoded OpenAPI document

## `QueryExpression`

Used to create filters or expressions to order records by. Use the classmethods on this

class to create instances, e.g. QueryExpression.fuzzySearch(QueryExpression.column("species"), "Monkey")

### `cast`

Creates a Cast expression. This attempts to convert one datatype into another.

**expr**  : *The expression to cast*

**data_type**  : *The datatype to cast to*

### `column`

Constructs a Column expression.

**column_name**  : *the name of the column*

### `contained_in`

Creates a ContainedIn expression. Tests if an expression is contained in an element. Often used

to check if columns of an Array datatype are contained in a value.

**expr**  : *The expression to search for*

**element**  : *The element to search in*

### `contains`

Creates a Contains expression. Tests if an expression contains an element. Often used

to check if columns of an Array datatype contain a value.

**expr**  : *The expression to search in*

**element**  : *The element to search for*

### `decode`

### `encode`

### `exact_search`

Constructs an ExactSearch expression. Only rows where the expr expression exactly matches the term will be returned. This can be used

to match exact substrings or exact numerical values

**expr**  : *the search expression to evaluate (often a column QueryExpression)*

**term**  : *the search term*

### `fuzzy_search`

Constructs a FuzzySearch expression. Only rows where the expr expression fuzzy-matches the term will be returned. Fuzzy-matching

uses trigram indexing to match slightly different spellings.

**expr**  : *the search expression to evaluate (often a column QueryExpression)*

**term**  : *the search term*

### `search_anywhere`

Constructs a SearchAnywhere expression. Only rows will be returned that contain the search term in one of their text-like columns.

**term**  : *The string to search for in all text-like columns.*

### `substructure_search`

Constructs a SubstructureSearch expression that uses chemical substructure testing. Only rows where the chemical substructure is contained in

the chemical superstructure are returned.

**substructure**  : *the substructure to search (often a SMILES string constant value)*

**superstructure**  : *the search term (often a Column of datatype SMILES)*

### `system_column`

Constructs a SystemColumn expression. SystemColumns are special columns maintained by EdelweissData.

The following SystemColumns are available:
        name (text): the name of a dataset
        created (text/datetime): the timestamp the dataset was created at
        version: (int): the version number of the dataset

**column_name**  : *the name of the column*

### `tanimoto_similarity`

Calculates the tanimoto distance between two molecular fingerprints.

**left**  : *the left argument. Often a SMILES string constant value or Column of datatype SMILES.*

**right**  : *the right argument. Often a SMILES string constant value or Column of datatype SMILES.*

## `Schema`

The schema of the dataset describing the columns (name, description, datatype, rdf predicate, ...)

### `Column`

The schema data of one column. This tells EdelweissData the name of the column, the datatype to use, how to handle missing values, ...

#### `decode`

#### `encode`

### `decode`

### `encode`

## `cast`

Cast a value to a type.

This returns the value unchanged.  To the type checker this
signals that the return value has the designated type, but at
runtime we intentionally don't check anything (we want this
to be as fast as possible).
