#!/usr/bin/env python

import requests
import logging


class Instance:

    DATACENTERS = {
        'us-east-1': 'ash3',
        'us-west-2': 'pdx2',
        'eu-west-1': 'dub1',
        'us-east4': 'ash4',
        'us-central1': 'ord1',
        'us-west1': 'pdx4',
    }

    @staticmethod
    def get_cloud_provider(**kwargs):
        provider = ""
        if requests.get("http://169.254.169.254/").content.split("\n")[1] == "computeMetadata/":
            provider = "gcp"
        else:
            provider = "aws"
        return provider
