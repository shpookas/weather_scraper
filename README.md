# Weather scraper stack

This application scrapes weather information every 10 minutes from 5 different cities, namely Zurich, London, Miami and Tokyo. The scraping is done by utilizing the [free API called wttr](https://github.com/chubin/wttr.in). 
The temperature together with the city and timestamp is stored in a PostgreSQL database and occasionally (when the user prompts) stored on the decentralized database of IPFS. 
There is monitoring stack deployed in order to track the health of the cluster and whether the data is coming in to postgres database periodically. 

### The following Microservices are included in this repo

* Scraper application developed in Python.  

* Kafka consumer application developed in Python.

* IPFS-client scraper developed in Bash.

* Apache Kafka, [taken from Bitnami Docker hub repo](https://hub.docker.com/r/bitnami/kafka/tags).

* Zookeeper,  [taken from Bitnami Docker hub repo](https://hub.docker.com/r/bitnami/zookeeper/tags).

* IPFS node, [taken from Docker hub repo](https://hub.docker.com/r/ipfs/go-ipfs).

* Grafana and Prometheus (https://github.com/prometheus-operator/kube-prometheus).

All of the applications have been containerized and [saved to my personal docker hub repo](https://hub.docker.com/repositories/shpookas).

![minikube-cluster](https://github.com/shpookas/weather_scraper/assets/84668053/af550eb4-6827-4ca6-b708-6cc1ccd0ff8d)



### Deployment process

First off, make sure that minikube cluster is running:
```
Minikube start
Minikube status
```
Clone this repository and start by depoying the application in the following manner (all of the deployments have been done to the default namespace in minikube cluster);

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

3. Deploy PostgreSQL application
  ```
  kubectl apply -f postgres-statefulset.yaml    
  ```
  This will deploy the PostgreQL kubernetes service, pvc and statefulset. In case the pod of postgres has to restart, the data will not be lost as it is stored in the pvc. 

4. Deploy Scraper (located under scraper folder)
  ```
  kubectl apply -f scraper.yml  
  ```
  The scraper python application is scraping weather information from 5 different cities using wittr (https://github.com/chubin/wttr.in), it is scheduled to scrape this information every 10 minutes and send this information in json format to 
  kafka server with the topic of temperature, this enables real-time monitoring of the temperature for these 5 different cities. 
 
  After the execution of the command the application will be deployed as kubernetes deployment. 

5. Deploy Kafka Consumer (located under consumer folder)
  ```
  kubectl apply -f consumer.yml  
  ```
  In summary, this script continuously consumes messages from the 'temperature' Kafka topic, parses the JSON data from these messages, and stores them into a PostgreSQL database, enabling the persistence of temperature data for various cities     
  over time.
  After the execution of the command the application will be deployed as kubernetes deployment. 
  Now you can test if the data that is being scraped is being stored in the PostgreSQL database by executing inside the postgres container and checking if the temperature_data table is being created and updated with new information
  Inside the postgres container issue the following commands;
  ```
  psql -U temperature_user -d temperature_database
  \dt
  SELECT * FROM temperature_data;
  ```
  You should get the following results;
  ![image](https://github.com/shpookas/weather_scraper/assets/84668053/0de26736-d0dc-48b5-b3d4-0e12b93464e6)

  However, the scraper runs only every 10 minutes, so you will have to wait 10 minute to see any results in the table. 


6. Deploy IPFS server (located under ipfs folder)
  ```
  kubectl apply -f ipfs.yml  
  ```
  This will deploy IPFS Service and Statefulset and initialize the ipfs daemon to run. In case the pod of ipfs has to restart, the data will not be lost as it is stored in the pvc.

7. Deploy the IPFS client (located under ipfs folder) and IPFS-client service
  ```
  kubectl apply -f scraper-deployment-2.yml
  kubectl apply -f ipfs-client-service.yml
  ```
  The client is deployed as a kubernetes deployment. If the user wants to trigger the script, the user has to issue the following command to get the IP address of ipfs-client-service

  ```
  minikube service ipfs-client-service --url
  ```
  You will then be able to curl to the application which will trigger the script to run and add data to IPFS CID. See the image bellow;
  ![ipfs-client-service](https://github.com/shpookas/weather_scraper/assets/84668053/38774c0f-750e-4e5f-a927-6c13a854d4ad)

  * The IPFS client bash script has a hardcoded IP address value of IPFS server (it cannot resolve to the internal kubernetes service name for some reason), thus if the IPFS has been redeployed with new service IP address, this has to be changed     manually inside of /usr/local/bin/scraper-bash-ipfs-2.sh under "REMOTE_IPFS_ADDRESS" to the IP adress of IPFS server service, see the screenshot below;
  ![image](https://github.com/shpookas/weather_scraper/assets/84668053/555374ab-8ee1-414e-acee-926398e449f8)

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
 Then one will have to add the Postgres, Kafka and Prometheus data sources to be able to scrape metrics of these services. 
 
 I've created a number of dashboards to track the health of the Minikube node and another dashboard to track if the data inside of PostgreSQL is coming in regularly as expected (every 10 minutes).
 The data of grafana is stored on a PVC so even if the pod will restart, the data will not be lost. 

 Minikube node health:
![Minikube-health](https://github.com/shpookas/weather_scraper/assets/84668053/8938f0cc-d4f9-4027-9ad9-913e32bb84f0)

Postgres db receiving new updates every 10minutes:
![postgres-health](https://github.com/shpookas/weather_scraper/assets/84668053/577e560b-5bc4-4d25-a38a-27a8eb1968db)



### Updates and rollbacks
All of the applications in this repo have been dockerized, so if one would like to implement new features, one would do good to test the new application code locally, and once satisfied, build new docker images, tag them with a version and push these images to dockerhub. Use the newly created docker image tag in the deployment specification of the kubernetes .yaml files. 
If for some reason a new feature proves to be faulty, then rollback to a previous version using a previous version docker tag in the kubernetes .yaml files. 


### Scaling the Weather scraper stack
* This project has been deployed to Minikube kubernetes cluster with only one node running all of the microservices. 
For more robust solution one would do good to increase the number of nodes in the minikube cluster or migrate to a cloud provider that offers Kubernetes services, such as Google Kubernetes Engine (GKE) on Google Cloud Platform, Amazon Elastic Kubernetes Service (EKS) on AWS, and Azure Kubernetes Service (AKS) on Microsoft Azure.
* If choosing to continue the work on Minikube one might consider to use Kubernetes Horizontal Pod Autoscaler (HPA) to automatically scale the number of pods based on CPU or custom metrics.
* If the application starts requiring more resources than a single pod can provide, you might need to vertically scale your pods by adjusting the CPU and memory limits in your pod's YAML definition and increasing the number of replicas each deployment and stateful set has. 
* Make use of Prometheus and Grafana to see if the stack requires more CPU, memory or Nodes.

### Troubleshooting
* Sometimes Kafka server might end up in CrashLoopBackOff Error due to cache memory problems or clusterID missmatch see (https://stackoverflow.com/questions/59592518/kafka-broker-doesnt-find-cluster-id-and-creates-new-one-after-docker-restart/59832914#59832914). If this happens then both Consumer and Scraper applications will stop working too. Thus to fix this delete the deployment and the pvc of kafka server and delete the deployment of zookeeper, after this is done redeploy first zookeeper, once its up and running redeploy kafka server. Check the kafka logs if everything is up and running as expected. 

* The IPFS client bash script has a hardcoded IP address value of IPFS server (it cannot resolve to the internal kubernetes service name for some reason), thus if the IPFS has been redeployed with new service IP address, this has to be changed manually inside of /usr/local/bin/scraper-bash-ipfs.sh under "REMOTE_IPFS_ADDRESS" to the IP adress of IPFS server service, see the screenshot below;
![image](https://github.com/shpookas/weather_scraper/assets/84668053/555374ab-8ee1-414e-acee-926398e449f8)


