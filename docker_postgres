#!/bin/bash
sudo docker pull sameersbn/postgresql:9.4-21
# run the image with data volume
sudo docker run --name postgresql -itd --restart always --publish 5432:5432 --volume /srv/docker/postgresql:/var/lib/postgresql --env 'DB_NAME=dukanty' --env 'DB_USER=dukantyadmin' --env 'DB_PASS=douh0115373730' sameersbn/postgresql:9.4-21