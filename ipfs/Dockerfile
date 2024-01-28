FROM ubuntu:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y curl

# Download and install IPFS binary
RUN curl -L https://dist.ipfs.io/go-ipfs/v0.26.0/go-ipfs_v0.26.0_linux-amd64.tar.gz | tar xz && \
    mv go-ipfs/ipfs /usr/local/bin/ipfs

# Clean up
RUN rm -rf go-ipfs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/local/bin/

# Copy the bash script into the image
COPY scraper-bash-ipfs.sh /usr/local/bin/

# Set up entrypoint
ENTRYPOINT ["sh", "-c", "ipfs init && tail -f /dev/null"]
