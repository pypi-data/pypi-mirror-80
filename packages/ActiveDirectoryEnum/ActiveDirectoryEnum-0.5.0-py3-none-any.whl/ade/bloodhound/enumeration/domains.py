####################
#
# Copyright (c) 2018 Fox-IT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
####################

import logging
import codecs
import json
from . .ad.utils import ADUtils, AceResolver
from . .ad.trusts import ADDomainTrust
from .acls import parse_binary_acl

class DomainEnumerator(object):
    """
    Class to enumerate trusts in the domain.
    Contains the dumping functions which
    methods from the bloodhound.ad module.
    """
    def __init__(self, addomain, addc):
        """
        Trusts enumeration. Enumerates all trusts between the source domain
        and other domains/forests.
        """
        self.addomain = addomain
        self.addc = addc

    def dump_domain(self, collect, filename='domains.json'):
        """
        Dump trusts. This is currently the only domain info we support, so
        this function handles the entire domain dumping.
        """
        if 'trusts' in collect:
            entries = self.addc.get_trusts()
        else:
            entries = []

        try:
            logging.debug('Opening file for writing: %s' % filename)
            out = codecs.open(filename, 'w', 'utf-8')
        except:
            logging.warning('Could not write file: %s' % filename)
            return

        # If the logging level is DEBUG, we ident the objects
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            indent_level = 1
        else:
            indent_level = None

        # Todo: fix this properly. Current code is quick fix to work with domains
        # that have custom casing in their DN
        domain_object = None
        for domain in self.addomain.domains.keys():
            if domain.lower() == self.addomain.baseDN.lower():
                domain_object = self.addomain.domains[domain]
                break

        if not domain_object:
            logging.error('Could not find domain object. Aborting domain enumeration')
            return

        # Initialize json structure
        datastruct = {
            "domains": [],
            "meta": {
                "type": "domains",
                "count": 0,
                "version":3
            }
        }
        # Get functional level
        level_id = ADUtils.get_entry_property(domain_object, 'msds-behavior-version')
        try:
            functional_level = ADUtils.FUNCTIONAL_LEVELS[int(level_id)]
        except KeyError:
            functional_level = 'Unknown'

        domain = {
            "ObjectIdentifier": domain_object['attributes']['objectSid'],
            "Properties": {
                "name": self.addomain.domain.upper(),
                "domain": self.addomain.domain.upper(),
                "highvalue": True,
                "objectid": ADUtils.get_entry_property(domain_object, 'objectSid'),
                "distinguishedname": ADUtils.get_entry_property(domain_object, 'distinguishedName'),
                "description": ADUtils.get_entry_property(domain_object, 'description'),
                "functionallevel": functional_level
            },
            "Trusts": [],
            "Aces": [],
            # The below is all for GPO collection, unsupported as of now.
            "Links": [],
            "Users": [],
            "Computers": [],
            "ChildOus": []
        }

        if 'acl' in collect:
            resolver = AceResolver(self.addomain, self.addomain.objectresolver)
            _, aces = parse_binary_acl(domain, 'domain', ADUtils.get_entry_property(domain_object, 'nTSecurityDescriptor'), self.addc.objecttype_guid_map)
            domain['Aces'] = resolver.resolve_aces(aces)

        if 'trusts' in collect:
            num_entries = 0
            for entry in entries:
                num_entries += 1
                trust = ADDomainTrust(ADUtils.get_entry_property(entry, 'name'), ADUtils.get_entry_property(entry, 'trustDirection'), ADUtils.get_entry_property(entry, 'trustType'), ADUtils.get_entry_property(entry, 'trustAttributes'), ADUtils.get_entry_property(entry, 'securityIdentifier'))
                domain['Trusts'].append(trust.to_output())

            logging.info('Found %u trusts', num_entries)

        # Single domain only
        datastruct['meta']['count'] = 1
        datastruct['domains'].append(domain)
        json.dump(datastruct, out, indent=indent_level)

        logging.debug('Finished writing domain info')
        out.close()
