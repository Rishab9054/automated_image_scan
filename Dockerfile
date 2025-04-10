# Start with a minimal, security-focused base image
FROM alpine:latest AS builder

# Update and install necessary packages in a single layer
RUN apk update && \
    apk upgrade && \
    apk add --no-cache ca-certificates tzdata && \
    rm -rf /var/cache/apk/*

# Create a non-root user to run the application
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Use multi-stage build to reduce attack surface
FROM scratch

# Copy only necessary files from builder
COPY --from=builder /etc/passwd /etc/group /etc/
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo

# Set working directory
WORKDIR /app

# Switch to non-root user
USER appuser

# Define healthcheck if applicable
# HEALTHCHECK --interval=30s --timeout=3s CMD ["/healthcheck"]

# Command to run when container starts
CMD ["sleep", "infinity"]

# Set specific labels for documentation
LABEL maintainer="your-name"
LABEL version="1.0"
LABEL description="Secure minimal Docker image"