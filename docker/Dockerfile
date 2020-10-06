# sha256 as of 2020-09-25 for mainline-alpine
FROM nginx@sha256:4635b632d2aaf8c37c8a1cf76a1f96d11b899f74caa2c6946ea56d0a5af02c0c

COPY docker/nginx.conf /etc/nginx
RUN mkdir -p /opt/nginx && chown nginx:nginx /opt/nginx

USER nginx
RUN mkdir -p /opt/nginx/run /opt/nginx/root/https-everywhere

# Only the latest rulesets are required (and listed in index.html), but
# include all versions that exist in the repo in case a client requests
# an old one (maybe they failed to fetch the latest timestamp).

COPY index.html latest-rulesets-timestamp default.rulesets.*.gz rulesets-signature.*.sha256 /opt/nginx/root/https-everywhere/
