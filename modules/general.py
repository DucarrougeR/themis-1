import configparser
import re
import os
from os import path

def get_looker_version(looker_client):
    '''Returns the version for the Looker instance'''
    return looker_client.versions(fields='looker_release_version').looker_release_version

def regex_base_url(url):
    '''Cleans instance URL from eventual trailing ports in API URL'''
    return re.sub(r':\d{2,6}.*', '', url)

def get_looker_instance():
    '''Returns the base URL for the Looker instance'''
    if path.exists("looker.ini"): 
        config = configparser.ConfigParser()
        config.read('looker.ini')
        config_details = dict(config['Looker'])
        return regex_base_url(config_details['base_url'])
    else:
        LOOKERSDK_BASE_URL = os.environ.get('LOOKERSDK_BASE_URL')
        return regex_base_url(LOOKERSDK_BASE_URL)

def format_output(function_results):
    '''Formats list of errors in Looker to display first 20 elements'''
    if isinstance(function_results, (list)):
        if len(function_results) < 1:
            return ['No issues found.']
        formatted_results = function_results[:20]
        formatted_results.append('...')
        return formatted_results
    elif isinstance(function_results, (tuple)): 
        formatted_results = list(function_results)[:20]
        formatted_results.append('...')
        return formatted_results
    else:
        return function_results