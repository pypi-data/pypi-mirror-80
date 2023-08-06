import json
import pickle
import elasticsearch
import psycopg2
from google.cloud.storage import Client

class ElasticsearchClient:
    
    def __init__(self, host, user, password):
        """Instantiate an elasticsearch client.
        
        Parameters
        ----------
        host: str
        user: str
        password: str

        Returns
        -------
        An elasticsearch client.
        """

        self.host = host
        self.user = user
        self.password = password
        
        try:
            es = self._connect()
            if es.ping():
                self._es = es
        except:
            raise ConnectionError(f"Connection to {self.host} failed")
    
    def _connect(self):
        return elasticsearch.Elasticsearch(
            hosts=[self.host],
            http_auth=(self.user, self.password),
            send_get_body_as='POST'
        )
        
    def query(self, index, body):
        return self._es.search(index=index, body=body)
         
class DatabaseClient:

    def __init__(self, host, database, user, password, port=5432):
        """Instantiate a PostgreSQL client.
        
        Parameters
        ----------
        host: str
        database: str
        user: str
        password: str
        port: int

        Returns
        -------
        A PostgreSQL client.
        """
        
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        
        try:
            conn = self._connect()
            conn.close()
        except:
            raise ConnectionError(f"Connection to {self.host} failed")
    
    def _connect(self):
        return psycopg2.connect(**self.__dict__)

    def query(self, query_):

        conn = None

        try:            
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(query_)
            return cursor.fetchall()
        
        except:
            raise
            
        finally:            
            if conn:
                cursor.close()
                conn.close()
    
class GCSClient:
    
    def __init__(self, bucket):
        """Instantiate a Google Cloud Storage client.
        
        Parameters
        ----------
        bucket: str

        Returns
        -------
        A Google Cloud Storage client.
        """
        self.bucket = bucket
        self._client = self._connect()
        
    def _connect(self):
        return Client()
    
    def download(self, blob):
        return self._client.get_bucket(self.bucket).get_blob(blob)

    def upload(self, blob, obj):
        try:
            self._client.get_bucket(self.bucket).blob(blob).upload_from_string(
                data=json.dumps(obj),
                content_type='application/json'
            )
        except TypeError:
            self._client.get_bucket(self.bucket).blob(blob).upload_from_string(
                data=pickle.dumps(obj),
                content_type='application/octet-stream'
            )
        except Exception as e:
            raise e