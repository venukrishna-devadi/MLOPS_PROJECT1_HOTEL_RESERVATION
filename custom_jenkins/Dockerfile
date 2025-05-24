# This file will help install Jenkins container setup
FROM jenkins/jenkins:lts

USER root

# Download and install Docker CLI manually
RUN curl -fsSL https://download.docker.com/linux/static/stable/x86_64/docker-24.0.5.tgz | tar xz && \
    mv docker/* /usr/bin/ && \
    chmod +x /usr/bin/docker && \
    rm -rf docker

# Add Jenkins user to docker group (so it can run docker commands)
RUN groupadd -f docker && usermod -aG docker jenkins

# Create a docker directory and docker volume for DinD
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

USER jenkins