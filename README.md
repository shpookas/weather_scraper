# weather_scraper stack

## Assignment for DIA Devops Engineer Technical Task

### The following Microservices are included in this repo

* Scrapper application developed in Python,  

* Kafka consumer application developed in Python 

* IPFS weather scraper developed in Bash

* Apache Kafka, [taken from Bitnami Docker hub repo](https://hub.docker.com/r/bitnami/kafka/tags).

* Zookeeper,  [taken from Bitnami Docker hub repo](https://hub.docker.com/r/bitnami/zookeeper/tags).

* IPFS node, [taken from Docker hub repo](https://hub.docker.com/r/ipfs/go-ipfs).

* Grafana and Prometheus (https://github.com/prometheus-operator/kube-prometheus).


All of the applications have been containerized and deployed to Minikube kubernetes cluster.


### Deployment process

First off, make sure that minikube cluster is running:
```
Minikube start
Minikube status
```

Then start by depoying the application in the following manner;

1. Deploy Zookeeper (located under kafka-zookeeper folder)
  ```
  kubectl apply -f zookeeper-deployment.yaml 
  ```
  This will deploy zookeeper kubernetes service and deployment. 

2. Deploy Kafka(located under kafka-zookeeper folder) 
  ```
  kubectl apply -f kafka-deployment.yaml    
  ```
  This will deploy kafka kubernetes service, pvc, and deployment. 

3. Deploy PostgresQL application
  ```
  kubectl apply -f kafka-deployment.yaml    
  ```

3. Deploy Scraper (located under scraper folder)
  ```
  kubectl apply -f scraper.yml  
  ```
  The scraper python application is scraping weather information from 5 different cities using wittr (https://github.com/chubin/wttr.in), it is scheduled to scrape this information every 10 minutes and send this information as json to kafka server   with the topic of temperature.
  The app is dockerized and push to my own docker hub repo(docker.io/shpookas/scraper:4) 
  After the execution of the command the application will be deployed as kubernetes deployment. 

4. Deploy Kafka Consumer (located under consumer folder)
  ```
  kubectl apply -f consumer.yml  
  ```
  Kafka Consumer application will connect to the kafka server to take the data that the scraper produced in json format. Then it will connect tot 







``` test ``` 
