FROM nginx:alpine

COPY . /usr/share/nginx/html/

# Thay đổi port từ 80 sang port khác
EXPOSE 8080

# Cấu hình nginx listen port 8080
RUN echo 'server { \
    listen 8080; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
