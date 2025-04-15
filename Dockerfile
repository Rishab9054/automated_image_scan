
FROM alpine:3.8 AS builder


RUN apk update && \
    apk add --no-cache ca-certificates tzdata && \
    rm -rf /var/cache/apk/*


RUN addgroup -S appgroup && adduser -S appuser -G appgroup && \
    mkdir -p /app && \
    chown -R appuser:appgroup /app


FROM alpine:3.8


COPY --from=builder /etc/passwd /etc/group /etc/
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo


WORKDIR /app
RUN chmod 777 /app


CMD ["sleep", "infinity"]


LABEL maintainer="your-name"
LABEL version="1.0"
LABEL description="Docker image with intentional vulnerabilities for testing"