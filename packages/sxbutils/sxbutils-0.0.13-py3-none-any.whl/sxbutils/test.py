import sxbutils
from envvar import envvar 

def test_stub():
    try:
        m="test_stub"
        sxbutils.do_stuff()
        report=envvar("REPORT", True, "sxb.txt", "The report env var")
        diddle=envvar("DIDDLE", False, "did", "The DIDDLE env var")

        envvars=[]
        envvars.append(report)
        envvars.append(diddle)
        print(m+" report.tostr()="+report.tostr())

# External lib
        sxbutils.validate_envvars(envvars)

    except Exception as e:
       print(m+" An exception occurred, error="+str(e)+"")

    finally:
       print(m+" Finally")

def test2():
    m="test2"
    #print(sxbutils.__version__)


test_stub()
test2()
