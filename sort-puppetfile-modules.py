#!/usr/bin/env python3

'''Sort module definitions in a Puppetfile.

Usage: python3 sort-puppetfile-modules.py

Reads `./Puppetfile` and outputs sorted version to stdout.

This is alpha quality code, it handles non-module lines before module specs (eg
shebang, ruby code, etc), but not after.
'''

###
# Example supported Puppetfile:
###
# #!/usr/bin/ruby env
#
# require 'rubygems'
#
# forge "https://forgeapi.puppetlabs.com"
#
# # Internal dependencies:
#
# mod 'datadog/datadog_agent',
#   :git => '...',
#   :ref => 'dev'
# mod 'dwerder/graphite',
#   :git => '...',
#   :ref => 'dev'

DEBUG = False


def debug(msg):
    if DEBUG:
        print(msg)

# This is essentially a low quality state machine
with open('Puppetfile') as f:
    in_module = False
    current_module = []
    pre_module_data = []
    module_data = []
    for line in f:
        line = line.rstrip()
        debug(line)
        if not current_module and not module_data and not line.startswith('mod'):
            debug('pre module data')
            pre_module_data.append(line)
            continue
        if line.startswith('mod'):
            debug('start of module')
            in_module = True
            if current_module:
                module_data.append(current_module)
            current_module = [line]
            continue
        if in_module and line.startswith(' '):
            debug('continuing module')
            current_module.append(line)
            continue
        # We would hit this with:
        # Any blank lines after the first module
        # Any non-module lines after modules
        debug("Unknown line: %s" % line)
        assert False

module_data.append(current_module)

print('\n'.join(pre_module_data))
for module in sorted(module_data, key=lambda m: m[0]):
    print('\n'.join(module))
