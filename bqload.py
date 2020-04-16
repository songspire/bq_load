from configparser import ConfigParser
from google.oauth2 import service_account
from google.cloud import storage
from google.cloud import bigquery

class LoadTaskList:
    def __init__(self, service_account_file_name='', config_name: str = 'bq_load.conf'):
        self.config_registry = {}
        if service_account_file_name:
            credentials = service_account.Credentials.from_service_account_file( 
                service_account_file_name, 
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )

            self.gcs = storage.Client(
                credentials=credentials,
                project=credentials.project_id,
            )

            self.bq = bigquery.Client(
                credentials=credentials,
                project=credentials.project_id,
            )
        else:
            self.gcs = storage.Client()
            self.bq = bigquery.Client()

        self.config_name = config_name

    def get_config(self, bucket_name: str, object_path: str):
        base_path = '/'.join( [bucket_name, *object_path.split('/')[:-1]] )
        if base_path in self.config_registry.keys():
            return( self.config_registry.get(base_path) )
        else:
            return self.read_config(bucket_name, object_path)

    def read_config(self, bucket_name: str, object_path: str):
        config_path = '/'.join( [*object_path.split('/')[:-1], 'bq_load.conf'] )

        bucket = self.gcs.get_bucket(bucket_name)
        config_blob = bucket.blob(config_path)
        config = ConfigParser()
        config.read_string(config_blob.download_as_string().decode())

        base_path = '/'.join( [bucket_name, *object_path.split('/')[:-1]] )

        self.config_registry[base_path] = config
        return(config)

    def process_task(self, bucket_name: str, object_path: str):
        # If the config file name appear at the end of the object_path then
        # the config file itself was written i.e. modified and we need to 
        # read it in case it was cached to avoid having stale entries in the
        # config_registry. No need to load any data so just return afer that.
        if object_path.endswith(self.config_name):
            self.read_config(bucket_name, object_path)
            return

        config = self.get_config(bucket_name, object_path)

        dataset_ref = self.bq.dataset(config['load']['dataset'])
        table_ref = dataset_ref.table(config['load']['table'])
        job_config = bigquery.LoadJobConfig()
        job_config.skip_leading_rows = 1
        #ToDo: accomodate other formats than CSV
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.autodetect = True

        uri = f"gs://{bucket_name}/{object_path}"

        load_job = self.bq.load_table_from_uri(
            uri, table_ref, job_config=job_config
        )
        print("Starting job {load_job.job_id}")

        # for k in config['load']:
        #     print(k)
