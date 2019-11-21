#!/usr/bin/env python

import optparse

import osint_runner


def run(email, output=None):
    osint_runner.run("email", "emails", email, output)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-o', '--output', action="store", dest="output", help="Save output in either JSON or HTML")
    options, args = parser.parse_args()
    email = args[0]
    run(email, options.output)
