# """
# A feature store client. This module exposes an API for interacting with feature stores in Bytehub.
# It hides complexity and provides utility methods such as:
#     - `configure()`
#     - `create_feature()`
#     - `get_feature()`.
#     #- `project_featurestore()`.
#     #- `get_featuregroup()`.
#     - `get_timeseries()`.
#     #- `sql()`
#     #- `insert_into_featuregroup()`
#     #- `get_featurestore_metadata()`
#     #- `get_project_featurestores()`
#     #- `get_featuregroups()`
#     #- `get_training_datasets()`
# """


import os
import itertools
import operator
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from getpass import getpass
import time
import json
import re


class FeatureStore():

    def __init__(self, endpoint, client_id=None, client_secret=None):
        # Save the endpoint
        self.endpoint = endpoint
        if endpoint[-1] != '/':
            self.endpoint += '/'
        # Get the Oauth2 URLs
        response = requests.get(self.endpoint + 'auth')
        response.raise_for_status()
        self.urls = response.json()

        # Decide with authentication method to use
        self.client_id = os.environ.get('BYTEHUB_CLIENT_ID', client_id)
        self.client_secret = os.environ.get(
            'BYTEHUB_CLIENT_SECRET', client_secret)
        if self.client_secret:
            # Use client-credentials
            client = BackendApplicationClient(client_id=self.client_id)
            oauth = OAuth2Session(client=client)
            tokens = oauth.fetch_token(
                self.urls['token_url'],
                client_id=self.client_id,
                client_secret=self.client_secret
            )
        else:
            # Use interactive login
            oauth = OAuth2Session(
                client_id, redirect_uri=self.urls['callback_url'])
            authorization_url, state = oauth.authorization_url(
                self.urls['login_url'])
            print(
                f'Please go to {authorization_url} and login. Copy the response code and paste below.')
            code_response = getpass('Response: ')
            tokens = oauth.fetch_token(
                self.urls['token_url'], code=code_response, include_client_id=True
            )
        self.tokens = tokens

    def _check_tokens(self):
        # Check that token hasn't expired
        if time.time() < self.tokens['expires_at'] - 10:
            return True
        else:
            # Token expired... refresh it
            if 'refresh_token' in self.tokens:
                oauth = OAuth2Session(self.client_id, token=token)
                tokens = oauth2.refresh_token(
                    self.urls['token_url'],
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    include_client_id=True
                )
            else:
                # Authenticate again with client credentials
                client = BackendApplicationClient(client_id=self.client_id)
                oauth = OAuth2Session(client=client)
                tokens = oauth.fetch_token(
                    self.urls['token_url'],
                    client_id=self.client_id,
                    client_secret=self.client_secret
                )
            self.tokens = tokens

    def _api_headers(self):
        self._check_tokens()
        return {
            'Authorization': self.tokens['access_token']
        }

    def list_features(self, feature=None, regex=None, metadata=False):
        """List features in feature store.

        Parameters
        ----------
        feature : str or list[str], optional
            Only return these feaures.
        regex : str, optional
            Regular expression to filter feature names.
        metadata : bool, default False
            Return metadata with features.

        Returns
        -------
        list[str] or pd.DataFrame
            A list of features or dataframe of features and metadata.

        Examples
        --------
        >>> bytehub.list_features()
        ['feature1', 'feature2', 'feature3']

        >>> bytehub.list_features(regex='weather', metadata=True)
        name	        metadata
        ------------------------------------------
        0	weather.actual	{'source': 'NOAA GFS'}
        """

        assert type(metadata) is bool, "metadata is type, bool."
        assert regex is None or isinstance(
            regex, str), "Expecting regex of type, str."

        df = self.get_feature_data_frame(feature=feature, regex=regex)

        if metadata:
            return df[['name', 'metadata']]
        else:
            return df.name.tolist()

    def feature_exists(self, feature):
        """Check whether feature(s) exist.

        Parameters
        ----------
        feature : str or list[str]
            A feature or list of features.

        Returns
        -------
        bool or list[bool]
            A boolean or list of booleans indicating whether feature(s) exist.

        Examples
        --------
        >>> bytehub.feature_exists(['feature1', 'nonsense'])
        [True, False]
        """

        names = self.list_features(feature=feature)
        if isinstance(feature, list):
            return [f in names for f in feature]
        else:
            return feature in names

    def get_feature_data_frame(self, feature=None, regex=None):
        """Get a dataframe of feature metadata.

        Parameters
        ----------
        feature : str or list[str]
            A feature or list of features.
        regex: str
            A regex to filter results with

        Returns
        -------
        pd.DataFrame
            A dataframe containing feature metadata

        Examples
        --------
        >>> bytehub.get_feature_data_frame(['feature1', 'feature2'])
            id                                      name            metadata
        ----------------------------------------------------------------------------
        0	0341bacc-e161-11ea-a042-0a53e92ebe18    feature1	    {'source': NULL}
        1	193177cc-e158-11ea-a042-0a53e92ebe18    feature2	    {'source': NULL}
        """

        params = {}
        if feature:
            if not isinstance(feature, list):
                feature = [feature]
            is_str = [isinstance(f, str) for f in feature]
            assert all(is_str), 'Feature names should be type, str.'
            params['name'] = ','.join(feature)
        if regex:
            assert isinstance(regex, str), 'Regex query should be type, str'
            params['query'] = regex

        url = self.endpoint + 'feature'

        response = requests.get(
            url, params=params, headers=self._api_headers())
        response.raise_for_status()

        result = response.json()

        df = pd.DataFrame({'id': [r['id'] for r in result],
                           'name': [r['name'] for r in result],
                           'metadata': [r['metadata'] for r in result]})

        return df

    def get_feature_id(self, feature):
        """Get the unique id number of feature(s).

        Parameters
        ----------
        feature : str or list[str]
            A feature or list of features.

        Returns
        -------
        str or list[str]
            Ids for the feature(s).

        Examples
        --------
        >>> bytehub.get_feature_id(['feature1', 'feature2'])
        ['0341bacc-e161-11ea-a042-0a53e92ebe18', 
        '193177cc-e158-11ea-a042-0a53e92ebe18']
        """

        df = self.get_feature_data_frame(feature=feature)
        if isinstance(feature, str):
            assert feature in df.name.tolist(), f'The feature(s), {feature}, is non-existent.'
            return df[df.name == feature]['id'].iloc[0]
        else:
            assert len(feature) == len(
                df), 'One or more features are non-existent.'
            result = [
                df[df.name == f]['id'].iloc[0]
                for f in feature
            ]
            return result

    def get_feature_metadata(self, feature):
        """Get the metadata for feature(s).

        Parameters
        ----------
        feature : str or list[str]
            A feature or list of features.

        Returns
        -------
        pd.DataFrame
            A dataframe of metadata for feature(s).

        Examples
        --------
        >>> bytehub.get_feature_metadata(['feature1', 'feature2'])
            name            metadata
        ------------------------------------
        0	feature1	    {'source': NULL}
        1	feature2	    {'source': NULL}
        """

        df = self.get_feature_data_frame(feature)

        return df[['name', 'metadata']]

    def get_first(self, feature):
        """Gets first entry from feature in feature store per entity.

        Parameters
        ----------
        feature : str
            A feature name.

        Returns
        -------
        pd.DataFrame
            A pandas dataframe of first entry of feature per entity. 

        Examples
        --------
        >>> bytehub.get_first('weather.actual')
            time	                    entity	    value
        -------------------------------------------------
        0	2020-08-19 23:00:00+00:00	London	    21780
        1	2020-08-19 23:00:00+00:00	New York	19774

        """

        assert type(feature) is str, 'Feature type is, str.'

        feature_id = self.get_feature_id(feature)

        url = self.endpoint + f'timeseries/{feature_id}/first'
        response = requests.get(url, headers=self._api_headers())
        response.raise_for_status()

        df = pd.DataFrame(response.json())

        df['time'] = pd.to_datetime(df['time'], utc=True, unit='ms')

        return df

    def get_last(self, feature):
        """Gets last entry from feature in feature store per entity.

        Parameters
        ----------
        feature : str
            A feature name.

        Returns
        -------
        pd.DataFrame
            A pandas dataframe of last entry of feature per entity. 

        Examples
        --------
        >>> bytehub.get_last('weather.actual')
            time	                    entity	    value
        -------------------------------------------------
        0	2020-08-26 22:30:00+00:00	London	    23985
        1	2020-08-26 22:30:00+00:00	New York	22895

        """

        assert type(feature) is str, 'Feature type is, str.'

        feature_id = self.get_feature_id(feature)

        url = self.endpoint + f'timeseries/{feature_id}/last'
        response = requests.get(url, headers=self._api_headers())
        response.raise_for_status()

        df = pd.DataFrame(response.json())

        df['time'] = pd.to_datetime(df['time'], utc=True, unit='ms')

        return df

    def get_freq(self, feature):
        """Gets freq of time column of feature in feature store.

        Parameters
        ----------
        feature : str
            A feature name.

        Returns
        -------
        str
            Datetime freq.

        Examples
        --------
        >>> bytehub.get_freq('weather.actual')
        '30T'
        """

        assert isinstance(feature, str), 'Feature type is, str.'
        assert self.feature_exists(feature), 'Feature does not exist.'

        feature_id = self.get_feature_id(feature)

        url = self.endpoint + f'timeseries/{feature_id}/freq'
        response = requests.get(url, headers=self._api_headers())
        response.raise_for_status()

        return response.json()['freq']

    def get_timeseries(self, feature, entity=None, from_date=None, to_date=None, freq=None):
        """Gets feature timeseries from feature store.

        Parameters
        ----------
        feature : str or list[str]
            Feature or list of features.
        entity : str or list[str] or list[list] or list[list, None, list, ...], optional
            Entities to filter on. If feature is singular, entity is a str, or a list of entities to filter on. If getting list of features, entity is list[str],
            this filter is applied to each feature in list, if entity is list[list] each feature is filtered by corresponding list of entities. To indicate that 
            a feature in the list isn't to be filtered by entity, include an empty list ([]) or None.
        from_date : str, optional
            A datetime string.
        to_date : str, optional
            A datetime string.
        freq : str, optional
            A freq string using pandas/datetime conventions, e.g. '1H'.

        Returns
        -------
        pd.DataFrame
            A pandas dataframe of specified data from the feed. 

        Examples
        --------
        >>> bytehub.get_timeseries('weather', entity='London', from_date='2020-01-01 9:00', to_date='2020-01-01 17:00', freq='1H')

        """

        if not isinstance(feature, list):
            feature = [feature]
        exists = self.feature_exists(feature)
        assert all(
            exists), f'The feature(s), {", ".join(list(itertools.compress(feature, map(operator.not_, exists))))}, non-existent.'

        assert isinstance(entity, str) or isinstance(
            entity, list) or entity is None, 'Entity should be of type, str or list[str] or None'
        if entity:
            if not isinstance(entity, list):
                entity = [entity]

        assert from_date is not None, 'from_date cannot be, None. Use bytehub.get_first() to define from_date.'

        if to_date is None:
            to_date = pd.Timestamp.utcnow()

        url = self.endpoint + f'timeseries'
        params = {
            'feature': ','.join(feature),
            'from_date': pd.Timestamp(from_date).isoformat(),
            'to_date': pd.Timestamp(to_date).isoformat(),
            'freq': freq,
            'entity': ','.join(entity) if entity else None
        }
        response = requests.get(
            url, params=params, headers=self._api_headers())
        response.raise_for_status()

        df = pd.DataFrame(response.json())
        if df.empty:
            return pd.DataFrame(
                {
                    col: []
                    for col in ['time', 'entity', *feature]
                }
            )

        df['time'] = pd.to_datetime(df.time, utc=True, unit='ms')

        return df

    def save_timeseries(self, feature, df):
        """Saves a dataframe of timeseries values to the feature store.

        Parameters
        ----------
        feature : str
            A feature name.
        df: pd.DataFrame
            A Pandas Dataframe of timeseries values to save.
            Must contain columns: time, value.
            Optionally can contain columns: entity, created_time.

        Examples
        --------
        >>> bytehub.save_timeseries('weather.actual', df)
        """

        assert isinstance(feature, str), 'Must save to a single feature'
        assert self.feature_exists(feature), 'Feature does not exist.'
        assert isinstance(
            df, pd.DataFrame), 'Must supply a DataFrame of feature values'
        assert 'time' in df.columns, 'No time column available in DataFrame'
        assert 'value' in df.columns, 'No value column available in DataFrame'
        assert not set(df.columns) - set(['time', 'entity', 'value',
                                          'created_time']), 'Extraneous columns in DataFrame'
        assert is_datetime(
            df.time), 'In DataFrame, time column must be a datetime'
        if 'created_time' in df.columns:
            assert is_datetime(
                df.create_time), 'In DataFrame, time column must be a datetime'

        # Convert to JSON
        payload = json.loads(df.to_json(orient='records'))

        feature_id = self.get_feature_id(feature)
        url = self.endpoint + f'timeseries/{feature_id}'
        response = requests.post(
            url, json=payload, headers=self._api_headers())
        response.raise_for_status()

    def create_feature(self, name, **kwargs):
        """Adds a feature to the feature store.

        Parameters
        ----------
        feature : str
            Feature name.

        kwargs : dict, optional
            Data to be added to metadata. 

        Examples
        --------
        >>> bytehub.create_feature('weather.actuals', source='NOAA GFS')

        """

        assert isinstance(name, str), 'Feature names should be type, str.'
        assert bool(re.match(r'^[a-zA-Z0-9\./#_-]+$', name)), 'Feature name must only contain alphanumeric .#_-'
        assert not self.feature_exists(name), 'Feature already exists.'

        payload = {
            'name': name,
            'metadata': kwargs
        }
        url = self.endpoint + f'feature'
        response = requests.post(
            url, json=payload, headers=self._api_headers())
        response.raise_for_status()

        data = response.json()

    def delete_feature(self, name):
        """Deletes a feature from the feature store.

        Parameters
        ----------
        feature : str
            Feature name.

        Examples
        --------
        >>> bytehub.delete_feature('weather.actuals')

        """

        assert isinstance(name, str), 'Feature names should be type, str.'
        assert self.feature_exists(name), 'Feature does not exist.'
        
        feature_id = self.get_feature_id(name)
        url = self.endpoint + f'feature/{feature_id}'
        response = requests.delete(url, headers=self._api_headers())
        response.raise_for_status()

    def update_feature(self, name, **kwargs):
        """Update a feature in the feature store.

        Parameters
        ----------
        feature : str
            Feature name.

        kwargs : dict, optional
            Data to be added to metadata.

        Examples
        --------
        >>> bytehub.create_feature('weather.actuals', source='NOAA GFS')

        """

        assert isinstance(name, str), 'Feature names should be type, str.'
        assert self.feature_exists(name), 'Feature does not exist.'

        payload = {
            'name': name,
            'metadata': kwargs
        }
        feature_id = self.get_feature_id(name)
        url = self.endpoint + f'feature/{feature_id}'
        response = requests.patch(
            url, json=payload, headers=self._api_headers())
        response.raise_for_status()

        data = response.json()

    def create_feature_group(self, name, **kwargs):
        """Adds a feature group to the feature store.

        Parameters
        ----------
        feature : str
            Feature group name.

        kwargs : dict, optional
            Data to be added to metadata.

        Examples
        --------
        >>> bytehub.create_feature('weather.actuals', source='NOAA GFS')

        """

        feature_ids = []

        payload = {
            'name': name,
            'feature_ids': feature_ids,
            'metadata': kwargs
        }
        url = self.endpoint + f'feature_group'
        response = requests.post(
            url, json=payload, headers=self._api_headers())
        response.raise_for_status()

        data = response.json()
