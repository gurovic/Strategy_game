import docker
import os
import tarfile
client = docker.from_env()
def copy_to(src, dst):
    name, dst = dst.split(':')
    container = client.containers.get(name)

    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src)
    tar = tarfile.open(src + '.tar', mode='w')
    try:
        tar.add(srcname)
    finally:
        tar.close()

    data = open(src + '.tar', 'rb').read()
    container.put_archive(os.path.dirname(dst), data)
#client.containers.run('alpine', 'cat <clientprog.py>', 'C:/Users/Маша/PycharmProjects/pythonProject29/')
copy_to('C:/Users/Маша/PycharmProjects/pythonProject29', 'quizzical_nightingale:tmp/clientprog.py')
