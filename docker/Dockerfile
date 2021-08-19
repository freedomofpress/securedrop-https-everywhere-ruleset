# sha256 as of 2021-08-18 for nginx:mainline-alpine
FROM nginx:mainline-alpine@sha256:bead42240255ae1485653a956ef41c9e458eb077fcb6dc664cbc3aa9701a05ce

COPY docker/nginx.conf /etc/nginx
RUN mkdir -p /opt/nginx && chown nginx:nginx /opt/nginx

USER nginx
RUN mkdir -p /opt/nginx/run /opt/nginx/root/https-everywhere

# Only the latest rulesets are required (and listed in index.html), but
# include all versions that exist in the repo in case a client requests
# an old one (maybe they failed to fetch the latest timestamp).

COPY index.html latest-rulesets-timestamp default.rulesets.*.gz rulesets-signature.*.sha256 /opt/nginx/root/https-everywhere/
