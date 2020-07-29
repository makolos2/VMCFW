# VMCFW - nsxtexport.py

VMware Cloud on AWS SDDC NSX-T firewall rule and object export tool

Exports JSON objects for the 2 Edge firewalls (MGW + CGW), as well as objects for both MGW + CGW.
Ouputs to console, with the following sections:
- MGW Groups
- CGW Groups
- Services
- MGW Rules
- CGW Rules
- DFW Rules

Note that DFW uses the CGW Objects.
Only user objects are exported. System Groups & Services are not included.


Installation

Requires python 2.7 with modules:

    argparse (https://docs.python.org/2.7/library/argparse.html)

Usage

usage: nsxtexport.py [-h] orgid sddcid refreshtoken

Known limitations
- No import capabilities
