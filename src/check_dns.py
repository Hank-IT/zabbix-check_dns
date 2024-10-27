#!/usr/bin/env python3

import sys, getopt, json, dns.resolver

def main(argv):
    nameserver = '8.8.8.8'
    hostname = 'hank-it.com'
    expected = "49.12.229.2"
    record = 'A'
    port = 53

    expect_exists = None

    opts, args = getopt.getopt(argv, "", ["nameserver=", "hostname=", "record=", "port=", "expected="])

    for opt, arg in opts:
        if opt in "--nameserver":
            nameserver = arg
        elif opt in "--hostname":
            hostname = arg
        elif opt in '--record':
            record = arg
        elif opt in '--port':
            port = arg
        elif opt in '--expected':
            expected = arg

    try:
        answer = dns.resolver.resolve_at(nameserver, hostname, record, port=port)

        if expected:
            expect_exists = 0

            for entry in answer:
                if str(entry) == expected:
                    expect_exists = 1

        print(json.dumps({"alive": 1, "expected_exists": expect_exists, "nameserver": nameserver, "hostname": hostname, "record": record, "port": port, "expected": expected}))
    except dns.resolver.LifetimeTimeout:
        print(json.dumps({"alive": 0, "error": "timeout", "nameserver": nameserver, "hostname": hostname, "record": record, "port": port, "expected": expected}))
    except Exception as e:
        print(json.dumps({"alive": 0, "error": repr(e), "nameserver": nameserver, "hostname": hostname, "record": record, "port": port, "expected": expected}))

if __name__ == "__main__":
    main(sys.argv[1:])