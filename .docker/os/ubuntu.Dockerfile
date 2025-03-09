FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    sudo \
    git \
    make \
    python3 \
    python3-pip \
    python3-venv \
    apt-utils \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/runner /home/runner/.config /home/runner/.local /home/runner/.cache

RUN useradd -m -s /bin/bash runner && \
    echo "runner:runner" | chpasswd && \
    adduser runner sudo

RUN chown -R runner:runner /home/runner

USER runner

WORKDIR /home/runner

RUN git clone https://github.com/frederiklind/games-tui.git

RUN python3 -m venv /home/runner/.venv
RUN /home/runner/.venv/bin/pip install --upgrade pip
RUN /home/runner/.venv/bin/pip install -r /home/runner/games-tui/requirements.txt

CMD ["/bin/bash"]


