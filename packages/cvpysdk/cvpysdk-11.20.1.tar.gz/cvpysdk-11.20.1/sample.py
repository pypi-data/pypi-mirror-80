# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 11:56:12 2020

@author: spakhare
"""

from cvpysdk.commcell import Commcell
c = Commcell('172.16.62.219', 'admin', 'Builder!12')

cg = c.client_groups.get('Azure_Cloud10')

print(cg.associated_clients)
cg.add_clients('unixtest4')
print(cg.associated_clients)

j = cg.push_servicepack_and_hotfix()

print(j)

print(j.status)

cg.remove_clients('unixtest4')

print(cg.associated_clients)
cg.remove_all_clients()

print(cg.associated_clients)

print(cg.description)
cg.description = 'test'

print(cg.description)

print(cg.clientgroup_name)
cg.clientgroup_name = cg.clientgroup_name

print(cg.name)

cg.clientgroup_name = 'Azure_cloud10'

print(cg.name)