---
linktitle: Long-lived containers
summary: Traditional, virtualized, and container deployment are the evolution steps toward an agile infrastructure.  
weight: 3

date: 2020-04-21
lastmod: 2020-21-14
draft: false # Is this a draft? true/false
type: docs # Do not modify.
toc: true

menu:
  containerization:
    parent: Docker
    weight: 33
---

## Lesson Notes

[Dockerization Lesson Notes](../02-long-lived-containers_notes.pdf)

[Dockerization Lesson Presentation](../02-long-lived-containers_presentation.pdf)

## Video

{{< youtube Z2XD1kzqYcc >}}

## Docker In Terminal - Long Lived Containers

* `-d, --detach` Run container in background and print container ID.
```bash
docker run --rm httpd
# AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 172.17.0.2. Set the 'ServerName' directive globally to suppress this message
# AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 172.17.0.2. Set the 'ServerName' directive globally to suppress this message
# [Sat Apr 18 01:31:07.312598 2020] [mpm_event:notice] [pid 1:tid 140057600050304] AH00489: Apache/2.4.43 (Unix) configured -- resuming normal operations
# [Sat Apr 18 01:31:07.312772 2020] [core:notice] [pid 1:tid 140057600050304] AH00094: Command line: 'httpd -D FOREGROUND'
docker run --rm -d httpd
```

* **port** List port mappings or a specific mapping for the container
* `-p, --publish list` Publish a container's port(s) to the host.
```bash
docker run -d httpd
docker run -d httpd
docker run -d httpd
docker run --rm -d httpd
docker run --rm -d -p 80:80 httpd
docker run --rm -d -p 8080:80 httpd
docker port nervous_lamarr
# 80/tcp -> 0.0.0.0:8080
```

* ![Docker Bridge Networking](../02-bridge-networking.png)

* **logs** Fetch the logs of a container.
* `-t, --timestamps` Show timestamps.
* `-f, --follow` Follow log output.
```bash
docker logs nervous_lamarr
# AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 172.17.0.6. Set the 'ServerName' directive globally to suppress this message
# AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using 172.17.0.6. Set the 'ServerName' directive globally to suppress this message
# [Sat Apr 18 18:02:11.771692 2020] [mpm_event:notice] [pid 1:tid 139892595709056] AH00489: Apache/2.4.43 (Unix) configured -- resuming normal operations
# [Sat Apr 18 18:02:11.772107 2020] [core:notice] [pid 1:tid 139892595709056] AH00094: Command line: 'httpd -D FOREGROUND'
# 172.17.0.1 - - [18/Apr/2020:18:03:02 +0000] "GET / HTTP/1.1" 200 45
# 172.17.0.1 - - [18/Apr/2020:18:03:02 +0000] "GET /favicon.ico HTTP/1.1" 404 196
docker logs -t nervous_lamarr
docker logs -f nervous_lamarr
```

* **restart**     Restart one or more containers
* `-t, --time int` Seconds to wait for stop before killing the container (default 10).
```bash
docker restart nervous_lamarr
# nervous_lamarr
docker ps -a
# CONTAINER ID    IMAGE    COMMAND              CREATED           STATUS          PORTS                  NAMES
# 89d48b6635c3    httpd    "httpd-foreground"   36 minutes ago    Up 3 seconds    0.0.0.0:8080->80/tcp   nervous_lamarr
# 357e2aafd0d3    httpd    "httpd-foreground"   40 minutes ago    Up 40 minutes   0.0.0.0:80->80/tcp     gallant_lewin
docker restart -t 5 nervous_lamarr
# nervous_lamarr
```

* **stop** Stop one or more running containers.
* `-t, --time int` Seconds to wait for stop before killing it (default 10).
```bash
docker stop cranky_chatterjee
# cranky_chatterjee
docker ps -a
# CONTAINER ID    IMAGE    COMMAND              CREATED           STATUS                      NAMES
# d16271db5d73    httpd    "httpd-foreground"   17 minutes ago    Exited (0) 3 seconds ago    cranky_chatterjee
docker rm cranky_chatterjee
# cranky_chatterjee
docker stop -t 5 cool_spence
# cool_spence
docker rm cool_spence
# cool_spence
```

* **kill** Kill one or more running containers.
```bash
docker kill gracious_jang
# gracious_jang
docker rm gracious_jang
# gracious_jang
```

