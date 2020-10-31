# Windriver test chart

This chart has been tested in minikube and helm v2

To install the package, run:

```
helm install restapi  ../helm_package/
```

To get link to application run this command with minikube:

```
minikube service restapisvc --url
```
