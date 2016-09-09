"""
@Created on: 09/09/16,
@author: Prathyush SP,
@version: 0.0.1

"""
import curses
import time
import subprocess
from threading import Thread

stdscr = curses.initscr()


class Process(object):
    def __init__(self, process_name, docker_image, service_name, docker_status='Downloading . . .', service_status='Not Started . . .'):
        self.process_name = process_name
        self.docker_image = docker_image
        self.service_name = service_name
        self.docker_status = docker_status
        self.service_status = service_status


_counter = set([])
_process_dict = {
    'pause': Process(process_name='Pause', docker_image='gcr.io/google_containers/pause-amd64', service_name=''),
    'addon': Process(process_name='Addon Manager', docker_image='gcr.io/google_containers/addon-resizer',
                     service_name=''),
    'dnsmasq': Process(process_name='DNSMASQ Manager', docker_image='gcr.io/google_containers/kube-dnsmasq-amd64',
                       service_name=''),
    'heapster': Process(process_name='Heapster', docker_image='gcr.io/google_containers/heapster', service_name=''),
    'dns': Process(process_name='DNS Manager', docker_image='gcr.io/google_containers/kubedns-amd64', service_name=''),
    'dashboard': Process(process_name='Dashboard Manager',
                         docker_image='gcr.io/google_containers/kubernetes-dashboard-amd64',
                         service_name=''),
    'exec': Process(process_name='Exec Health Manager', docker_image='gcr.io/google_containers/exechealthz-amd64',
                    service_name=''),
    'hyperkube': Process(process_name='Hyperkube', docker_image='quay.io/coreos/hyperkube', service_name=''),
    'test': Process(process_name='Hyperkube', docker_image='abcd', service_name='')
}


class Query(Thread):
    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)

    def query_docker_status(self, docker_name):
        return subprocess.check_output('vagrant ssh -c "docker images -q ' + docker_name + '" 2> /dev/null', shell=True)

    def run(self):
        global _process_dict
        global _counter
        while len(_counter) <= 7:
            for k, v in _process_dict.items():
                if self.query_docker_status(v.docker_image) != b'':
                    _counter.add(k)
                    _process_dict[k] = Process(process_name=v.process_name, docker_image=v.docker_image,
                                               service_name=v.service_name, docker_status='Completed\t', service_status='Started\t')
            time.sleep(10)


def blink(char, period_in_sec):
    print(char, end='\r')
    time.sleep(period_in_sec)
    print(' ' * 50, end='\r')
    time.sleep(period_in_sec)


def display_manager():
    display_str = \
        " ---------------------------------------------------------------------------------------\n" \
        "| Process\t\t\t|| Docker Image\t\t\t||  Services\t\t|\n" \
        " ---------------------------------------------------------------------------------------\n" \
        "| 1. " + _process_dict['pause'].process_name + "\t\t\t|| " + _process_dict[
            'pause'].docker_status + "\t\t|| " + _process_dict['pause'].service_status + "\t|\n" \
                                                                                         "| 2. " + _process_dict[
            'addon'].process_name + "\t\t|| " + _process_dict['addon'].docker_status + "\t\t|| " \
        + _process_dict['addon'].service_status + "\t|\n" \
                                                  "| 3. " + _process_dict['dnsmasq'].process_name + "\t\t|| " \
        + _process_dict['dnsmasq'].docker_status + "\t\t|| " + _process_dict['dnsmasq'].service_status + "\t|\n" \
                                                                                                         "| 4. " + \
        _process_dict['heapster'].process_name + "\t\t\t|| " + _process_dict['heapster'].docker_status \
        + "\t\t|| " + _process_dict['heapster'].service_status + "\t|\n" \
                                                                 "| 5. " + _process_dict[
            'dns'].process_name + "\t\t|| " + _process_dict['dns'].docker_status + "\t\t|| " \
        + _process_dict['dns'].service_status + "\t|\n" \
                                                "| 6. " + _process_dict['dashboard'].process_name + "\t\t|| " + \
        _process_dict['dashboard'].docker_status \
        + "\t\t|| " + _process_dict['dashboard'].service_status + "\t|\n" \
                                                                  "| 7. " + _process_dict[
            'exec'].process_name + "\t|| " + _process_dict['exec'].docker_status + "\t\t|| " \
        + _process_dict['exec'].service_status + "\t|\n" \
                                                 "| 8. " + _process_dict['hyperkube'].process_name + "\t\t\t|| " + \
        _process_dict['hyperkube'].docker_status \
        + "\t\t|| " + _process_dict['hyperkube'].service_status + "\t|\n" \
                                                                  " ---------------------------------------------------------------------------------------\n"
    stdscr.addstr(0, 0, display_str)
    blink('Progress: ' + str(len(_counter) / 8 * 100) + ' %', 0.5)
    stdscr.refresh()


Query().start()

while len(_counter) <= 7:
    display_manager()
time.sleep(3)
display_manager()
