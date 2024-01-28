# weather_scraper stack

## Assignment for DIA Devops Engineer Technical Task

### The following Microservices are included in this repo

Scrapper application developed in Python,  

Kafka consumer application developed in Python 

IPFS weather scraper developed in Bash

Apache Kafka, [taken from Bitnami Docker hub repo](https://hub.docker.com/r/bitnami/kafka/tags).

Zookeeper,  [taken from Bitnami Docker hub repo](https://hub.docker.com/r/bitnami/zookeeper/tags).

IPFS node, [taken from Docker hub repo](https://hub.docker.com/r/ipfs/go-ipfs).

Grafana and Prometheus (https://github.com/prometheus-operator/kube-prometheus).


All of the applications have been containerized and deployed to Minikube kubernetes cluster.


### Deployment process

First off, make sure that minikube cluster is running:
```
Minikube start
Minikube status
```

Then start by depoying the application in the following manner;

1. Deploy Zookeeper
  ```
  kubectl apply -f zookeeper-service.yaml  
  kubectl apply 
  ```







``` test ``` 
