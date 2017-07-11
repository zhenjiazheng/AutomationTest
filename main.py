# coding=UTF-8
# __author__ = 'zhengandy'
import sys
import os
from argparse import ArgumentParser

sys.path.extend(os.path.dirname(os.path.abspath(__file__)))
# print os.path.dirname(os.path.abspath(__file__))


ap = ArgumentParser(
    # prog = __file__,
    description='Automation Test.'
)

ap.add_argument('-P', dest='platform', action="store", type=str, nargs='?', default="api")
ap.add_argument('-F', dest='projectCaseFolder', action='store', type=str, nargs='?', default='Cases\\API\\POS\\BOSS')
ap.add_argument('-N', dest='number', action="store", type=int, nargs='?', default=0)
ap.add_argument('-S', dest='sleep_time', action="store", type=float, nargs='?', default=0)
ap.add_argument('-DB', dest='database', action="store", type=str, nargs='?', default="waiwang")
ap.add_argument('-CL', dest='caselist', action="store", type=str, nargs='?', default="")
ap.add_argument('-MD', dest='method', action="store", type=str, nargs='?', default="DEBUG")
ap.add_argument('-E', dest="email", action="store", type=int, nargs="?", default=0)
ap.add_argument('-L', dest='list', action="store", type=str, nargs='?', default="")

args = ap.parse_args()

os.environ.setdefault('platform', args.platform)
os.environ.setdefault('projectCaseFolder', args.projectCaseFolder)
os.environ.setdefault('UT_ITEM', str(args.number-1))
os.environ.setdefault('SLEEP_TIME', str(args.sleep_time))
os.environ.setdefault('DATABASE', args.database)
os.environ.setdefault('CASELIST', args.caselist)
os.environ.setdefault('METHOD', args.method)
os.environ.setdefault('email', str(args.email))
os.environ.setdefault('testlist', args.list)


platform = os.environ.get('platform', "api")

if platform:
    if os.path.isfile("log.txt"):
        os.remove("log.txt")
    from TestRunner import testRunner
    testRunner.main()
