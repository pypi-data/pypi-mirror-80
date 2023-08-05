# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import random
import string
import logging
from ..utils import utils


class ModelData(object):
    def __init__(self, obj_type, **kwargs):
        self.type = obj_type
        self.kwargs = kwargs
        self.data = {}

        if obj_type == "Network":
            self.data_base = {
                "name": utils.random_string(min=1, max=64),
                "description": utils.random_string(min=0, max=1024),
            }
        elif obj_type == "Connection":
            # If no connection 'type' specified, default 'SITE_IPSEC_VPN'
            self.conn_type = kwargs.get("type", "SITE_IPSEC_VPN")
            self.data_base = {
                "type": self.conn_type,
                "name": utils.random_string(min=1, max=64),
                "billing_term": random.choice(
                    ["HOURLY", "MONTHLY", "ONE_YEAR", "TWO_YEAR"]
                ),
                "high_availability": random.choice([True, False]),
                "location": {"href": utils.random_string(min=1, max=64)},
                "speed": random.choice(
                    [50, 100, 200, 300, 400, 500, 1000, 2000, 5000, 10000]
                ),
            }
            if self.conn_type == "SITE_IPSEC_VPN":
                self.data_type = {
                    "routing_type": random.choice(
                        ["POLICY_BASED", "ROUTE_BASED_STATIC", "ROUTE_BASED_BGP"]
                    ),
                    "primary_customer_router_ip": utils.random_string(min=15, max=20),
                    "auth_type": "PSK",
                    "ike_version": random.choice(["V1", "V2"]),
                    "ike_v2": {
                        "esp": {
                            "dh_group": "MODP_2048",
                            "encryption": "AES_128",
                            "integrity": "SHA256_HMAC",
                        },
                        "ike": {
                            "dh_group": "MODP_2048",
                            "encryption": "AES_128",
                            "integrity": "SHA256_HMAC",
                        },
                    },
                    "customer_asn": utils.random_int(min=1, max=65000),
                }

            elif self.conn_type == "AZURE_EXPRESS_ROUTE":
                self.data_type = {"service_key": utils.random_string(min=1, max=64)}

            elif self.conn_type == "AWS_DIRECT_CONNECT":
                self.data_type = {
                    "aws_account_id":
                        "".join(random.choice(string.digits) for _ in range(12)),
                    "aws_region": utils.random_string(min=1, max=64),
                }
            elif self.conn_type == "GOOGLE_CLOUD_INTERCONNECT":
                self.data_type = {
                    "primary_pairing_key": utils.random_string(min=1, max=64),
                    "secondary_pairing_key": utils.random_string(min=1, max=64),
                }
            elif self.conn_type == "ORACLE_FAST_CONNECT":
                self.data_type = {
                    "primary_ocid": utils.random_string(min=1, max=256),
                    "secondary_ocid": utils.random_string(min=1, max=256),
                    "cloud_region": utils.random_string(min=1, max=64),
                    "peering": {
                        "primaryPureportBgpIP": utils.random_string(min=1, max=64),
                        "primaryRemoteBgpIP": utils.random_string(min=1, max=64),
                        "secondaryPureportBgpIP": utils.random_string(min=1, max=64),
                        "secondaryRemoteBgpIP": utils.random_string(min=1, max=64),
                        "type": "PRIVATE",
                    },
                }

            self.data_base.update(self.data_type)

        else:
            self.data_base = {}
            logging.error(
                "Error: model_data object type {} not supported".format(obj_type)
            )

        self.data = self._override_attributes(self.data_base, **kwargs)

        logging.info("Models object data: {}".format(self.data))

    def _override_attributes(self, base, **kwargs):
        if "remove" in kwargs:
            for attr in kwargs.keys():
                if attr in base and attr != "type":
                    del base[attr]
        else:
            # Actions:  override attribute if it already exists OR
            # insert attribute if not (negative); log both at INFO
            for attr in kwargs.keys():
                if attr in base and attr != "type":
                    logging.info(
                        "INFO: Overriding attribute {}:{}".format(attr, kwargs[attr])
                    )
                    base[attr] = kwargs[attr]
                elif attr != "type":
                    logging.info(
                        "INFO: Inserting new attribute {}:{}".format(attr, kwargs[attr])
                    )
                    base[attr] = kwargs[attr]
        return base
