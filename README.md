# weather_scraper stack

## Assignment for DIA Devops Engineer Technical Task

### The following Microservices are included in this repo

* Scrapper application developed in Python,  

* Kafka consumer application developed in Python 

* IPFS-client scraper developed in Bash

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
  This will deploy kafka kubernetes service, pvc, and deployment. In case the pod of kafka has to restart, the data will not be lost as it is stored in the pvc. 

3. Deploy PostgresQL application
  ```
  kubectl apply -f kafka-deployment.yaml    
  ```
  This will deploy the PostgreQL kubernetes service, pvc and statefulset. In case the pod of postgres has to restart, the data will not be lost as it is stored in the pvc. 

4. Deploy Scraper (located under scraper folder)
  ```
  kubectl apply -f scraper.yml  
  ```
  The scraper python application is scraping weather information from 5 different cities using wittr (https://github.com/chubin/wttr.in), it is scheduled to scrape this information every 10 minutes and send this information as json to kafka server   with the topic of temperature.
  The app is dockerized and pushed to my own docker hub repo(docker.io/shpookas/scraper:4) 
  After the execution of the command the application will be deployed as kubernetes deployment. 

5. Deploy Kafka Consumer (located under consumer folder)
  ```
  kubectl apply -f consumer.yml  
  ```
  Kafka Consumer application will connect to the kafka server to take the data that the scraper produced in json format. Then it will connect to the PostgresQL database to create a new table (if it not exist) and insert all the data that is coming   in from the scraper. 
  After the execution of the command the application will be deployed as kubernetes deployment. 

6. Deploy IPFS server (located under ipfs folder)
  ```
  kubectl apply -f ipfs.yml  
  ```
  This will deploy IPFS Service and Statefulset and initialize the ipfs daemon to run. In case the pod of ipfs has to restart, the data will not be lost as it is stored in the pvc.

7. Deploy the IPFS client (located under ipfs folder)
  ```
  kubectl apply -f scraper-deployment.yml
  ```
  The client is deployed as a kubernetes deployment. If the user wants to trigger the script, the user has to execute inside into this container and navigate to /usr/local/bin/ where the  ``` scraper-bash-ipfs.sh ``` script is located. After this    is done the script will scrape the weather from 5 different cities and send all data to IPFS server, the output will provide a unique CID for the location of the files. 
  ```
  root@ipfs-client-6686477d6c-nhn5w:/usr/local/bin# ./scraper-bash-ipfs.sh 
  Added weather data for all cities to IPFS with CID: QmRx8sfRi1W2uamaxgiUMnvLpvA9zXfSJwkd8aDWYq2WRP
  ```
8. Deploy the Prometheus and Grafana stack for monitoring.
   This was done with the help of helm repos
 ```
 helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
 helm repo update
 helm install stable prometheus-community/kube-prometheus-stack
 ```
After the deployment is complete, one can port-forward to the grafana server(local port 3000 to grafana port 3000) and then create a SSH tunnel from local machine to the Hetzner server(local port 8080, remote port 3000)
 ```
 kubectl port-forward <grafana-pod-name> 3000:3000
 ssh -L 8080:localhost:3000 evaluator@159.69.1.218
 ```
 This will allow one to connect to grafana server locally on your machine by accessing ( http://localhost:8080/)
 I've created a number of dashboards to track the health of the Minikube node and another dashboard to track if the data inside of postgresql is coming in regularly as expected (every 10 minutes).
 The data of grafana is stored on a PVC so even if the pod will restart, the data will not be lost. 
   
   
