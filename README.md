This project is an example of service-discovery with CoreOS for microservices. `discovery-agent` refers to [docker-discover].

## Pre-requirements
- CoreOS etcd cluster on AWS EC2 Instance

## Backend
- ### redis unit
  `redis` is a backend to store key-value from workers.
  ```sh
  $ cd redis
  $ cp redis@.service /etc/systemd/system
  $ cd /etc/systemd/system
  $ flletdctl start redis@1
  ```

- ### redis-register unit
  The `redis-register` is a sidekick unit of `redis` unit. It works on the same machine of `redis` unit. Also it registers host, port of `redis` unit with the etcd cluster. 
  ```sh
  $ cd redis-register
  $ cp redis-register@.service /etc/systemd/system
  $ cd /etc/systemd/system
  $ flletdctl start redis-register@1
  ```

## Worker
- ### worker
  Worker connects to the redis, and then set or get keys. It use `haproxy:80` as a hostname and a port of redis.
  ```sh
  $ cd worker
  $ docker build -t worker .
  $ docker run -it --link discovery-agent:haproxy worker
  ```
  
- ### discovery-agent
  The discovery-agent get `redis` unit info from etcd and update `HAProxy` configurations. `HAProxy` is bound to port number `80`.
  ```sh
  $ cd discovery-agent
  $ docker build -t discovery-agent .
  $ docker run -it -p 80:80 --name discovery-agent discovery-agent
  ```


[docker-discover]: <https://github.com/joemccann/dillinger>
