# dovecot-connector

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.0.2](https://img.shields.io/badge/AppVersion-1.0.2-informational?style=flat-square)

A Helm chart for the dovecot-connector

**Homepage:** <https://www.univention.de/>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://gitregistry.knut.univention.de/univention/customers/dataport/upx/common-helm/helm | common | ^0.1.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| dovecotConnector.authLdapSecret | string | `""` | LDAP access password, base64 encoded. See /etc/ldap.secret on your UCS machine. |
| dovecotConnector.caCert | string | `""` | CA certificate of UCS machine, base64 encoded. |
| dovecotConnector.caCertFile | string | `"/run/secrets/ca_cert"` |  |
| dovecotConnector.certPem | string | `""` | Certificate of the ucs machine, base64 encoded. |
| dovecotConnector.certPemFile | string | `"/run/secrets/cert_pem"` |  |
| dovecotConnector.dccAdmAcceptedExitCodes | string | `"0 2 68 75"` | [dovecot specs](https://doc.dovecot.org/admin_manual/error_codes/) |
| dovecotConnector.dccAdmHost | string | `"dovecot.example.org"` | Host where the doveadm HTTP API is hosted. |
| dovecotConnector.dccAdmPassword | string | `"somepassword"` | doveadm password, usually under `doveadm_password` on the `dovecot.conf` file. |
| dovecotConnector.dccAdmPort | string | `"80"` | Host where the doveadm HTTP API is exposed. |
| dovecotConnector.dccAdmUri | string | `"http://{dcc_adm_host}:{dcc_adm_port}/doveadm/v1"` | Template for the python dovecot-connector script. |
| dovecotConnector.dccAdmUsername | string | `"doveadm"` | doveadm user, normally `doveadm` or specified under `doveadm_username` at `dovecont.conf`. |
| dovecotConnector.dccDcVmailTemplate | string | `"/var/spool/dovecot/private/{domain}/{username}"` | doveadm password, usually under `doveadm_password` on the `dovecot.conf` file, with options `domain`, `username`, `email`, `uuid`. |
| dovecotConnector.dccLoglevel | string | `"DEBUG"` | Log level |
| dovecotConnector.debugLevel | string | `"5"` |  |
| dovecotConnector.domainName | string | `"example.org"` |  |
| dovecotConnector.ldapBaseDn | string | `"dc=example,dc=org"` |  |
| dovecotConnector.ldapBindSecret | string | `"/run/secrets/ldap_secret"` |  |
| dovecotConnector.ldapHost | string | `"domain.example.org"` |  |
| dovecotConnector.ldapHostDn | string | `"cn=domain,cn=dc,cn=computers,dc=example,dc=org"` |  |
| dovecotConnector.ldapHostIp | string | `""` | Will add a mapping from "ldapHost" to "ldapHostIp" into "/etc/hosts" if set |
| dovecotConnector.ldapPort | string | `"389"` |  |
| dovecotConnector.notifierServer | string | `"domain.example.org"` | Defaults to "ldap_host" if not set. |
| environment | object | `{}` |  |
| fullnameOverride | string | `""` |  |
| image.imagePullPolicy | string | `"Always"` |  |
| image.registry | string | `"registry.souvap-univention.de"` |  |
| image.repository | string | `"souvap/tooling/images/dovecot-connector"` |  |
| image.tag | string | `"1.0.2"` |  |
| ingress | object | `{"enabled":false}` | Kubernetes ingress |
| ingress.enabled | bool | `false` | Set this to `true` in order to enable the installation on Ingress related objects. |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| probes.liveness.enabled | bool | `false` |  |
| probes.readiness.enabled | bool | `false` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `""` |  |
| tolerations | list | `[]` |  |
