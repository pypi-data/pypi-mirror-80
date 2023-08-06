import os
from pynidus.clients import ElasticsearchClient, DatabaseClient, GCSClient
from pynidus.errors import ErrorLogger

class MLTBase:
    
    def __init__(self, **kwargs):
        
        es_config = kwargs.get("es_config")
        pg_config = kwargs.get("pg_config")
        gcs_config = kwargs.get("gcs_config")
        bugsnag_config = kwargs.get("bugsnag_config")

        if es_config:
            self.es_client = ElasticsearchClient(**es_config)

        if pg_config:
            self.pg_client = DatabaseClient(**pg_config)

        if gcs_config:
            self.gcs_client = GCSClient(**gcs_config)

        if bugsnag_config:
            self.error_logger = ErrorLogger(**bugsnag_config)

class MultiClient:

    def __init__(self, config):
        self._set_clients(config)

    def _set_clients(self, config):

        for client in config.keys():

            [type_, name] = client.split("_", 1)

            if type_ == "pg":

                if "pg_client" not in self.__dict__ :
                    self.pg_client = {}

                self.pg_client[name] = DatabaseClient(**config.get(client))
            
            elif type_ == "es":

                if "es_client" not in self.__dict__ :
                    self.es_client = {}

                self.es_client[name] = ElasticsearchClient(**config.get(client))

            elif type_ == "gcs":

                if "gcs_client" not in self.__dict__ :
                    self.gcs_client = {}

                self.gcs_client[name] = GCSClient(**config.get(client))

                
        

