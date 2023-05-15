## Install nginx

Nginx is a web server software that is used to serve web content, reverse proxy, and load balance HTTP and HTTPS traffic.
It is known for its high performance, scalability, and reliability. Nginx is free and open-source software, and it can
run on a variety of operating systems, including Linux, Windows, and macOS. It is widely used by websites and web
applications to handle high traffic and improve the performance and security of their systems. Nginx also supports
various plugins and modules, which allows developers to customize its functionality to fit their needs.


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

![](https://github.com/stupns/FastStupnsAPI2/blob/main/img/hostiq.png)
![](https://github.com/stupns/FastStupnsAPI2/blob/main/img/digitaloc.png)
![](https://github.com/stupns/FastStupnsAPI2/blob/main/img/domens.png)
___

[<-- prev step](DIGITAL_OCEANS_README.md)_______________________________________[next step -->](Firewall_README.md)