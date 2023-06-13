# dovecot-connector

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.0.2](https://img.shields.io/badge/AppVersion-1.0.2-informational?style=flat-square)

A Helm chart for the dovecot-connector

**Homepage:** <https://www.univention.de/>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://charts.bitnami.com/bitnami | common | ^2.2.2 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| dovecot_connector.authLdapSecret | string | `""` | LDAP access password, base64 encoded. See /etc/ldap.secret on your UCS machine. |
| dovecot_connector.caCert | string | `""` | CA certificate of UCS machine, base64 encoded. |
| dovecot_connector.caCertFile | string | `"/run/secrets/ca_cert"` |  |
| dovecot_connector.certPem | string | `""` | Certificate of the ucs machine, base64 encoded. |
| dovecot_connector.certPemFile | string | `"/run/secrets/cert_pem"` |  |
| dovecot_connector.dccAdmAcceptedExitCodes | string | `"0 2 68 75"` | [dovecot specs](https://doc.dovecot.org/admin_manual/error_codes/) |
| dovecot_connector.dccAdmHost | string | `"dovecot.example.org"` | Host where the doveadm HTTP API is hosted. |
| dovecot_connector.dccAdmPassword | string | `"somepassword"` | doveadm password, usually under `doveadm_password` on the `dovecot.conf` file. |
| dovecot_connector.dccAdmPort | string | `"80"` | Host where the doveadm HTTP API is exposed. |
| dovecot_connector.dccAdmUri | string | `"http://{dcc_adm_host}:{dcc_adm_port}/doveadm/v1"` | Template for the python dovecot-connector script. |
| dovecot_connector.dccAdmUsername | string | `"doveadm"` | doveadm user, normally `doveadm` or specified under `doveadm_username` at `dovecont.conf`. |
| dovecot_connector.dccDcVmailTemplate | string | `"/var/spool/dovecot/private/{domain}/{username}"` | doveadm password, usually under `doveadm_password` on the `dovecot.conf` file, with options `domain`, `username`, `email`, `uuid`. |
| dovecot_connector.dccLoglevel | string | `"DEBUG"` | Log level |
| dovecot_connector.debugLevel | string | `"5"` |  |
| dovecot_connector.domainName | string | `"example.org"` |  |
| dovecot_connector.ldapBaseDn | string | `"dc=example,dc=org"` |  |
| dovecot_connector.ldapBindSecret | string | `"/run/secrets/ldap_secret"` |  |
| dovecot_connector.ldapHost | string | `"domain.example.org"` |  |
| dovecot_connector.ldapHostDn | string | `"cn=domain,cn=dc,cn=computers,dc=example,dc=org"` |  |
| dovecot_connector.ldapHostIp | string | `""` | Will add a mapping from "ldap_host" to "ldap_host_ip" into "/etc/hosts" if set |
| dovecot_connector.ldapPort | string | `"389"` |  |
| dovecot_connector.notifierServer | string | `"domain.example.org"` | Defaults to "ldap_host" if not set. |
| environment | object | `{}` |  |
| fullnameOverride | string | `""` |  |
| image.imagePullPolicy | string | `"Always"` |  |
| image.registry | string | `"registry.souvap-univention.de"` |  |
| image.repository | string | `"souvap/tooling/images/dovecot-connector"` |  |
| image.tag | string | `"standalone-1.0.2"` |  |
| ingress | object | `{"enabled":false}` | Kubernetes ingress |
| ingress.enabled | bool | `false` | Set this to `true` in order to enable the installation on Ingress related objects. |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| probes.liveness.enabled | bool | `false` |  |
| probes.readiness.enabled | bool | `false` |  |
| replicaCount | int | `1` |  |
| resources.limits.cpu | string | `"4"` |  |
| resources.limits.memory | string | `"4Gi"` |  |
| resources.requests.cpu | string | `"250m"` |  |
| resources.requests.memory | string | `"512Mi"` |  |
| securityContext | object | `{}` |  |
| service.enabled | bool | `false` |  |
| tolerations | list | `[]` |  |
