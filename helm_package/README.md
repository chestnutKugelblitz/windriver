# Windriver test chart

This chart has been tested in the microk8s and Google Kubernetes Enginer with helm v3

To install the package, run:

```
helm3 install restapi  ../helm_package/
```
If you use minikube, you can get link to the application running this command with minikube:

```
minikube service restapisvc --url
```

Overwise, with other kubernetes engines, you can do something like this:

```shell script
kubectl port-forward service/restapi-svc-windriver 8080:8080
```
And than connect to http://localhost:8080/api/ and http://localhost:8080/api/ui via your browser or curl