# get base image
FROM python:3.14

# set environment variables
ENV user=ubuntu
ENV DEBIAN_FRONTEND=noninteractive
# set python version
ARG PYTHON_VERSION="3.14"
ENV PYTHON_VERSION=${PYTHON_VERSION}

# install required software and programmes for development environment
RUN apt-get update
RUN apt-get install -y apt-utils vim curl wget unzip tree htop adduser

# set up home environment
RUN adduser ${user}
RUN mkdir -p /home/${user} && chown -R ${user}: /home/${user}

# clone git repo
COPY . /home/${user}/AgenticNewsLetter
# set working directory
WORKDIR /home/${user}/AgenticNewsLetter

# install required python packages
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv sync
RUN uv cache clear

# set cmd
ENV PATH="/app/.venv/bin:$PATH"
#CMD ["uv", "run", "newsletter/main.py"]
RUN chmod 755 /home/ubuntu/AgenticNewsLetter/entry.sh
ENTRYPOINT [ "sh","/home/ubuntu/AgenticNewsLetter/entry.sh" ]
CMD [ "newsletter.LambdaHandler.lambda_handler" ]