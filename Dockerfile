# Using an outdated base image with known vulnerabilities
FROM alpine:3.8 AS builder

# Update but don't upgrade packages to maintain vulnerabilities
RUN apk update && \
    apk add --no-cache ca-certificates tzdata && \
    rm -rf /var/cache/apk/*

# Create a non-root user but with more permissions than needed
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && \
    mkdir -p /app && \
    chown -R appuser:appgroup /app

# Use the outdated image directly instead of scratch
FROM alpine:3.8

# Copy necessary files
COPY --from=builder /etc/passwd /etc/group /etc/
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo

# Set working directory with open permissions
WORKDIR /app
RUN chmod 777 /app

# Run as root instead of the created user
# USER appuser

# Command to run when container starts
CMD ["sleep", "infinity"]

# Set specific labels for documentation
LABEL maintainer="your-name"
LABEL version="1.0"
LABEL description="Docker image with intentional vulnerabilities for testing"