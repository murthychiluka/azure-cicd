```
mkdir agent
cd agent
sudo yum install -y icu libicu
sudo dnf install docker -y
sudo yum install git -y
sudo systemctl start docker
sudo chmod 666 /var/run/docker.sock
curl -O https://download.agent.dev.azure.com/agent/4.272.0/vsts-agent-linux-x64-4.272.0.tar.gz

tar zxvf vsts-agent-linux-x64-4.272.0.tar.gz
```

./ config.sh

./ run.sh





