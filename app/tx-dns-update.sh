#!/bin/bash
echo ${PATH}
export PATH=${PATH}:/app
export PYTHONPATH=${PYTHONPATH}:/app

echo 'usage: python tx-dns-update.py --access_key_id ${SECRETID} --access_key_secret ${SECRETKEY} --subdomain ${SUBDOMAIN} --domain ${DOMAIN}'
if [[ -z ${SECRETID} ]];then
echo 'please provides your env for tencent cloud SECRETID'
exit 1
fi
if [[ -z ${SECRETKEY} ]];then
echo 'please provides your env for tencent cloud SECRETKEY'
exit 1
fi
if [[ -z ${SUBDOMAIN} ]];then
echo 'please provides your env for tencent cloud SUBDOMAIN='
exit 1
fi
if [[ -z ${SUBDOMAIN} ]];then
echo 'please provides your env for tencent cloud DOMAIN'
exit 1
fi

python tx-dns-update.py --access_key_id ${SECRETID} --access_key_secret ${SECRETKEY} --subdomain ${SUBDOMAIN} --domain ${DOMAIN}

