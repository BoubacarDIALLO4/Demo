# nfs_client

## Objective

- setup nfs on central station
- mount buffer result folder from the edge stations on /storage/buffer/<name of edge station> 
- mount archived results folder from the edge stations on /storage/archive/<name of edge station> 
- the results in the buffer directory will be uploaded to the datalake by the Nifi agent and moved to the archive directory afterward.
