# simple-storage
Two ways simple interaction between cloud storage and local filesystem.

    pip install simplestorage

## Examples

### Path file/folder listing
    import simplestorage


    results = simplestorage.ls('/home/myuser/')

    print("Listing DIRECTORIES:")
    for r in results:
        if r.is_folder:
            print(r.name)

    print("Listing FILES:")
    for r in results:
        if not r.is_folder:
            print(r.name)

you can use it with cloud too

    simplestorage.ls('gs://my-bucket/someprefix')

### File Saving to local/cloud
    import simplestorage

    binary_data = b"some initial binary data: \x00\x01"
    uri = "gs://mybucket/test/binary.bin"
    simplestorage.save(data=binary_data, uri=uri)

for local just change the uri

    simplestorage.save(
        data=..., uri="/home/user/test/binary.bin")