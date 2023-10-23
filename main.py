import docker
client = docker.from_env()
client.containers.run('alpine', 'echo hello world')
