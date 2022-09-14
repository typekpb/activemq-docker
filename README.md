# activemq-docker

Sources are available at GitHub: [typekpb/activemq-docker](https://github.com/typekpb/activemq-docker)

[![Docker Pulls](https://img.shields.io/docker/pulls/butkovic/activemq.svg?maxAge=2592000)](https://hub.docker.com/r/butkovic/activemq/)

## Credits

Please note, the repo itself got heavily inspired by the https://github.com/rmohr/docker-activemq.
Just a bit more automation of new image releases provided.

## Running
Run the latest container with:
```commandline
docker pull butkovic/activemq
docker run -p 61616:61616 -p 8161:8161 butkovic/activemq
The JMX broker listens on port 61616 and the Web Console on port 8161.
```

## Port Map

* 61616 JMS
* 8161  UI
* 5672  AMQP  
* 61613 STOMP 
* 1883  MQTT  
* 61614 WS    

## Customizing configuration and persistence location
By default data and configuration is stored inside the container and will be lost after the container has been shut down and removed. To persist these files you can mount these directories to directories on your host system:

```
docker run -p 61616:61616 -p 8161:8161 \
           -v /your/persistent/dir/conf:/opt/activemq/conf \
           -v /your/persistent/dir/data:/opt/activemq/data \
           butkovic/activemq
```

ActiveMQ expects that some configuration files already exists, so they won't be created automatically, instead you have to create them on your own before starting the container. If you want to start with the default configuration you can initialize your directories using some intermediate container:

```
docker run --user root --rm -ti \
  -v /your/persistent/dir/conf:/mnt/conf \
  -v /your/persistent/dir/data:/mnt/data \
  butkovic/activemq:5.15.4-alpine /bin/sh
```

This will bring up a shell, so you can just execute the following commands inside this intermediate container to copy the default configuration to your host directory:
```
chown activemq:activemq /mnt/conf
chown activemq:activemq /mnt/data
cp -a /opt/activemq/conf/* /mnt/conf/
cp -a /opt/activemq/data/* /mnt/data/
exit
```
The last command will stop and remove the intermediate container. Your directories are now initialized and you can run ActiveMQ as described above.
