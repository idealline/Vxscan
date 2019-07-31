# coding=utf-8
import re
import sys
from lib.bcolors import bcolors
from lib.iscdn import iscdn
from virustotal_python import Virustotal
from lib.settings import VIRUSTOTAL_API
from plugins.PassiveReconnaissance.ip_history import ipinfo


def virustotal(host):
    # VT接口，主要用来查询PDNS，绕过CDN
    pdns = []
    history_ip = []
    sys.stdout.write(bcolors.RED + "PDNS：\n" + bcolors.ENDC)
    if VIRUSTOTAL_API:
        try:
            vtotal = Virustotal(VIRUSTOTAL_API)
            if re.search(r'\d+\.\d+\.\d+\.\d+', host):
                return None
            resp = vtotal.domain_report(host)
            if resp.get('status_code') != 403:
                for i in resp.get('json_resp').get('resolutions'):
                    address = i.get('ip_address')
                    timeout = i.get('last_resolved')
                    if iscdn(address):
                        history_ip.append(address + ' : ' + timeout)
                pdns = history_ip[10:]
        except:
            pass
    pdns.extend(ipinfo(host))
    if pdns:
        sys.stdout.write(bcolors.OKGREEN + "\n".join("[+] " + str(i) for i in pdns[:10]) + "\n" + bcolors.ENDC)
    else:
        sys.stdout.write(bcolors.OKGREEN + '[+] None \n' + bcolors.ENDC)
    return pdns
