# cdk8s+ (cdk8s-plus)

**cdk8s+** is a software development framework that provides high level abstractions for authoring Kubernetes applications.
Built on top of the auto generated building blocks provided by [cdk8s](../cdk8s), this library includes a hand crafted *construct*
for each native kubernetes object, exposing richer API's with reduced complexity.

> **You should not use this library in production environments.**<br><br>
> ![Experimental](https://img.shields.io/badge/experimental-important.svg?style=for-the-badge)<br><br>
> This library is in very early stages of development, as such, and in correspondence with a `0.x` semantic major version line, its `API` is
> likely to rapidly change in breaking ways. We therefore highly discourage from using this library in production workloads.

## Letter Of Intent

We strive to develop this library with full transparency and as much community feedback and contributions as possible.
To that end, we publish this development version. The lack of features/capabilities is intentional, we look forward to build and expand this framework with the help of the community.

> If you are interested in contributing, see [Contribution Guide](./CONTRIBUTING.md).

## At a glance

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus
import cdk8s as cdk8s
import path as path

# our cdk app
app = cdk8s.App()

# our kuberentes chart
chart = cdk8s.Chart(app, "Chart")

# lets create a volume that contains our app.
# we use a trick with a config map!
app_data = kplus.ConfigMap(chart, "AppData")
app_data.add_directory(path.join(__dirname, "app"))

app_volume = kplus.Volume.from_config_map(app_data)

# now we create a container that runs our app
app_path = "/var/lib/app"
port = 80
container = kplus.Container(
    image="node:14.4.0-alpine3.12",
    command=["node", "index.js", f"{port}"],
    port=port,
    working_dir=app_path
)

# make the app accessible to the container
container.mount(app_path, app_volume)

# now lets create a deployment to run a few instances of this container
deployment = kplus.Deployment(chart, "Deployment",
    spec=DeploymentSpec(
        replicas=3,
        pod_spec_template=PodSpec(
            containers=[container]
        )
    )
)

# finally, we expose the deployment as a load balancer service and make it run
deployment.expose(port=8080, service_type=kplus.ServiceType.LOAD_BALANCER)

# we are done, synth
app.synth()
```

```yaml
apiVersion: v1
data:
  index.js: |-
    var http = require('http');

    var port = process.argv[2];

    //create a server object:
    http.createServer(function (req, res) {
      res.write('Hello World!'); //write a response to the client
      res.end(); //end the response
    }).listen(port); //the server object listens on port 80
kind: ConfigMap
metadata:
  annotations: {}
  labels: {}
  name: chart-appdata-configmap-da4c63ab
---
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations: {}
  labels: {}
  name: chart-deployment-pod-d4285cc9
spec:
  replicas: 3
  selector:
    matchLabels:
      cdk8s.deployment: ChartDeploymentCFC2E30C
  template:
    metadata:
      annotations: {}
      labels:
        cdk8s.deployment: ChartDeploymentCFC2E30C
    spec:
      containers:
        - command:
            - node
            - index.js
            - "80"
          env: []
          image: node:14.4.0-alpine3.12
          name: main
          ports:
            - containerPort: 80
          volumeMounts:
            - mountPath: /var/lib/app
              name: configmap-chart-appdata-configmap-da4c63ab
          workingDir: /var/lib/app
      volumes:
        - configMap:
            name: chart-appdata-configmap-da4c63ab
          name: configmap-chart-appdata-configmap-da4c63ab
---
apiVersion: v1
kind: Service
metadata:
  annotations: {}
  labels: {}
  name: chart-deployment-service-pod-42f50c26
spec:
  externalIPs: []
  ports:
    - port: 8080
      targetPort: 80
  selector:
    cdk8s.deployment: ChartDeploymentCFC2E30C
  type: LoadBalancer
```

## Installation and Usage

We currently support both Python and TypeScript/JavaScript. More languages are coming soon.

> We would love to hear which languages you want to see next: [Languages Support](https://github.com/awslabs/cdk8s/issues/134)

### TypeScript/JavaScript

`❯ npm install cdk8s-plus cdk8s`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus
import cdk8s as cdk8s

app = cdk8s.App()
chart = cdk8s.Chart(app, "Chart")

kplus.Deployment(chart, "Deployment",
    spec=DeploymentSpec(
        replicas=3,
        pod_spec_template=PodSpec(
            containers=[kplus.Container(
                image="ubuntu"
            )]
        )
    )
)
```

### Python

`❯ pip install cdk8s-plus cdk8s`

```python
import cdk8s_plus as kplus
import cdk8s

app = cdk8s.App()
chart = cdk8s.Chart(app, 'Chart')

kplus.Deployment(chart, 'Deployment',
  spec=kplus.DeploymentSpec(
    replicas=1,
    pod_spec_template=kplus.PodSpec(containers=[kplus.Container(image='ubuntu')])
  )
)
```

## In Depth

Following are excerpts for the usage of every *construct* provided by this library. It details the commonly used patterns and configuration properties.
In general, every such construct can be configured using two mechanisms:

* Spec Constructor Properties
* Post Instantiation Spec Mutations

The documentation presented here focuses on post instantiation mutations, however, every such mutation can also be pre-configured
using constructor properties for the corresponding spec. A complete API reference can be found in [here](./API.md).

### `Container`

Define containers that run in a pod using the `Container` class.

> API Reference: [Container](./API.md#cdk8s-plus-container)

#### Environment variables

Environment variables can be added to containers using various sources, via semantically explicit API's:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus

container = kplus.Container(
    image="my-app"
)

# explicitly use a value.
container.add_env("endpoint", kplus.EnvValue.from_value("value"))

# use a specific key from a config map.
backends_config = kplus.ConfigMap.from_config_map_name("backends")
container.add_env("endpoint", kplus.EnvValue.from_config_map(backends_config, "endpoint"))

# use a specific key from a secret.
credentials = kplus.Secret.from_secret_name("credentials")
container.add_env("password", kplus.EnvValue.from_secret(credentials, "password"))
```

#### Volume Mounts

A very common capability is to mount a volume with some data onto a container. Using pure kubernetes API, this would require writing something like:

```yaml
kind: Pod
apiVersion: v1
spec:
  containers:
    - name: main
      volumeMounts:
        - mountPath: /path/to/mount
          name: 'config-volume'
  volumes:
    - name: 'config-volume'
      configMap:
        name: 'config'
```

Notice the apparent redundancy of having to specify the volume name twice. Also, if you happen to need the same mount in other pods,
you would need to duplicate this configuration. This can get complex and cluttered very fast.

In contrast, here is how to do this with `cdk8s+`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus

config = kplus.ConfigMap.from_config_map_name("config")
volume = kplus.Volume.from_config_map(config)

container = kplus.Container(
    image="my-app"
)

# Cool alert: every pod that will later be configured with this container,
# will automatically have access to this volume, so you don't need to explicitly add it to the pod spec!.
container.mount("/path/to/mount", volume)
```

### `Volume`

Volume represents a named volume in a pod that may be accessed by any container in the pod.

> API Reference: [Volume](./API.md#cdk8s-plus-volume)

#### Create from a ConfigMap

A very useful operation is to create a volume from a `ConfigMap`. Kubernetes will translate every key in the config map to a file,
who's content is the value of the key.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus

config_map = kplus.ConfigMap.from_config_map_name("redis-config")
config_volume = kplus.Volume.from_config_map(config_map)
```

#### Create from an EmptyDir

The easiest way to allocate some persistent storage to your container is to create a volume from an empty directory.
This volume, as the name suggests, is initially empty, and can be written to by containers who mount it.
The data in the volume is preserved throughout the lifecycle of the pod, but is deleted forever as soon as the pod itself is removed.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus

data = kplus.Volume.from_empty_dir(config_map)

redis = kplus.Container(
    image="redis"
)

# mount to the redis container.
redis.mount("/var/lib/redis", data)
```

### `Job`

Jobs are a very useful concept in kubernetes deployments.
They can be used for add-hoc provisioning tasks, as well as long running processing jobs.

> API Reference: [Job](./API.md#cdk8s-plus-job)

In configuration, they don't differ much from regular pods, but offer some additional properties.

#### Delete a Job after its finished

You can configure a TTL for the job after it finished its execution successfully.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s as k
import cdk8s_plus as kplus

# let's define a job spec, and set a 1 second TTL.
job_spec = {
    "ttl_after_finished": kplus.Duration.seconds(1)
}

# now add a container to all the pods created by this job
job_spec.pod_spec_template.add_container(kplus.Container(
    image="loader"
))

app = k.App()
chart = k.Chart(app, "Chart")

# now we create the job
load = kplus.Job(chart, "LoadData", spec=job_spec)
```

### `Service`

Use services when you want to expose a set of pods using a stable network identity. They can also be used for externalizing
endpoints to clients outside of the kubernetes cluster.

> API Reference: [Service](./API.md#cdk8s-plus-service)

#### Selectors

Services must be configured with selectors that tell it which pods should it serve.
The most common selector method is using labels.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s as k
import cdk8s_plus as kplus

app = k.App()
chart = k.Chart(app, "Chart")
frontends = kplus.Service(chart, "FrontEnds")

# this will cause the service to select all pods with the 'run: frontend' label.
frontends.spec.select_by_label("run", "frontend")
```

#### Ports

Ports that the service will listen and redirect to can be configured like so:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s as k
import cdk8s_plus as kplus

app = k.App()
chart = k.Chart(app, "Chart")
frontends = kplus.Service(chart, "FrontEnds")

# make the service bind to port 9000 and redirect to port 80 on the associated containers.
frontends.spec.serve(port=9000, target_port=80)
```

### `Deployment`

Create a deployment to govern the lifecycle and orchestration of a set of identical pods.

> API Reference: [Deployment](./API.md#cdk8s-plus-deployment)

#### Automatic pod selection

When you specify pods in a deployment, you normally have to configure the appropriate labels and selectors to
make the deployment control the relevant pods. This construct does this automatically.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s as k
import cdk8s_plus as kplus

app = k.App()
chart = k.Chart(app, "Chart")

kplus.Deployment(chart, "FrontEnds",
    spec=DeploymentSpec(
        pod_spec_template=PodSpec(
            containers=[kplus.Container(image="node")]
        )
    )
)
```

Note the resulting manifest contains a special `cdk8s.deployment` label that is applied to the pods, and is used as
the selector for the deployment.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations: {}
  labels: {}
  name: chart-frontends-pod-a48e7f2e
spec:
  replicas: 1
  selector:
    matchLabels:
      cdk8s.deployment: ChartFrontEndsDD8A97CE
  template:
    metadata:
      annotations: {}
      labels:
        cdk8s.deployment: ChartFrontEndsDD8A97CE
```

#### Exposing via a service

Following up on pod selection, you can also easily create a service that will select the pods relevant to the deployment.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# store the deployment to created in a constant
frontends = kplus.Deployment(chart, "FrontEnds")

# create a ClusterIP service that listens on port 9000 and redirects to port 9000 on the containers.
frontends.expose(port=9000)
```

Notice the resulting manifest, will have the same `cdk8s.deployment` magic label as the selector.
This will cause the service to attach to the pods that were configured as part of the said deployment.

```yaml
apiVersion: v1
kind: Service
metadata:
  annotations: {}
  labels: {}
  name: chart-frontends-service-pod-1f70150b
spec:
  externalIPs: []
  ports:
    - port: 9000
  selector:
    cdk8s.deployment: ChartFrontEndsDD8A97CE
  type: ClusterIP
```

### `ConfigMap`

ConfigMap are used to store configuration data. They provide a dictionary based data structure that can be consumed in
various shapes and forms.

> API Reference: [ConfigMap](./API.md#cdk8s-plus-configmap)

#### Use an existing `ConfigMap`

You can reference to an existing `ConfigMap` like so. Note that this does not create a new object,
and will therefore not be included in the resulting manifest.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus

config = kplus.ConfigMap.from_config_map_name("config")

# the 'config' constant can later be used by API's that require an IConfigMap.
# for example when creating a volume.
volume = kplus.Volume.from_config_map(config)
```

#### Adding data

You can create config maps and add some data to them like so:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus
import cdk8s as k

app = k.App()
chart = k.Chart(app, "Chart")

config = kplus.ConfigMap(chart, "Config")()
config.add_data("url", "https://my-endpoint:8080")
```

#### Creating a volume from a directory

Here is a nifty little trick you can use to create a volume that contains a directory on the client machine (machine that runs `cdk8s synth`):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus
import cdk8s as k
import path as path

app = k.App()
chart = k.Chart(app, "Chart")

app_map = kplus.ConfigMap(chart, "Config")()

# add the files in the directory to the config map.
# this will create a key for each file.
# note that only top level files will be included, sub-directories are not yet supported.
app_map.add_directory(path.join(__dirname, "app"))

app_volume = kplus.Volume.from_config_map(app_map)

# for here, just mount the volume to a container, and run your app!
mount_path = "/var/app"
container = kplus.Container(
    image="node",
    command=["node", "app.js"],
    working_dir=mount_path
)

container.mount(mount_path, app_volume)
```

### `Pod`

A pod is essentially a collection of containers. It is the most fundamental computation unit that can be provisioned.

> API Reference: [Pod](./API.md#cdk8s-plus-pod)

#### Adding Containers/Volumes

Containers and volumes can be added to pod definition like so:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus

container = kplus.Container(
    image="node"
)

storage = kplus.Volume.from_empty_dir("storage")

container.mount("/data", storage)

app = k.App()
chart = k.Chart(app, "Chart")

pod = kplus.Pod(chart, "Pod")()

# this will automatically add the volume as well.
pod.spec.add_container(container)

# but if you want to explicitly add it, simply use:
pod.spec.add_volume(storage)
```

#### Applying a restart policy

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus

app = k.App()
chart = k.Chart(app, "Chart")

pod = kplus.Pod(chart, "Pod")()
pod.spec.restart_policy = kplus.RestartPolicy.NEVER
```

#### Assigning a ServiceAccount

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus

app = k.App()
chart = k.Chart(app, "Chart")

pod = kplus.Pod(chart, "Pod")()
pod.spec.service_account = kplus.ServiceAccount.from_service_account_name("aws")
```

### `Secret`

Secrets are used to store confidential information. Never store such information on the definition of the pod itself.

> API Reference: [Secret](./API.md#cdk8s-plus-secret)

#### Use an existing `Secret`

To reference a secret created outside of your deployment definition, use the following. Note that this does not create a new object,
and will therefore not be included in the resulting manifest.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus

secret = kplus.Secret.from_secret_name("aws-creds")
```

#### Adding data

To create a new secret with some data, use:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus
import cdk8s as k

app = k.App()
chart = k.Chart(app, "Chart")

secret = kplus.Secret(chart, "Secret")
secret.add_string_data("password", "some-encrypted-data")
```

### `ServiceAccount`

Use service accounts to provide an identity for pods.

> API Reference: [ServiceAccount](./API.md#cdk8s-plus-serviceaccount)

#### Use an existing `ServiceAccount`

To reference a service account created outside of your deployment definition, use the following. Note that this does not create a new object,
and will therefore not be included in the resulting manifest.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus

service_account = kplus.ServiceAccount.from_service_account_name("aws-service")
```

#### Allowing access to secrets

To create a new service account, and give it access to some secrets, use the following:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk8s_plus as kplus
import cdk8s as k

app = k.App()
chart = k.Chart(app, "Chart")

aws_creds = kplus.Secret.from_secret_name("aws-creds")
aws_service = kplus.ServiceAccount(chart, "AWS")

# give access to the aws creds secret.
aws_service.add_secret(aws_creds)
```
