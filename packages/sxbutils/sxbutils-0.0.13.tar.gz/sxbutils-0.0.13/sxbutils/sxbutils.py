import os
from datetime import datetime
from pytz import timezone
import pytz

c="sxbutils"

def do_stuff():
    m=c+".do_stuff"
    print (m+" 0.0.13") # <- Update/Match this with ../*setup*
    print (m+" "+str(datetime.now()))
    new_zone_name="America/New_York"
    new_zone = timezone(new_zone_name)
    new_dt = datetime.now().astimezone(new_zone)
    print (m+" "+str(new_dt))


def validate_envvars(envvars):

    m=c+".validate_envvars"
    print(m+" Starts")

    count=0
    try:
       for envvar in envvars:
          count += 1
          if not envvar.name in os.environ and envvar.required:
              message=m+" missing envvar ("+envvar.name+") and it is required"
              raise Exception(message)
          print(m+" envvar="+envvar.name+" value="+str(os.environ.get(envvar.name)))

    except Exception as e:
       message=m+" An exception occurred, error="+str(e)+""
       raise Exception(message)

    finally:
       print(m+" Finally")

    print(m+" validated "+str(count)+" envvars")

