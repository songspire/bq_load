# BQ Load
Google cloud function to load data from GCS into BigQuery

## Installation
Use provide Terraform script

Note: The bucket is created with a lifecycle policy which deletes all objects older than 1 day. To avoid deleting any bq_load.conf files, Place a [temparary hold](https://cloud.google.com/storage/docs/holding-objects#place-object-hold) on each bq_load.conf object in your buckect so that these are not deleted by the bucket's lifecycle policy. 

## Usage
