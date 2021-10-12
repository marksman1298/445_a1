import argparse, sys
from formatRequest import formatGet, formatPost


parser = argparse.ArgumentParser(
    description="httpc is a curl-like application but supports HTTP protocol only.",
     epilog="""Use "help [command]" for more information about a command.""",
    add_help=False
)
subparser = parser.add_subparsers(
    title="The commands are",
    help="""
get executes a HTTP GET request and prints the response.
post executes a HTTP POST request and prints the response.
help prints this screen.""")


getParser = subparser.add_parser("get", add_help=False)
getParser.add_argument("-v", help="""Prints the detail of the response such as protocol, status,
and headers.""", action="store_true", dest="VERBOSE", default=False)
getParser.add_argument("-h", help="""key:value Associates headers to HTTP Request with the format
'key:value'.""", action="append", dest="HEADERS", metavar="key:value", default=[])
getParser.add_argument("url", help="url", metavar="URL")
getParser.add_argument("-o", help="–o filename allow the HTTP client to write the body of the response to the specified file instead of the console", dest="OUTPUTFILE", default=False)

postParser = subparser.add_parser("post", add_help=False)
postParser.add_argument("-v", action="store_true", help="""Prints the detail of the response such as protocol, status,
and headers.""", dest="VERBOSE", default=False)
postParser.add_argument("-h", help="""Associates headers to HTTP Request with the format'key:value'.""", action="append", dest="HEADERS", metavar="key:value", default=[])
postParser.add_argument("-d", help="""Associates an inline data to the body HTTP POST request.'.""", metavar="string", dest="DATA")
postParser.add_argument("-f", help=("""Associates the content of a file to the body HTTP POST request. 
Either [-d] or [-f] can be used but not both."""), metavar="file", dest="FILE")
postParser.add_argument("url", help="request url", metavar="URL")
postParser.add_argument("-o", help="–o filename allow the HTTP client to write the body of the response to the specified file instead of the console", dest="OUTPUTFILE", default=False)

helpParser = subparser.add_parser("help", add_help=False)
helpParser.add_argument("requestType", metavar="requestType", choices=("get", "post"), nargs="?")

args = parser.parse_args()


try:
    if sys.argv[1].lower() == "get":
        formatGet(args)
    elif sys.argv[1].lower() == "post":
        formatPost(args)
    else:
        raise AttributeError
except AttributeError:
    if args.requestType is None:
        parser.print_help()
    elif args.requestType == "get":
        getParser.print_help()
    elif args.requestType == "post":
        postParser.print_help()


