from bqload import LoadTaskList

# gcs = None
# bq = None
# jobList = None
taskList = LoadTaskList()

def books_load(event, context):
    global taskList

    # if jobList == None:
    #     jobList = LoadJobList()

    taskList.process_task(event['bucket'], event['name'])


# if __name__=='__main__':
#     event = {'bucket': 'tmp2-271812-test', 'contentLanguage': 'en', 'contentType': 'text/csv', 'crc32c': 'VpXZyg==', 'etag': 'CNiurYP26ugCEAE=', 'generation': '1586970558682968', 'id': 'tmp2-271812-test/ext_books/books1.csv/1586970558682968', 'kind': 'storage#object', 'md5Hash': 'ks3W0OXi7EA4vUaqNB7odQ==', 'mediaLink': 'https://www.googleapis.com/download/storage/v1/b/tmp2-271812-test/o/ext_books%2Fbooks1.csv?generation=1586970558682968&alt=media', 'metageneration': '1', 'name': 'ext_books/books1.csv', 'selfLink': 'https://www.googleapis.com/storage/v1/b/tmp2-271812-test/o/ext_books%2Fbooks1.csv', 'size': '43573', 'storageClass': 'STANDARD', 'timeCreated': '2020-04-15T17:09:18.682Z', 'timeStorageClassUpdated': '2020-04-15T17:09:18.682Z', 'updated': '2020-04-15T17:09:18.682Z'}
#     context = {"event_id": "1124110157864995", "timestamp": "2020-04-15T17:09:19.273Z", "event_type": "google.storage.object.finalize", "resource": {'service': 'storage.googleapis.com', 'name': 'projects/_/buckets/tmp2-271812-test/objects/ext_books/books1.csv', 'type': 'storage#object'}}

#     testf1(event, context)

#     event['name']='ext_books/books2.csv'
#     testf1(event, context)

#     event['name']='ext_books/bq_load.conf'
#     testf1(event, context)