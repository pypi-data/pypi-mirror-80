from base64 import b64encode, b64decode
from glob import glob
import os
import socket
import sys
from raft import task
import yaml
from boto3 import Session
from sewer.client import Client
from sewer.dns_providers.route53 import Route53Dns


def new_cert(hostname, alt_domains, email=None, profile=None):
    """
    :param str hostname:
        the fqdn of the local host for which we are creating the cert

    :param str alt_domains:
        a comma-separated list of alternative domains to also
        requests certs for.

    :param str email:
        the email of the contact on the cert

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials
    """
    if profile:
        os.environ['AWS_PROFILE'] = profile
    alt_domains = alt_domains.split(',') if alt_domains else []
    client = Client(
        hostname, domain_alt_names=alt_domains, contact_email=email,
        provider=Route53Dns(), ACME_AUTH_STATUS_WAIT_PERIOD=60,
        ACME_AUTH_STATUS_MAX_CHECKS=15, ACME_REQUEST_TIMEOUT=60)
    certificate = client.cert()
    account_key = client.account_key
    key = client.certificate_key
    return certificate, account_key, key


def get_certificate(ns, hostname, profile=None):
    if not ns.startswith('/'):
        ns = f'/{ns}'
    hostname = hostname.replace('*', 'star')
    try:
        session = Session(profile_name=profile)
        ssm = session.client('ssm')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'account_key' ])
        response = ssm.get_parameter(Name=name)
        account_key = response['Parameter']['Value']
        print('account key retrieved')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'key' ])
        response = ssm.get_parameter(Name=name, WithDecryption=True)
        key = response['Parameter']['Value']
        print('private key retrieved')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'cert' ])
        response = ssm.get_parameter(Name=name)
        certificate = response['Parameter']['Value']
        print('public cert retrieved')
    except:  # noqa: E722, pylint: disable=bare-except
        account_key = None
        key = None
        certificate = None
    return certificate, account_key, key


def get_pfx(ns, hostname, profile=None):
    if not ns.startswith('/'):
        ns = f'/{ns}'
    hostname = hostname.replace('*', 'star')
    try:
        session = Session(profile_name=profile)
        ssm = session.client('ssm')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'pfx' ])
        rg = []
        for n in range(1, 10):
            try:
                st = f'{name}{n}'
                print(f'[pfx]  getting {st}')
                response = ssm.get_parameter(Name=st, WithDecryption=True)
                rg.append(response['Parameter']['Value'])
            except:  # noqa: E722, pylint: disable=bare-except
                break
        pfx_data = ''.join(rg)
        pfx_data = b64decode(pfx_data.encode('utf-8'))
        print(f'[pfx]  decoded {len(pfx_data)} bytes')
    except:  # noqa: E722, pylint: disable=bare-except
        pfx_data = None
    return pfx_data


def renew_cert(
        ns, hostname, alt_domains=None,
        email=None, profile=None, **kwargs):
    if profile:
        os.environ['AWS_PROFILE'] = profile
    alt_domains = alt_domains.split(',') if alt_domains else []
    _, account_key, key = get_certificate(ns, hostname, profile)
    client = Client(
        hostname, domain_alt_names=alt_domains, contact_email=email,
        provider=Route53Dns(), account_key=account_key,
        certificate_key=key, ACME_AUTH_STATUS_WAIT_PERIOD=60,
        ACME_AUTH_STATUS_MAX_CHECKS=15, ACME_REQUEST_TIMEOUT=60)
    certificate = client.renew()
    account_key = client.account_key
    key = client.certificate_key
    return certificate, account_key, key


def pfx(ctx, certificate, key):
    f1, f2, f3 = '/tmp/p1.cert', '/tmp/p1.crt', '/tmp/p1.pfx'
    with open(f1, 'w') as f:
        f.write(certificate)
    with open(f2, 'w') as f:
        f.write(key)
    os.chmod(f1, 0o644)
    os.chmod(f2, 0o600)
    ctx.run(
        f'/usr/bin/openssl pkcs12 -export -in {f1} -inkey {f2}'
        f' -out {f3} -passout pass:')
    with open(f3, 'rb') as f:
        data = f.read()
    data = b64encode(data).decode('utf-8')
    rg = []
    while data:
        rg.append(data[:4096])
        data = data[4096:]
    os.remove(f1)
    os.remove(f2)
    os.remove(f3)
    return rg


@task
def renew_all(ctx, dir_name=None, profile=None):
    """
    Requests a letsencrypt cert using route53 and sewer, also requests
    wildcard certs based on the provided hostname

    :param raft.context.Context ctx:
        the raft-provided context

    :param str dir_name:
        the config directory

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials

    """
    default_filename = os.path.join(dir_name, 'defaults.yml')
    defaults = {}
    if os.path.exists(default_filename):
        with open(default_filename, 'r') as f:
            defaults = yaml.load(f, Loader=yaml.SafeLoader)
    defaults = defaults or {}
    dir_name = os.path.join(dir_name, '*.yml')
    files = glob(dir_name)
    for filename in files:
        if filename.endswith('defaults.yml'):
            continue
        request_cert(ctx, filename, profile, defaults)


