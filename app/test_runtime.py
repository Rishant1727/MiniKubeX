from runtime.docker_runtime import DockerRuntime


runtime = DockerRuntime()

containers = runtime.list_containers()

for container in containers:
    print(
        f"{container.name} - {container.status}"
    )