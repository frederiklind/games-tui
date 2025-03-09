FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt update && apt install -y \
    sudo \
    git \
    make \
    python3 \
    python3-pip \
    python3-venv \
    apt-utils \
    && rm -rf /var/lib/apt/lists/*

# Create directories for the runner user
RUN mkdir -p /home/runner /home/runner/.config /home/runner/.local /home/runner/.cache

# Add the runner user and set permissions
RUN useradd -m -s /bin/bash runner && \
    echo "runner:runner" | chpasswd && \
    adduser runner sudo

# Set ownership of /home/runner to 'runner' user to ensure proper permissions
RUN chown -R runner:runner /home/runner

# Switch to 'runner' user before cloning the repo
USER runner

# Set the working directory to the home directory of 'runner' user
WORKDIR /home/runner

# Clone the repo
RUN git clone https://github.com/frederiklind/games-tui.git

# Set up the virtual environment and install dependencies
RUN python3 -m venv /home/runner/.venv
RUN /home/runner/.venv/bin/pip install --upgrade pip
RUN /home/runner/.venv/bin/pip install -r /home/runner/games-tui/requirements.txt

# Set the entrypoint to bash so you can interact with the container
CMD ["/bin/bash"]


