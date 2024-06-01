---
linktitle: More than 1 container app
summary: Traditional, virtualized, and container deployment are the evolution steps toward an agile infrastructure.  
weight: 4

date: 2020-04-21
lastmod: 2020-21-14
draft: false # Is this a draft? true/false
type: docs # Do not modify.
toc: true

menu:
  containerization:
    parent: Docker
    weight: 44
---

## Lesson Notes

[Dockerization Lesson Notes](../03-more-than-1-container-app_notes.pdf)

[Dockerization Lesson Presentation](../03-more-than-1-container-app_presentation.pdf)

## Video

{{< youtube NwMhAXVIOZg >}}


## Docker default bridge network

* What if we have an application with more than one container.
*  Ex; WordPress rich content management system uses apache httpd and mysql servers.
*  `-e, --env list` Set environment variables.
```bash
docker run --name mysql -e MYSQL_ROOT_PASSWORD=P@ssw0rd -d mysql:5.7
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=P@ssw0rd \
       -d mysql:5.7
hostname
# hostname.lan
docker run -it --rm mysql:5.7 mysql -hhostname.lan -uroot -pP@ssw0rd
docker run -it --rm mysql:5.7 mysql -h"$(hostname)" -uroot -pP@ssw0rd
# OR
docker run -it --rm mysql:5.7 mysql -h`hostname` -uroot -pP@ssw0rd
```

## User-defined bridge network

![User-defined bridge network](../User-defined-bridge-network.png)

* User-defined bridges provide automatic DNS resolution between containers.
*  User-defined bridges provide better isolation.
* Containers can be attached and detached from user-defined networks on the fly.
* Each user-defined network creates a configurable bridge.
* Linked containers on the default bridge network share environment variables.

## Docker Network Commands 
* `create` Create a network.
* `ls` List networks.
* `connect` Connect a container to a network.
* `inspect` Display detailed information on one or more networks.
* `rm` Deletes one or more networks.
 ```bash
docker network create wp-network
docker network connect wp-network mysql
docker network inspect wp-network
docker run --name wordpress --network wp-network -p 8080:80 \
       -e WORDPRESS_DB_HOST=mysql -e WORDPRESS_DB_NAME=wp_db \
       -e WORDPRESS_DB_USER=root -e WORDPRESS_DB_PASSWORD=P@ssw0rd \
       -d wordpress
docker network inspect wp-network
docker network rm wp-network
```
