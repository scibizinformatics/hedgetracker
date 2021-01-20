from fabric.contrib.project import rsync_project
from fabric.api import env, run, local

# 34.208.166.207
env.hosts = ['ec2-34-208-166-207.us-west-2.compute.amazonaws.com']
env.user = 'ubuntu'
env.forward_agent = True
env.key_filename = '/home/jethro/Documents/dev/scibiz-aws-keypair1.pem'

def uname():
    run('uname -a')

def sync():
    exc = [
            'venv', '*.pyc', '.DS_Store', '*.pid',
            '*~', '.git', '.gitignore', '*.log',
            '*.rdb', '*sqlite*', '__pycache__', 'static',
            'node_modules', '.env'
        ]
    rsync_project(
        '/home/ubuntu',
        delete=False,
        exclude=exc, 
        ssh_opts='-o stricthostkeychecking=no'
    )
