import etcd
import sys
import json
import time
import urllib

from subprocess import call
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('haproxy', 'templates'))
POLL_TIMEOUT=5


def get_etcd_addr():
    etcd_host = urllib.urlopen("http://169.254.169.254/latest/meta-data/local-ipv4").read()
    etcd_port = 4001
    return etcd_host, etcd_port


def get_services():
    etcd_host, etcd_port = get_etcd_addr()
    client = etcd.Client(host=etcd_host, port=int(etcd_port))
    backends = client.read('/services', recursive = True)
    services = {}

    for i in backends.children:
        print i.key
        if i.key.count("/") != 3:
            continue

        ignore, ignore2, service, container = i.key.split("/")
        value = json.loads(i.value)
        
        ep = services.setdefault(service, dict(port="", backends=[]))
        ep["bindport"] = value["port"]
        ep["backends"].append(dict(name=container.replace("@",""), host=value["host"], port=value["port"]))

    return services

def generate_config(services):
    template = env.get_template('haproxy.cfg.tmpl')
    with open("/etc/haproxy.cfg", "w") as f:
        f.write(template.render(services=services))

if __name__ == "__main__":
    current_services = {}
    while True:
        try:
            services = get_services()

            if not services or services == current_services:
                time.sleep(POLL_TIMEOUT)
                continue

            print "config changed. reload haproxy"
            generate_config(services)

            ret = call(["./reload-haproxy.sh"])
            if ret != 0:
                print "reloading haproxy returned: ", ret
                time.sleep(POLL_TIMEOUT)
                continue
 
            current_services = services

        except Exception, e:
            print "Error:", e

        time.sleep(POLL_TIMEOUT)
       
