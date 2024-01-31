FROM ubuntu:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y curl netcat

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
COPY scraper-bash-ipfs-2.sh /usr/local/bin/scraper-bash-ipfs-2.sh

# Make the script executable
RUN chmod +x /usr/local/bin/scraper-bash-ipfs-2.sh

# Expose the port where the server will listen
EXPOSE 8080

# Run the script as the entrypoint
ENTRYPOINT ["/usr/local/bin/scraper-bash-ipfs-2.sh"]
