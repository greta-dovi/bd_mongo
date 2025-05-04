### Assignment 3
Note: I used "aisdk-2025-01-23.csv" dataset for this task. <br>

##### NoSQL Database cluster
NoSQL database cluster was set up on my local machine using MongoDB and Docker. The sharded set up was created in the following way: <br>
- Create a `docker-compose.yml` file indicating the following structure: 3 config servers, 2 shards each containing 3 nodes (3 to assure data accessibility in case one node goes down) and mongos router. 
- Start the cluster using command `docker compose up -d`. Assure that docker desktop program is running.
- Initialize config server and shard replica sets, then connect them to the router. Run the following commands:
    - Initialize config replica set: `docker exec -it bd_mongo-configsvr1-1 mongosh`
    - Then in mongo shell run: `rs.initiate({_id: "configReplSet", configsvr: true, members: [ {_id: 0, host: "configsvr1:27017"},{_id: 1, host: "configsvr2:27017"}, {_id: 2, host: "configsvr3:27017"}]})`
    - Initialize shard replica sets (shard 1): `docker exec -it bd_mongo-shard1_node1-1 mongosh --port 27001`
    - `rs.initiate({_id: "shard1ReplSet", members: [{_id: 0, host: "shard1_node1:27001"}, {_id: 1, host: "shard1_node2:27002"}, {_id: 2, host: "shard1_node3:27005"}] })`
    - Initialize shard replica sets (shard 2): `docker exec -it bd_mongo-shard2_node1-1 mongosh --port 27003`
    - `rs.initiate({_id: "shard2ReplSet", members: [{_id: 0, host: "shard2_node1:27003"}, {_id: 1, host: "shard2_node2:27004"}, {_id: 2, host: "shard2_node3:27006"}] })`
    - Add the shards to the cluster via mongos: `docker exec -it bd_mongo-mongos-1 mongosh --port 27017`
    - `sh.addShard("shard1ReplSet/shard1_node1:27001,shard1_node2:27002,shard1_node3:27005")`
    - `sh.addShard("shard2ReplSet/shard2_node1:27003,shard2_node2:27004,shard2_node3:27006")`
Now the cluster is set up and running. <br>

##### Data insertion in parallel
Before data insertion, enable sharding inside the dabase abd collection:
- Check names of containers running: docker ps
- Connect to mongos router: `docker exec -it bd_mongo-mongos-1 mongosh`
- `use vesselsDB`
- `sh.enableSharding("vesselsDB")`
- `db.raw_data.createIndex({"MMSI":1})`
- `sh.shardCollection("vesselsDB.raw_data", {"MMSI":1})`
After this setup run the Python script `data_insertion.py`. <br>
Note: the parallelization task was distributed among 10 workers. <br>
Data distribution between the shards can be checked using `db.raw_data.getShardDistribution()` <br>

##### Data noise filtering in parallel
To clean the data from database, run this Python script: `data_cleaning.py`. <br>
Cleaned data is stored in a separate collection of vesselsDB database. 

##### Calculate delta t and generate historgams
To calculate delta t and generate histograms run this Python script: `delta_t_histo.py` <br>
The generated histograms show that majority of ships have very frequent location reporting (every few seconds), however, some larger intervals (in hours) do also appear.

##### Showcase MongoDB instance failure
Sharding with uneven number of nodes assures that if the minority of nodes is down, the data is still accessible. <br>
The video shows that information can be retrieved when all containers are running as well as when the absolute majority of nodes are working inside a shard. However, if absolute majority of nodes are down, the data becomes not accessible. <br>
Link to the video: <br>
https://vult-my.sharepoint.com/:v:/g/personal/greta_dovidaityte_mif_vu_lt/EdaiFEHL01NBuy6kfhNGiH4BsA1JjasQI_JrSzfDpczfRg?e=bhY2hN&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D
If link is not available, check in github repository <br>