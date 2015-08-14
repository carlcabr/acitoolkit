import sys
from  acitoolkit.acitoolkit import *

# Creating an empty tenant list.
tenant_list =[]

# Let's create 50 tenants, with all their EPGs, VRFs, BDs...because...why not?
for i in range(1, 50):

    #Tenant Creation - basically, the names will be Matrix1, Matrix2...you get it. That's why my str(i) is there.
    tenant = Tenant('Matrix'+ str(i))
    
    #My VRF creation, under the Tenant Matrix created above
    context= Context('Matrix-Router' + str(i), tenant)
    
    #My BridgeDomain, under the Context/Tenant created above
    bd = BridgeDomain('BD1-'+str(i), tenant)
    bd.add_context(context)
    
    #Creation of the AppProfile - Will you take the Red or the Blue pill? too many pills here :)
    app = AppProfile('RedOrBlueANP' + str(i), tenant)
    
    #Create the EPG RED and attach it to the BD1
    red = EPG('RED' + str(i), app )
    red.add_bd(bd)
    
    #Create the EPG BLUE and attach it to the BD1
    blue = EPG('BLUE' + str(i), app )
    blue.add_bd(bd)     

    # Adding the newly created the Tenant to our list. Next please...
    tenant_list.append(tenant)


# Getting credentials from the command line.
description = 'VoD application'
creds = Credentials('apic', description)
creds.add_argument('--delete', action='store_true',
               help='Delete the configuration from the APIC')
               
args = creds.get()

# Delete the configuration if desired
if args.delete:
            tenant.mark_as_deleted()

# Login to APIC
session = Session(args.url, args.login, args.password)
session.login()

# Now we'll actually push what we created. All the tenants in our list.
for tenant in tenant_list:
    
    if args.delete:
        tenant.mark_as_deleted()
        
    resp = tenant.push_to_apic(session)
    if resp.ok:
        print 'Success'

    # Print what was sent
    print 'Pushed the following JSON to the APIC'
    print 'URL:', tenant.get_url()
    print 'JSON:', tenant.get_json()
    print






