def request_cert(ctx, filename, profile, defaults):
    print(f'processing {filename}')
    with open(filename, 'r') as f:
        values = yaml.load(f, Loader=yaml.SafeLoader)
    for key, value in defaults.items():
        values.setdefault(key, value)
    namespaces = values.pop('namespaces', [])
    profile = profile or values.pop('profile', None)
    ns = namespaces[0]
    certificate, account_key, key = renew_cert(
        **values, ns=ns, profile=profile)
    for x in namespaces:
        save_cert(ctx, x, values['hostname'], certificate, account_key, key)


@task
def request(ctx, filename=None, profile=None):
    """
    Requests a letsencrypt cert using route53 and sewer, also requests
    wildcard certs based on the provided hostname

    :param raft.context.Context ctx:
        the raft-provided context

    :param str filename:
        the config file

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials

    """
    default_filename = os.path.join(os.path.dirname(filename), 'defaults.yml')
    defaults = {}
    if os.path.exists(default_filename):
        with open(default_filename, 'r') as f:
            defaults = yaml.load(f, Loader=yaml.SafeLoader)
    defaults = defaults or {}
    request_cert(ctx, filename, profile, defaults)


def save_cert(ctx, ns, hostname, certificate, account_key, key, profile=None):
    session = Session(profile_name=profile)
    ssm = session.client('ssm')
    pfx_data = pfx(ctx, certificate, key)
    hostname = hostname.replace('*', 'star')
    prefix = ns
    if not prefix.startswith('/'):
        prefix = f'/{prefix}'
    prefix = os.path.join(prefix, 'apps_keystore', hostname)
    name = os.path.join(prefix, 'account_key')
    print(f'saving {name}')
    ssm.put_parameter(
        Name=name,
        Description='sewer / certbot account key',
        Value=account_key,
        Overwrite=True,
        Type='String')
    name = os.path.join(prefix, 'cert')
    print(f'saving {name}')
    ssm.put_parameter(
        Name=name,
        Description='sewer / certbot certificate',
        Overwrite=True,
        Value=certificate,
        Type='String')
    name = os.path.join(prefix, 'key')
    print(f'saving {name}')
    ssm.put_parameter(
        Name=name,
        Description='sewer / certbot private key',
        Value=key,
        Overwrite=True,
        Type='SecureString',
        KeyId=f'alias/{ns}')
    name = os.path.join(prefix, 'pfx')
    for n, x in enumerate(pfx_data, 1):
        st = f'{name}{n}'
        print(f'saving {st}')
        ssm.put_parameter(
            Name=st,
            Description='sewer / certbot pfx',
            Value=x,
            Overwrite=True,
            Type='SecureString',
            KeyId=f'alias/{ns}')


@task
def install_cert(ctx, config, hostname=None):
    """
    installs a cert on the local system:

        on linux to /etc/ssl/certs
        on windows to cert:/localmachine/my
    """
    with open(config, 'r') as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
    ns = conf['namespace']
    profile = conf.get('profile')
    owner = conf.get('owner', 'root')
    group = conf.get('group', owner)
    cert_filename = conf.get('certificate')
    key_filename = conf.get('key')
    hostname = hostname or conf.get('hostname')
    if not hostname:
        hostname = get_hostname(ctx)
    if is_linux():
        install_cert_on_linux(
            ctx, ns, hostname, profile,
            cert_filename, key_filename, owner, group)
    elif is_windows():
        install_cert_on_windows(
            ctx, ns, hostname, profile)


def get_hostname(ctx):
    if is_linux():
        result = ctx.run('/bin/hostname')
        return result.stdout.strip()
    if is_windows():
        result = socket.getfqdn()
        return result
    return None


def install_cert_on_linux(
        ctx, ns, hostname, profile, cert_filename, key_filename,
        owner, group):
    certificate, _, key = get_certificate(ns, hostname, profile)
    if not cert_filename:
        st = f'{hostname}.bundled.crt'
        cert_filename = os.path.join('/etc/ssl/certs', st)
    if not key_filename:
        key_filename = os.path.join('/etc/ssl/private', f'{hostname}.key')
    with open(cert_filename, 'w') as f:
        f.write(certificate)
    ctx.run(f'chmod 0644 {cert_filename}')
    ctx.run(f'chown {owner}:{group} {cert_filename}')
    with open(key_filename, 'w') as f:
        f.write(key)
    ctx.run(f'chmod 0600 {key_filename}')
    ctx.run(f'chown {owner}:{group} {key_filename}')


@task
def install_cert_on_windows(ctx, ns, hostname, profile):
    """
    not yet implemented -- have to find a good, cost-effective way
    to generate the pfx file and store to ssm
    """
    pfx_data = get_pfx(ns, hostname, profile)
    c = 'powershell.exe -command "[System.IO.Path]::GetTempFileName()"'
    result = ctx.run(c)
    filename = result.stdout.strip()
    with open(filename, 'wb') as f:
        f.write(pfx_data)
    c = (
        'powershell.exe -command "'
        'Import-PfxCertificate '
        r'  -CertStoreLocation cert:\localmachine\my'
        f' -filepath {filename}'
        f'"'
    )
    ctx.run(c)
    os.remove(filename)


def is_linux():
    return sys.platform == 'linux'


def is_windows():
    return sys.platform == 'win32'
