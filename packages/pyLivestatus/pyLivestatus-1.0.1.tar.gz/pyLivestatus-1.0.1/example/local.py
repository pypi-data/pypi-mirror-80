# 
# ELMEC INFORMATICA - CONFIDENTIAL
# __________________
# 
#  [2020] Elmec Informatica
#  All Rights Reserved.
#  Author: BosettiE
#  Data:  29/09/2020
# __________________
# NOTICE:  All information contained herein is, and remains
# the property of Elmec Informatica and its suppliers,
# if any.  The intellectual and technical concepts contained
# herein are proprietary to Elmec Informatica
# and its suppliers and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material
# is strictly forbidden unless prior written permission is obtained
# from Elmec Informatica.
from pprint import pprint

from pyLivestatus import Livestatus

if __name__ == '__main__':
    livestatus = Livestatus('172.16.254.95', '6557')  # host and port of livestatus socket
    livestatus.set_separator(28, 29, 30, 31)
    hosts = livestatus.get_hosts()  # return array with details for all hosts
    pprint(hosts)
    # livestatus.get_host('my_host')  # return details for host 'my_host'
    services = livestatus.get_services(
        'ELMEC_elmec-internet-varese')  # return details for every service of host 'my_host'
    for service in services:
        pprint(service['service_description'])
