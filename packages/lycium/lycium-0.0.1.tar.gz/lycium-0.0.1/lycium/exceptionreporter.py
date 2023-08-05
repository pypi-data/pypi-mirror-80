#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
from .singleton import singleton
from .elasticsearchsaver import ELASTICSEARCH_SAVER

LOG = logging.getLogger('async.request')

@singleton
class ExceptionReporter(object):
    """Configures address that would reports execption content to
    """
    def __init__(self):
        super().__init__()
        self.db_connector = 'es'
        self.db_category = 'exceptions'
        self.address = '127.0.0.1:9200'
        self.es_index = 'exceptions'
        self.es_doc_type = self.db_category

    def configure(self, category: str, conf: dict) -> bool:
        connector = conf.get('connector', '')
        host = conf.get('host', '127.0.0.1')
        port = int(conf.get('port', 0))
        configure_result = True
        if 'es' == connector or 'elasticsearch' == connector:
            self.db_connector = 'es'
            self.address = '%s:%d' % (host, port)
            self.es_doc_type = category
            configure_result = ELASTICSEARCH_SAVER.configure(self.address)
            if configure_result:
                # mappings = {
                #     'index_patterns': [self.es_index+'-*'],
                #     'template': {
                #         'mappings': {
                #             'properties': {
                #                 'key': { 'type': 'text' },
                #                 'type': { 'type': 'text' },
                #                 'level': { 'type': 'text' },
                #                 'endpoint': { 'type': 'text' },
                #                 'method': { 'type': 'text' },
                #                 '@timestamp': {
                #                     'type': 'date',
                #                 },
                #                 'timestamp': {
                #                     'type': 'date',
                #                 }
                #             }
                #         },
                #     }
                # }
                mappings = self.get_elasticsearch_template(self.es_index)
                configure_result = ELASTICSEARCH_SAVER.ensure_template(index=self.es_index, mappings=mappings)
        elif 'restful' == connector or 'rest' == connector:
            self.db_connector = 'restful'
            self.address = host
        else:
            LOG.error('configure exception reporter failed while unknown connector:%s', connector)
            return False
        self.db_category = category
        return configure_result

    def report(self, key: str, typ: str, endpoint: str, method: str, inputs: str, outputs: str, content: str, level: str = 'ERROR') -> bool:
        cur_date_endfix = '-' + time.strftime('%Y-%m-%d', time.localtime())
        data = {
            'key': key,
            'type': typ,
            'level': level,
            'endpoint': endpoint,
            'method': method,
            'input': inputs,
            'output': outputs,
            'content': content,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        }

        if 'es' == self.db_connector:
            data['@timestamp'] = time.time()*1000
            return ELASTICSEARCH_SAVER.save(index=self.es_index+cur_date_endfix, doc_type=self.es_doc_type, body=data)
        else:
            # not supported
            log_texts = ['%s:[%s]' % (k, k) for k, v in data.items()]
            LOG.error('reports of %s', ' '.join(log_texts))
            return False
        
    def get_elasticsearch_template(self, index: str) -> dict:
        mappings = {
            "order" : 0,
            "template": index + "-*",
            "index_patterns": [index + "-*"],
            "settings": {
                "index": {
                    "refresh_interval": "5s"
                }
            },
            "mappings": {
                # "_doc" : {
                    "dynamic_templates": [
                        {
                            "message_field": {
                                "mapping": {
                                    "fielddata": {
                                        "format": "disabled"
                                    },
                                    "index": "analyzed",
                                    "omit_norms" : True,
                                    "type": "string"
                                },
                                "match_mapping_type" : "string",
                                "match" : "content"
                            }
                        },
                        {
                            "date_fields" : {
                                "mapping" : {
                                    "fielddata" : {
                                        "format" : "disabled"
                                    },
                                    "index" : "analyzed",
                                    "omit_norms" : True,
                                    "type" : "date",
                                    "fields" : {
                                        "raw" : {
                                        "ignore_above" : 256,
                                        "index" : "not_analyzed",
                                        "type" : "string"
                                        }
                                    }
                                },
                                "match_mapping_type" : "date",
                                "match" : "@?timestamp"
                            }
                        },
                        {
                            "string_fields" : {
                                "mapping" : {
                                    "fielddata" : {
                                        "format" : "disabled"
                                    },
                                    "index" : "analyzed",
                                    "omit_norms" : True,
                                    "type" : "string",
                                    "fields" : {
                                        "raw" : {
                                        "ignore_above" : 256,
                                        "index" : "not_analyzed",
                                        "type" : "string"
                                        }
                                    }
                                },
                                "match_mapping_type" : "string",
                                "match" : "*"
                            }
                        }
                    ],
                    "_source": {
                        "enabled": False
                    },
                    "properties" : {
                        "@timestamp" : {
                            "type" : "date"
                        },
                        # "geoip" : {
                        #     "dynamic" : True,
                        #     "properties" : {
                        #     "ip" : {
                        #         "type" : "ip"
                        #     },
                        #     "latitude" : {
                        #         "type" : "float"
                        #     },
                        #     "location" : {
                        #         "type" : "geo_point"
                        #     },
                        #     "longitude" : {
                        #         "type" : "float"
                        #     }
                        #     }
                        # },
                        "@version" : {
                            "type" : "text"
                        },
                        'key': { 'type': 'text' },
                        'type': { 'type': 'text' },
                        'level': { 'type': 'text' },
                        'endpoint': { 'type': 'text' },
                        'method': { 'type': 'text' },
                        'timestamp': {
                            'type': 'date',
                        }
                    }
                # }
            },
            "aliases" : { }
        }
        return mappings
