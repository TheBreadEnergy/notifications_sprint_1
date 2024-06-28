#!/bin/sh

#!/usr/bin/env sh

if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/healthcheck -H "X-Request-Id: $(uuidgen)" | grep -q 200; then
    exit 0;  # Successful HTTP response, pod is healthy
else
    exit 1;  # HTTP response not successful, pod is unhealthy
fi