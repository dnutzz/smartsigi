# smartsigi
smart home application for viewing various sensor data within the local network 

## Description
todo: sensor setup mit rasp beschreiben

A small flask backend then serves as a connector for a progressive web app, which is accessible within the local network.
## Requirements
- docker

## Setup
https://docs.docker.com/compose/install/

## Start
`docker-compose up --build`

## Troubleshooting
To reinstatite the sql setup, use 
`docker-compose down -v `
first before building with the startup command.