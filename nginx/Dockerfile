FROM nginx:alpine

# Build argument to choose config file
ARG CONFIG_FILE=nginx.conf

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY ${CONFIG_FILE} /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
