# Cloud Computing Final Project

It is the final project of AUT Cloud Computing course.

> Instructor: [Dr. S. A. Javadi](https://scholar.google.com/citations?user=Va7RTUsAAAAJ&hl=en)

> Semester: Fall 2021

## About

For this project, a simple URL shortener service has been developed using Flask and Redis and containerized using Docker. Full project instructions (in Persian) is available [here](./instruction.pdf).

The shortener, exposes two endpoints. One for shortening the given URL and one for redirecting shortened URLs to the original one. For example, if the container was running in localhost and you wanted to shorten this repository's address, you could use:
```bash
curl -r POST \
	--form "u=https://github.com/2000mahan/Cloud-Computing-Project" \
	127.0.0.1:8080/shortener
```
And the answer would be:
```
{"shortened":"baa3a"}
```
Now, if you go to [127.0.0.1:8080/baa3a](http://127.0.0.1:8080/baa3a), you will be redirected to this repository.

The short URLs also expire after certain amount of time. You can change this behavior by setting `URL_EX` environment variable.

## Deployment via Docker Compose

To deploy the project in detached mode via Docker Compose, run the following command:
```bash
docker-compose up -d
```

## Deployment in Kubernetes

For deployment in Kubernetes, you can either use a single pod for Redis database (using Deployment object) or replicated Redis databases (using StatefulSet object).

### Single Redis pod

For deploying using only one pod for Redis, simply use provided Helm chart.
```bash
helm install --generate-name helm
```

### Replicated Redis pods

For having replicated Redis pods, head into the `k8s` directory and apply the description files in the following order:
```bash
kubectl apply -f sts/cm.yaml
kubectl apply -f secret.yaml
kubectl apply -f sts/redis-sts.yaml
kubectl apply -f sts/redis-service.yaml
kubectl apply -f shortener-deployment.yaml
kubectl apply -f shortener-service.yaml
kubectl apply -f hpa.yaml
```