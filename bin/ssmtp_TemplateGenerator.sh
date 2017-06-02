#!/bin/sh
#WDN
#define parameters which are passed in.
fromAddrOfficial=$1
smtpServerAphp=$2

#define the template.
cat  << EOF

#
# Config file for sSMTP sendmail
#
# The person who gets all mail for userids < 1000
# Make this empty to disable rewriting.
root=$fromAddrOfficial


# The place where the mail goes. The actual machine name is required no 
# MX records are consulted. Commonly mailhosts are named mail.domain.com
#mailhub=mail
mailhub=$smtpServerAphp

# Where will the mail seem to come from?
#rewriteDomain=

# The full hostname
hostname=Analysis-Manager

# Are users allowed to set their own From: address?
# YES - Allow the user to specify their own From: address
# NO - Use the system generated From: address
#UseTLS=YES
#UseSTARTTLS=YES
#FromLineOverride=YES

EOF
