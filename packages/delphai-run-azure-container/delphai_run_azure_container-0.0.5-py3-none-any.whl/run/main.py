#-------------------------------------------------------------------------
# Copyright (c) Delphai Corporation. All rights reserved.
# Licensed under the MIT License. See LICENCE in the project root for
# license information.
# Auther: Ahmed => DevOps/Delphai
#--------------------------------------------------------------------------

import azure.common.exceptions
from azure.mgmt.resource import ResourceManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (ContainerGroup, Container, ContainerPort, Port, IpAddress,
                                                 ResourceRequirements, ResourceRequests, ContainerGroupNetworkProtocol, OperatingSystemTypes, image_registry_credential)


def create_container_instance(_subscription_id:str, _client_id:str, _client_secret:str, _tenant_id:str, _resource_group:str , _container_group:str, _container_name:str, _image:str, _image_credentials:list=None, _command=None):
  '''
    :arg:
  '''
  # Authenticate to Azure Cloud
  try:
    print(':debug: Authenticating...')
    azure_context = AzureContext(subscription_id=_subscription_id, client_id=_client_id,
                        client_secret=_client_secret, tenant=_tenant_id)
    print('Authenticated to azure')
  except:
    print('Please make sure you have passed the right credentials')

  # Construct Client
  print(':debug: Setting client construct...')
  resource_client = ResourceManagementClient(
    azure_context.credentials, azure_context.subscription_id)

  client = ContainerInstanceManagementClient(
    azure_context.credentials, azure_context.subscription_id)
  
  container_groups = list_container_groups(client)
  print(container_groups)
  if _container_group in container_groups:
    print(f':debug: Container group ({_container_group}) exists in subscription {_subscription_id}')
  else:
    print(f':debug: Container group ({_container_group}) does not exist in subscription {_subscription_id}')
    raise Exception("Make sure Container Group exists")
    exit()
  
  #Create Container
  if _image_credentials != None:
    server = _image_credentials['server']
    _image_credentials = image_registry_credential.ImageRegistryCredential(server=server)
  else:
    _image_credentials = None
  create_container(client=client, resource_group=_resource_group, container_name=_container_name, image=_image, image_cred=_image_credentials ,command=_command)

  print(':debug: Showing Results')
  show_container_group(client=client,resource_group_name=_resource_group,name=_container_name)

# -------------------------#
#        MAIN UP           #
# -------------------------#
def list_container_groups(client:ContainerInstanceManagementClient):
    container_groups = client.container_groups.list()
    cg = []
    for container_group in container_groups:
        cg.append(container_group.name)
        # print("\t{0}: {{ location: '{1}', containers: {2} }}".format(
        #       container_group.name,
        #       container_group.location,
        #       len(container_group.containers))
        #       )
    return cg

def create_container(client:ContainerInstanceManagementClient, resource_group:str , container_name:str, image:str, image_cred ,container_resource_requirements = None, 
                      environment_variables = None, command = None, port = 80, memory = 1, cpu = 1,
                      container_os=OperatingSystemTypes.linux, IP_type='public', protocol=ContainerGroupNetworkProtocol.tcp):
  
  # set memory and cpu
  print(':debug: setting container configrations')
  container_resource_requests = ResourceRequests(
        memory_in_gb=memory, cpu=cpu)

  container_resource_requirements = ResourceRequirements(
        requests=container_resource_requests)

  container = Container(name=container_name,
                          image=image,
                          resources=container_resource_requirements,
                          command=command.split(),
                          ports=[ContainerPort(port=port)],
                          environment_variables=environment_variables)
  
  cgroup_os_type = container_os
  container_ip_address = IpAddress(type=IP_type, ports=[Port(protocol=protocol, port=port)])
  

  print(':debug: Setting Container group configrations')
  cgroup = ContainerGroup(location='westeurope',
                            containers=[container],
                            os_type=cgroup_os_type,
                            ip_address=container_ip_address,
                            image_registry_credentials=image_cred)
  
  #Create Container
  print(':debug: Creating container instance')
  client.container_groups.create_or_update(resource_group, container_name, cgroup)
  print(f'CONTAINER {container_name} CREATED')


def show_container_group(client:ContainerInstanceManagementClient,resource_group_name, name):
    cgroup = client.container_groups.get(resource_group_name, name)

    print('\n{0}\t\t\t{1}\t{2}'.format(
        'name', 'location', 'provisioning state'))
    print('---------------------------------------------------')
    print('{0}\t\t{1}\t\t{2}'.format(cgroup.name,
                                     cgroup.location, cgroup.provisioning_state))

# Azure Context                                    
class AzureContext(object):
    def __init__(self, subscription_id, client_id, client_secret, tenant):
        self.credentials = ServicePrincipalCredentials(
            client_id=client_id,
            secret=client_secret,
            tenant=tenant
        )
        self.subscription_id = subscription_id