* **stats** Display a live stream of container(s) resource usage statistics.
* `-a, --all` Show all containers (default shows just running).
* `--no-stream` Disable streaming stats and only pull the first result.
```bash
docker stats nervous_lamarr
# CONTAINER ID    NAME              CPU %    MEM USAGE / LIMIT     MEM %    NET I/O            BLOCK I/O    PIDS
# 89d48b6635c3    nervous_lamarr    0.01%    6.109MiB / 1.943GiB   0.31%    9.29kB / 4.54kB    0B / 0B      82
docker stats -a
# CONTAINER ID    NAME              CPU %    MEM USAGE / LIMIT     MEM %    NET I/O            BLOCK I/O    PIDS
# 89d48b6635c3    nervous_lamarr    0.01%    6.109MiB / 1.943GiB   0.31%    9.29kB / 4.54kB    0B / 0B      82
# 357e2aafd0d3    gallant_lewin     0.02%    5.996MiB / 1.943GiB   0.30%    2.01kB / 558B      0B / 0B      82
docker stats -a --no-stream
```

* **top** Display the running processes of a container
```bash
docker top nervous_lamarr
# PID     USER    TIME    COMMAND
# 3634    root    0:00    httpd -DFOREGROUND
# 3668    bin     0:00    httpd -DFOREGROUND
# 3669    bin     0:00    httpd -DFOREGROUND
# 3670    bin     0:00    httpd -DFOREGROUND
```

* **pause** Pause all processes within one or more containers
* **unpause** Unpause all processes within one or more containers
```bash
docker pause nervous_lamarr
# nervous_lamarr
docker ps -a
# CONTAINER ID    IMAGE    COMMAND              CREATED           STATUS                   PORTS                  NAMES
# 89d48b6635c3    httpd    "httpd-foreground"   36 minutes ago    Up 36 minutes (Paused)   0.0.0.0:8080->80/tcp   nervous_lamarr
# 357e2aafd0d3    httpd    "httpd-foreground"   40 minutes ago    Up 40 minutes            0.0.0.0:80->80/tcp     gallant_lewin
docker unpause nervous_lamarr
# nervous_lamarr
docker ps -a
# CONTAINER ID    IMAGE    COMMAND              CREATED           STATUS          PORTS                  NAMES
# 89d48b6635c3    httpd    "httpd-foreground"   36 minutes ago    Up 36 minutes   0.0.0.0:8080->80/tcp   nervous_lamarr
# 357e2aafd0d3    httpd    "httpd-foreground"   40 minutes ago    Up 40 minutes   0.0.0.0:80->80/tcp     gallant_lewin
```

* **exec** Run a command in a running container.
* `-i, --interactive` Keep STDIN open even if not attached.
* `-t, --tty` Allocate a pseudo-TTY.
```bash
docker exec  nervous_lamarr /bin/ls
docker exec nervous_lamarr /bin/bash
docker ps -a
# CONTAINER ID    IMAGE    COMMAND              CREATED           STATUS          PORTS                  NAMES
# 89d48b6635c3    httpd    "httpd-foreground"   36 minutes ago    Up 36 minutes   0.0.0.0:8080->80/tcp   nervous_lamarr
# 357e2aafd0d3    httpd    "httpd-foreground"   40 minutes ago    Up 40 minutes   0.0.0.0:80->80/tcp     gallant_lewin
docker exec -i nervous_lamarr /bin/bash
docker ps -a
# CONTAINER ID    IMAGE    COMMAND              CREATED           STATUS          PORTS                  NAMES
# 89d48b6635c3    httpd    "httpd-foreground"   36 minutes ago    Up 36 minutes   0.0.0.0:8080->80/tcp   nervous_lamarr
# 357e2aafd0d3    httpd    "httpd-foreground"   40 minutes ago    Up 40 minutes   0.0.0.0:80->80/tcp     gallant_lewin
docker exec -i -t nervous_lamarr /bin/bash
# root@89d48b6635c3:/usr/local/apache2# cat htdocs/index.html
# <html><body><h1>It works!</h1></body></html>
# root@89d48b6635c3:/usr/local/apache2# exit
# exit
docker ps -a
# CONTAINER ID    IMAGE    COMMAND              CREATED           STATUS          PORTS                  NAMES
# 89d48b6635c3    httpd    "httpd-foreground"   36 minutes ago    Up 36 minutes   0.0.0.0:8080->80/tcp   nervous_lamarr
# 357e2aafd0d3    httpd    "httpd-foreground"   40 minutes ago    Up 40 minutes   0.0.0.0:80->80/tcp     gallant_lewin
```

* **cp** Copy files/folders between a container and the local filesystem
```bash
docker cp nervous_lamarr:/usr/local/apache2/htdocs/index.html .
vim index.html
docker cp index.html nervous_lamarr:/usr/local/apache2/htdocs/index.html
```

* **wait** Block until one or more containers stop, then print their exit codes.
```bash
docker wait nervous_lamarr
# 0
docker stop nervous_lamarr
# nervous_lamarr
```

* **attach** Attach local standard input, output, and error streams to a running container.
```bash
docker attach gallant_lewin
```
