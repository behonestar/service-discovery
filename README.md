This project is an example of service-discovery with CoreOS for microservices. `discovery-agent` refers to [docker-discover].

## Pre-requirements
- CoreOS etcd cluster on AWS EC2 Instance

## Backend
- ### redis unit
  `redis` is a backend to store key-value from workers.
  ```sh
  $ cd fleet-unit-files
  $ cp redis@.service /etc/systemd/system
  $ cd /etc/systemd/system
  $ fleetdctl start redis@1
  ```

- ### redis-register unit
  The `redis-register` is a sidekick unit of `redis` unit. It registers host, port of `redis` unit with the etcd cluster. Also it works on the same machine of `redis` unit.
  ```sh
  $ cd fleet-unit-files
  $ cp redis-register@.service /etc/systemd/system
  $ cd /etc/systemd/system
  $ fleetdctl start redis-register@1
  ```

## Worker
- ### worker
  Worker uses `haproxy:80` as a `host:port` to connect to the Redis backend.
  ```sh
  $ cd worker
  $ docker build -t worker .
  $ docker run -it --link discovery-agent:haproxy worker
  ```
  
- ### discovery-agent
  The discovery-agent gets `redis` unit info from the etcd and update `HAProxy` configurations. `HAProxy` is bound to port number `80`.
  ```sh
  $ cd discovery-agent
  $ docker build -t discovery-agent .
  $ docker run -it -p 80:80 --name discovery-agent discovery-agent
  ```


[docker-discover]: <https://github.com/joemccann/dillinger>
