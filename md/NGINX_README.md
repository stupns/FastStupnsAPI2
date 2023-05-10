## Install nginx

```commandline
sudo apt install nginx -y
systemctl start nginx

cd /etc/nginx/sites-available/
cat default

sudo vi cat default
```

Paste next :

```text
        location / {
                proxy_pass http://localhost:8000;
                proxy_http_version 1.1;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $http_host;
                proxy_set_header X-NginX-Proxy true;
                proxy_redirect off;
        }
```
```commandline
systemctl restart nginx
```

## Register domain

![](..\img\hostiq.png)
![](..\img\digitaloc.png)
