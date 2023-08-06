#!/usr/bin/env python3

import boto3
import logging
import sys
import json
from botocore.exceptions import ClientError
from datetime import datetime
from pyawscp.Functions import Functions
from pyawscp.Utils import Utils, Style
from pyawscp.PrettyTable import PrettyTable
from pyawscp.Emoticons import Emoticons
from pyawscp.Config import Config
from pyawscp.TableArgs import TableArgs
from pygments import highlight, lexers, formatters

LOG = logging.getLogger("app." + __name__)
LOG.setLevel(logging.INFO)

class PyEc2CP:
    config = None

    def __init__(self, config):
        self.config = config

    # A main function called from user
    # Check if a specific subnetId is Public looking up its Route Table for a IGW-* 0.0.0.0/0
    # arguments:
    #      subnetId: mandatory
    def subnetIsPublic(self):
        ec2      = self.botoSession().client('ec2')
        subnetId = self.config.commandArguments

        if not subnetId:
           resultTxt = "Where is the SubnetId? You didn't tell me which one " + Emoticons.ops() +  Style.RESET
           return Utils.formatResult(Functions.SUBNET_IS_PUBLIC,resultTxt, self.config, "", True)

        filters=[{'Name': 'association.subnet-id','Values': [subnetId]}, 
                 {'Name': 'route.destination-cidr-block','Values': ['0.0.0.0/0']},
                 {'Name': 'route.gateway-id','Values': ['igw-*']}]
        if self.config.awsTagsToFilter():
           for tag in self.config.awsTags: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]}
               ) 
        route_tables = ec2.describe_route_tables(Filters=filters)

        jsonResult = ""
        if self.config.printResults: 
           jsonResult = Utils.dictToJson(route_tables)

        routeTableIgw = route_tables['RouteTables']
        if len(routeTableIgw) >= 1:
           resultTxt = "Subnet " + Style.GREEN + subnetId + Style.RESET + " is " + Style.GREEN + "PUBLIC" +  Style.RESET + "\n"

           printSeparator = False
           for route in routeTableIgw[0]["Routes"]:
               if route["DestinationCidrBlock"] == '0.0.0.0/0':
                  if route["State"]:
                     if not printSeparator:
                        resultTxt = resultTxt + Utils.separator()
                        printSeparator = True
                     resultTxt = resultTxt + "\n"
                     resultTxt = resultTxt + ' '.ljust(2,' ') + "- State...........: " + Style.GREEN + route['State'] + Style.RESET 
                  if route["GatewayId"]:
                     if not printSeparator:
                        resultTxt = resultTxt + Utils.separator()
                        printSeparator = True
                     resultTxt = resultTxt + "\n"
                     resultTxt = resultTxt + ' '.ljust(2,' ') + "- GatewayId.......: " + Style.GREEN + route['GatewayId'] + Style.RESET    
                  if routeTableIgw[0]["VpcId"]:
                     if not printSeparator:
                        resultTxt = resultTxt + Utils.separator()
                        printSeparator = True
                     resultTxt = resultTxt + "\n"
                     resultTxt = resultTxt + ' '.ljust(2,' ') + "- Vpc Id..........: " + Style.GREEN + routeTableIgw[0]['VpcId'] + Style.RESET   
           return Utils.formatResult(Functions.FUNCTIONS[Functions.SUBNET_IS_PUBLIC]["name"],resultTxt, self.config, jsonResult, True, None)
        else:
           resultTxt = ""
           subnet = ec2.describe_subnets(Filters=[{'Name':'subnet-id','Values':[subnetId]}])
           if len(subnet['Subnets']) == 0:
               resultTxt = "Subnet " + Style.GREEN + subnetId + Style.RED + " not found! " + Emoticons.ops() +  Style.RESET
           else:   
               if self.config.awsTagsToFilter():
                  resultTxt = "Subnet " + Style.GREEN + subnetId + Style.RESET + " is NOT " + Style.GREEN + "PUBLIC" +  Style.RESET + ", or either did not pass the Filters Tag! " + + Emoticons.thumbsUp()
               else:   
                  resultTxt = "Subnet " + Style.GREEN + subnetId + Style.RESET + " is NOT " + Style.GREEN + "PUBLIC" +  Style.RESET + " " + Emoticons.thumbsUp() 
           return Utils.formatResult(Functions.FUNCTIONS[Functions.SUBNET_IS_PUBLIC]["name"],resultTxt, self.config, "", True, None)     
    
    # Reusable Function, used by: 
    # -lisSubtnetsVpc
    def _checkSubnetIsPublic(self, subnetId, extraFilters):
        ec2 = self.botoSession().client('ec2')
        filters=[{'Name': 'association.subnet-id','Values': [subnetId]}, 
                 {'Name': 'route.destination-cidr-block','Values': ['0.0.0.0/0']},
                 {'Name': 'route.gateway-id','Values': ['igw-*']}
        ]
        route_tables = ec2.describe_route_tables(Filters=filters)
        routeTableIgw = route_tables['RouteTables']
        if len(routeTableIgw) >= 1:
            return True
        else:
            return False    

    # List all Subnets from a VPC
    def listSubnetsVpc(self):
        ec2   = self.botoSession().client('ec2')

        vpcId     = ""
        isPublic  = False
        tableArgs = TableArgs()
        tableArgs.setArguments(self.config.commandArguments) 

        if "," in self.config.commandArguments:
           vpcId = self.config.commandArguments.split(",")[0]
           tableArgs.setArguments(self.config.commandArguments)
           if "ispublic" in self.config.commandArguments:
               isPublic = True
        else:
           vpcId = tableArgs.cleanPipelineArguments()

        if not vpcId:
           resultTxt = "Where is the VpcId? You didn't tell me which VPC " + Emoticons.ops() +  Style.RESET
           return Utils.formatResult(Functions.LIST_SUBNETS_VPC,resultTxt, self.config, "", True, tableArgs)

        filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    vpcId
                ]
            }
        ]
        if self.config.awsTagsToFilter():
           # Environment Tags set
           for tag in self.config.awsTags: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]}
               )

        # Tags from command line arguments
        if len(tableArgs.tagsTemp) > 0:
           for tag in tableArgs.tagsTemp: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[tableArgs.tagsTemp[tag]]}
               )

        subnets = ec2.describe_subnets( Filters=filters )

        jsonResult = ""
        if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile: 
           jsonResult = Utils.dictToJson(subnets)

        resultTxt = ""
        if len(subnets["Subnets"]) >= 1:
            resultTxt = "The VPC " + Style.GREEN + vpcId + Style.RESET + " has " + Style.GREEN + str(len(subnets["Subnets"])) + Style.RESET + " Subnets\n"
            resultTxt = resultTxt + Utils.separator()  + "\n\n"

            idx_lin=0
            header      = ["#","Subnet Id", "Availability Zone", "CIDR Block", "Available IP Address Count"]
            if isPublic:
                header.append("Is Public?")
            if tableArgs.showTags:
                header.append("Tags")    
            prettyTable = PrettyTable(header)
            
            for subnet in subnets["Subnets"]:
                idx_lin += 1

                columns = [ str(idx_lin), subnet['SubnetId'], subnet['AvailabilityZone'],  subnet['CidrBlock'], subnet['AvailableIpAddressCount'] ]

                if isPublic:
                   resultIsPublic = self._checkSubnetIsPublic(subnet['SubnetId'], None)
                   result = "--- "
                   if resultIsPublic:
                      result = "PUBLIC"
                   columns.append(result)
                if tableArgs.showTags:
                   tags = Utils.formatPrintTags(subnet['Tags'])
                   columns.append(tags)

                prettyTable.addRow(columns)

            if (int(tableArgs.sortCol) - 1) > len(columns):
                tableArgs.sortCol = "1"
            prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
            prettyTable.ascendingOrder(not tableArgs.desc)
            result = "VPC...: " + Style.GREEN + vpcId + Style.RESET + "\n\n" + prettyTable.printMe(self.config.tableLineSeparator, tableArgs)
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_SUBNETS_VPC]["name"], result, self.config, jsonResult, True, tableArgs)
        else:
           resultTxt = ""
           try: 
             vpc = ec2.describe_vpcs(VpcIds=[vpcId])
             if not self.config.awsTagsToFilter():
                resultTxt = "VPC was found, but there's no Subnet associated. " + Emoticons.ops()
             else:   
                resultTxt = "VPC was found, but there's no Subnet associated or either did not pass the Filters Tag! " + Emoticons.ops()
           except ClientError as e:
             if "InvalidVpcID.NotFound" == e.response['Error']['Code']:
                resultTxt = "VPC with the Id " + Style.GREEN + vpcId + Style.RESET + " was not found! " + Emoticons.ops() +  Style.RESET
             else:    
                resultTxt = "Exception! ❌💣 " + Style.GREEN + e.response['Error']['Code'] + Style.RESET
           except:
             resultTxt = sys.exc_info + " ❌💣 "
           return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_SUBNETS_VPC]["name"], resultTxt, self.config, "", True, tableArgs)

    # List all VPCs
    def listVpc(self):
        ec2 = self.botoSession().client('ec2')

        tableArgs = TableArgs()
        tableArgs.setArguments(self.config.commandArguments)

        listSubnets    = False
        subnetIsPublic = False

        if "subnets" in self.config.commandArguments:
           listSubnets    = True
        if "ispublic" in self.config.commandArguments:
           subnetIsPublic = True   

        filters = []
        if self.config.awsTagsToFilter():
           # Tags from Environment
           for tag in self.config.awsTags: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]}
               )

        # Tags from command line arguments
        if len(tableArgs.tagsTemp) > 0:
           for tag in tableArgs.tagsTemp: 
               filters.append(
                   {'Name':'tag:' + tag,'Values':[tableArgs.tagsTemp[tag]]}
               )
        vpcs = ec2.describe_vpcs(Filters=filters)

        jsonResult = ""
        if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile:
           jsonResult = Utils.dictToJson(vpcs)

        resultTxt = ""
        if len(vpcs["Vpcs"]) >= 1:
            resultTxt = "List of VPCs, total of " + Style.GREEN + str(len(vpcs["Vpcs"])) + Style.RESET + "\n"
            resultTxt = resultTxt + Utils.separator()  + "\n\n"

            idx_lin=0
            header = ["#","VPC Id", "CIDR Block", "Default"]
            if listSubnets:
               header = ["#","VPC Id", "CIDR Block", "Default", "Subnet Id", "Subnet CIDR Block", "AZ", "Available IP Count"] 
               if subnetIsPublic:
                  header.append("Is Public?")
            if tableArgs.showTags:
               header.append("VPC Tags")       

            prettyTable = PrettyTable(header)
            for vpc in vpcs["Vpcs"]:
                idx_lin += 1

                vpcId     = vpc['VpcId']
                cidrBlock = vpc['CidrBlock']
                default   = "Default" if vpc['IsDefault'] else "---"
                columns   = None
                # Asked to list the subnets of each VPC?
                if listSubnets:
                   subnets = ec2.describe_subnets( Filters=[{'Name': 'vpc-id','Values': [vpc['VpcId']]}])
                   idx_subnet_lin = 0

                   for subnet in subnets["Subnets"]:
                       idx_subnet_lin += 1
                       lblSubnet = subnet['SubnetId'] + "  (" + str(idx_subnet_lin) + ")"
                       cidrBlockSubnet = subnet['CidrBlock']
                       az = subnet['AvailabilityZone']
                       availableIpdAddressCount = subnet['AvailableIpAddressCount']

                       columns = [ idx_lin, vpcId, cidrBlock, default, lblSubnet, cidrBlockSubnet, az, availableIpdAddressCount ]

                       # Asked to inform if the Subnet is Public? 
                       if subnetIsPublic:
                          resultSubnetIsPublic = "--- "
                          if self._checkSubnetIsPublic(subnet['SubnetId'], None) :
                             resultSubnetIsPublic = "PUBLIC"
                          columns.append(resultSubnetIsPublic)
                       if tableArgs.showTags:
                          tags = Utils.formatPrintTags(vpc['Tags'])
                          columns.append(tags)   

                       prettyTable.addRow(columns)

                   prettyTable.addSeparatorGroup()    
                else:   
                   columns = [ idx_lin, vpcId, cidrBlock, default ]
                   if tableArgs.showTags:
                      tags = Utils.formatPrintTags(vpc['Tags'])
                      columns.append(tags)
                   prettyTable.addRow(columns)

            if (int(tableArgs.sortCol) - 1) > len(columns):
                sortCol = "1"

            prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
            prettyTable.ascendingOrder(not tableArgs.desc)
            result = "VPCs " + "\n\n" + prettyTable.printMe(self.config.tableLineSeparator, tableArgs)
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_VPC]["name"], result, self.config, jsonResult, True, tableArgs)    
        else:
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_VPC]["name"], " No VPC found " + Emoticons.ops(), self.config, jsonResult, True, tableArgs)         

    # List all Ec2 Instances
    def listEc2(self):
       ec2              = self.botoSession().client('ec2')
       instanceId       = None
       privateIPFilter  = None
       vpcIdFilter      = None
       subnetIdFilter   = None
       showSg           = False
       showVpc          = False
       showSubnet       = False
       showImage        = False
       showCpu          = False
       hideName         = False

       tableArgs = TableArgs()
       tableArgs.setArguments(self.config.commandArguments)
       if "," in self.config.commandArguments:
          for arg in self.config.commandArguments.split(","):
              if "i-" in arg:
                 instanceId = arg
              elif arg == "sg":
                 showSg = True
              elif arg == "vpc":
                 showVpc = True    
              elif arg == "subnet":
                 showSubnet = True   
              elif arg == "image":
                 showImage = True 
              elif arg == "cpu":
                 showCpu = True
              elif arg == "noname":
                 hideName = True
              elif arg.startswith("vpc-"):
                 vpcIdFilter = arg
              elif arg.startswith("subnet-"):
                 subnetIdFilter = arg              
              else:
                 # Check IP
                 if Utils.isNumber(arg[0:2]):
                    privateIPFilter = arg

       else:
          arg = self.config.commandArguments
          if "i-" in arg:
            instanceId = arg
          elif arg == "sg":
             showSg = True
          elif arg == "vpc":
             showVpc = True    
          elif arg == "subnet":
             showSubnet = True   
          elif arg == "image":
             showImage = True 
          elif arg == "cpu":
             showCpu = True
          elif arg == "noname": 
             hideName = True
          elif arg.startswith("vpc-"):
             vpcIdFilter = arg
             print(arg)
          elif arg.startswith("subnet-"):
             subnetIdFilter = arg   
          else:
             # Check IP
             if Utils.isNumber(arg[0:2]):
                privateIPFilter = arg


       filters=[]   

       if instanceId:
          filters.append({'Name': 'instance-id','Values': [instanceId]})   
       if privateIPFilter:   
          filters.append({'Name': 'private-ip-address','Values': [privateIPFilter]})
       if vpcIdFilter:   
          filters.append({'Name': 'vpc-id','Values': [vpcIdFilter]})
       if subnetIdFilter:   
          filters.append({'Name': 'subnet-id','Values': [subnetIdFilter]})         

       if self.config.awsTagsToFilter():
           # Environment Tags set
           for tag in self.config.awsTags: 
               filters.append({'Name':'tag:' + tag,'Values':[self.config.awsTags[tag]]})   

       # Tags from command line arguments
       if len(tableArgs.tagsTemp) > 0:
          for tag in tableArgs.tagsTemp: 
              filters.append({'Name':'tag:' + tag,'Values':[tableArgs.tagsTemp[tag]]})        

       reservations = ec2.describe_instances( Filters=filters )        

       jsonResult = ""
       if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile: 
          jsonResult = Utils.dictToJson(reservations)

       if reservations and len(reservations["Reservations"]) > 0:
  
          idx_lin = 0

          if hideName:
             header = ["#","Instance Id",       "Type","Launch Time", "Private IP", "Public IP", "State"]
          else:   
             header = ["#","Instance Id","Name","Type","Launch Time", "Private IP", "Public IP", "State"]

          if showSg:             
             header.append("Security Groups")
          if showImage:          
             header.append("Image Id")
          if showCpu:            
             header.append("CPU Options")
          if showVpc:            
             header.append("VPC")
          if showSubnet:         
             header.append("Subnet")
          if tableArgs.showTags: 
             header.append("Tags")

          prettyTable = PrettyTable(header)

          totalListed = 0

          for instanceGroup in reservations["Reservations"]:
              for instance in instanceGroup["Instances"]:
                  idx_lin     += 1
                  totalListed += 1

                  if not hideName:
                     name = ""
                     for t in instance['Tags']:
                         if t["Key"] == "Name":
                            name = t["Value"]

                  launchTimeDate = ""
                  if instance['LaunchTime']:
                     launchTimeDate = instance['LaunchTime'].strftime("%d-%b-%y %H:%M")

                  privateIp = instance['PrivateIpAddress'] if "PrivateIpAddress" in instance else ""
                  publicIp  = instance["PublicIpAddress"] if "PublicIpAddress" in instance else ""
                  state     = instance["State"]["Name"]
                  state     = Style.CYAN + state + Style.RESET if state == "stopped" else state

                  if hideName:
                     columns = [ str(idx_lin), str(instance['InstanceId']), instance['InstanceType'], launchTimeDate, privateIp, publicIp, state ]
                  else:   
                     columns = [ str(idx_lin), str(instance['InstanceId']), name, instance['InstanceType'], launchTimeDate, privateIp, publicIp, state ]

                  if showSg:
                     securityGroups = ""
                     for sg in instance["SecurityGroups"]:             
                         if securityGroups != "": securityGroups += ","
                         securityGroups += sg["GroupId"]
                     columns.append(securityGroups)    
                  if showImage:          
                     columns.append(instance["ImageId"])       
                  if showCpu:   
                     cpu  = Style.MAGENTA + "Core:"    + Style.GREEN + str(instance["CpuOptions"]["CoreCount"]) + Style.RESET + " "
                     cpu += Style.MAGENTA + "Threads:" + Style.GREEN + str(instance["CpuOptions"]["ThreadsPerCore"])
                     columns.append(cpu)       
                  if showVpc:            
                     vpc = instance["VpcId"]
                     columns.append(vpc)
                  if showSubnet:         
                     subnet = instance["SubnetId"]
                     columns.append(subnet)
                  if tableArgs.showTags:
                     tags = Utils.formatPrintTags(instance['Tags'])
                     columns.append(tags)

                  prettyTable.addRow(columns)

          resultTxt = ""

          if instanceId:
             if resultTxt != "": resultTxt = resultTxt + "\n"
             resultTxt = resultTxt + "      Instance Id........: " + Style.GREEN + instanceId + Style.RESET
          if privateIPFilter:   
             if resultTxt != "": resultTxt = resultTxt + "\n"
             resultTxt = resultTxt + "      Private IP Address.: " + Style.GREEN + privateIPFilter + Style.RESET
          if vpcIdFilter:   
             if resultTxt != "": resultTxt = resultTxt + "\n"
             resultTxt = resultTxt + "      VPC Id.............: " + Style.GREEN + vpcIdFilter + Style.RESET
          if subnetIdFilter:   
             if resultTxt != "": resultTxt = resultTxt + "\n"
             resultTxt = resultTxt + "      Subnet Id..........: " + Style.GREEN + subnetIdFilter + Style.RESET

          resultTxt = resultTxt + "\n\n Total of EC2s...: " + Style.GREEN + format(totalListed,",") + Style.RESET   

          if (int(tableArgs.sortCol) - 1) > len(columns):
              tableArgs.sortCol = "1"
          prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
          prettyTable.ascendingOrder(not tableArgs.desc)
          result = resultTxt + "\n\n" + prettyTable.printMe(self.config.tableLineSeparator, tableArgs)
          return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_EC2]["name"], result, self.config,jsonResult, True, tableArgs)    
       else:
          resultTxt = ""
          resultTxt = "No EC2 Instance was found. " + Emoticons.ops()
          return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_EC2]["name"], resultTxt, self.config, "", True, tableArgs)

    def botoSession(self):
        return self.config.botoSession()

if __name__ == '__main__':
    config = Config()
    config.awsProfile = "ecomm"
    config.awsRegion = "eu-central-1"
    config.printResults = True
    #config.awsTags["Environment"] = "production"
    config.tableLineSeparator = False
    
    
    # subnets, is-public (only with subnets active)
    # sort1,desc (when requested together with subnets, the group lines will be omitted)
    if len(sys.argv) > 1:
       config.commandArguments = sys.argv[1]
    pyEc2CP = PyEc2CP(config)
    report = pyEc2CP.listEc2()
    Utils.addToClipboard(report)
    print(report)

    # TODO:
    # findEc2 (by IP, by InstanceId, by Tag, etc.)
    # Result show: IP, t3.medium, region, subnet, vpc, security group, (attached Load Balancer optional), (Security Groups Rules optional)
