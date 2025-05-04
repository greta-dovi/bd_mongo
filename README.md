### Assignment 3
Note: I used "aisdk-2025-01-23.csv" dataset for this task. <br>

##### NoSQL Database cluster
NoSQL database cluster was set up on my local machine using MongoDB and Docker. The sharded set up was created in the following way: <br>
- Create a `docker-compose.yml` file indicating the following structure: 3 config servers, 2 shards each containing 3 nodes (3 to assure data accessibility in case one node goes down) and mongos router. 
- Start the cluster using command `docker compose up -d`. Assure that docker desktop program is running.
- Initialize config server and shard replica sets, then connect them to the router. Run the following commands:
    - 123
