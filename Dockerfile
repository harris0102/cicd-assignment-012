# Production image for the static site
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
