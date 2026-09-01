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

```text
Absolutely. This was a useful end-to-end CI/CD troubleshooting exercise. The most important learning points from what you just went through are these:

1. Separate CI/CD stages clearly

Your pipeline essentially has:

GitHub
   ↓
GitHub Actions
   ↓
Docker build
   ↓
Push image to ACR
   ↓
SSH to EC2
   ↓
Docker login to ACR
   ↓
Docker pull
   ↓
Stop old container
   ↓
Start new container

When troubleshooting, identify which stage failed instead of assuming the whole pipeline is broken.

2. Docker image vs container

This is an important distinction:

Docker Image
     ↓ docker run
Docker Container

For example:

docker pull murthy.azurecr.io/cloud-app:6

downloads the image.

Then:

docker run -d -p 80:80 --name cloud-app \
  murthy.azurecr.io/cloud-app:6

creates and starts the container.

Useful commands:

docker images       # images
docker ps           # running containers
docker ps -a        # all containers
3. ACR authentication and Docker daemon permissions are different

This was probably the most valuable troubleshooting lesson.

Your GitHub Actions server showed:

Login Succeeded

but:

permission denied while trying to connect to the Docker daemon socket

These are two different things.

docker login
     ↓
Authenticate to ACR

versus:

docker pull
     ↓
Communicate with Docker daemon
     ↓
/var/run/docker.sock

So:

Successful ACR login does not mean the user has permission to run Docker.

4. Linux user permissions matter in CI/CD

Manually, you were logged in as:

root

Therefore Docker worked.

GitHub Actions SSH was connecting as:

ec2-user

Therefore Docker initially failed.

The fix was:

usermod -aG docker ec2-user

This gives ec2-user permission to communicate with Docker without requiring sudo.

Very important operational concept:

ec2-user
   ↓
docker group
   ↓
/var/run/docker.sock
   ↓
Docker daemon
5. su and SSH authentication are different

You tried:

su - ec2-user

and Linux asked for a password.

That doesn't mean EC2 is broken.

Your EC2 access uses an SSH key, while su expects the user's local password.

Since you were already logged in as:

ec2-user

the correct approach was simply to exit and establish a new SSH session so the new Docker group membership would take effect.

6. set +e can hide deployment failures

You originally had:

set +e

This means:

Continue even if a command fails.

That's dangerous for deployments.

For example:

docker pull ❌
docker run   ❌
Deployment complete ✅

Instead, use:

set -e

Then:

docker pull ❌
     ↓
script stops ❌
     ↓
GitHub Actions fails ❌

This makes failures visible.

7. || true is useful for expected failures

You correctly have:

docker stop $APP_NAME || true
docker rm $APP_NAME || true

Why?

On the first deployment, the container might not exist:

Error: No such container: cloud-app

That's not necessarily a deployment failure.

So:

docker stop cloud-app || true

means:

Try to stop it, but if it doesn't exist, continue.

This is a good use of || true.

8. GitHub run_number gives you versioned images

You use:

TAG=${{ github.run_number }}

Suppose GitHub Actions run number is:

6

Then your image becomes:

murthy.azurecr.io/cloud-app:6

Build:

docker build -t murthy.azurecr.io/cloud-app:6 .

Push:

docker push murthy.azurecr.io/cloud-app:6

Deploy:

docker pull murthy.azurecr.io/cloud-app:6

This is better than relying only on:

cloud-app:latest

because you know exactly which build you're deploying.

9. --password-stdin is the preferred Docker login approach

You used:

echo "${{ secrets.ACR_PASSWORD }}" | \
docker login "$REGISTRY" \
-u "${{ secrets.ACR_USERNAME }}" \
--password-stdin

The important part:

--password-stdin

means Docker reads the password from standard input instead of putting the password directly in the command arguments.

Avoid:

docker login ... -p "$PASSWORD"

Use:

--password-stdin

instead.

10. Container port mapping is critical

You used:

docker run -d -p 80:80 ...

Remember:

-p HOST_PORT:CONTAINER_PORT

Therefore:

-p 80:80

EC2 port 80
     ↓
Container port 80

If your application listens on port 5000, you'd need:

-p 80:5000
11. Test from inside → outside

This was another very good troubleshooting approach.

You tested:

curl http://localhost:80

and received:

HTTP/1.1 200 OK

That proved:

Docker ✅
Container ✅
Application ✅
Port mapping ✅

If the application then cannot be accessed externally, investigate:

Security Group
Network ACL
Firewall
Public IP
Load Balancer

rather than changing the application.

12. Don't confuse private IP with public access

Your EC2 hostname showed:

ip-10-0-2-201

which corresponds to:

10.0.2.201

That's a private IP.

For Internet access, you need the appropriate public IP/DNS or a load balancer.

The troubleshooting methodology to remember

When a deployment fails, use this sequence:

1. Is GitHub Actions running?
          ↓
2. Can SSH reach the target?
          ↓
3. Is the correct Linux user being used?
          ↓
4. Does that user have Docker permission?
          ↓
5. Can Docker login to ACR?
          ↓
6. Can Docker pull the expected tag?
          ↓
7. Is the container running?
          ↓
8. Is the application listening on the expected port?
          ↓
9. Does curl localhost work?
          ↓
10. If localhost works, check external networking/SG
Your final architecture
                 GitHub
                   │
                   ▼
            GitHub Actions
                   │
             docker build
                   │
                   ▼
           Azure Container
             Registry
          murthy.azurecr.io
                   │
              docker push
                   │
                   ▼
              SSH to EC2
                   │
               ec2-user
                   │
              docker group
                   │
                   ▼
             Docker daemon
                   │
             docker pull
                   │
                   ▼
          cloud-app:6
                   │
              docker run
                   │
                   ▼
             Port 80
                   │
                   ▼
             Application

The biggest takeaway: when CI/CD says "successful" or "failed," don't just look at the final status. Read the logs and identify the exact boundary where the failure occurs — SSH, authentication, permissions, registry, Docker, application, or network. That skill is extremely important for real-world DevOps troubleshooting.
```




