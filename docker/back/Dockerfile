FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc sudo \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

ARG USERNAME=vscode
ARG USER_UID
ARG USER_GID

RUN groupadd -f -g $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
