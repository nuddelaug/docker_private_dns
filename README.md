# DNS resolution for Private development similar to nio.ip

ever had issues to test various containers/services with the same IP ? There's a public Service call nio.ip which provides DNS resolution like:

```
mycontainer.192.168.0.1.nio.ip  -> 192.168.0.1 
anothercontainer.192.168.0.1.nio.ip -> 192.168.0.1
```

This provides the possibility to easily test multiple containers or versions without to much effort on Load Balancer configurations on your development Docker Host. 

## reason

the reason I've created this image is, that providing a simple to use DNS which can be limited to a specific IP Range for deployment/Enterprise integration into a large Network or private usage. 
Even though there is a service public available (nio.ip) it's limited to the name and without guarantee to be there when you need it.

## based on

the image is based on Centos:latest (time of release, Centos7) and Bind DNS 9.9.4-RedHat-9.9.4-72.el7

## container usage

Requirements:

- IP range you want to provide the service for (192.168.0.0/24, 172.27.0.0/16) 
- Domain you want to _append_ (my.ip, container.dev)
- if you want to use it as resolver for your system(s)

Defaults:

- IP range: 192.168.0.0/24
- Domain:   my.ip
- Resolving: no

without specifying the Environment variables, these values will be applied.
The image is not supposed to be _managed_ (no rndc or similar) as clearing the cache can be done by restaring the container.
The image is not supposed to host more Zone's (different names) or any other Zone.

spawning the image gattered the requirements as follows:

```
docker run --name mydns -d -e DNS_DOMAIN=my.ip -e DNS_SUBNET=172.17.0.0/16 -e DNS_RECURSION=yes docker.io/michaellang/docker_private_dnsc 
```

### verify deployment

get the IP address of the deployment
```
docker logs mydns | grep eth0
25-Dec-2018 19:50:14.061 listening on IPv4 interface eth0, 172.17.0.4#53

docker inspect mydns | grep IPAddress
            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.4",
                    "IPAddress": "172.17.0.4",
```

verify querying for your IP's works
```
dig +short @172.17.0.4 mytest.172.17.0.4.my.ip
172.17.0.4
```

in our example, you should also be able to resolv foreign hosts
```
dig +short @172.17.0.4 www.google.com.
172.217.17.228
```

with that when you expose the port 53 on your Docker host you, could use the DNS for resolving public/external stuff and your development.
