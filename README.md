### discovery-agent
```sh
$ cd discovery-agent
$ docker build -t discovery-agent .
$ docker run -it -p 80:80 --name discovery-agent discovery-agent
```

### worker
```sh
$ cd worker
$ docker build -t worker .
$ docker run -it --link discovery-agent:haproxy worker
```
