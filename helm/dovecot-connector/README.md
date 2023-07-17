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
| dovecotConnector.caCert | string | `nil` | CA root certificate. Optional; will be written to "caCertFile" if set. |
| dovecotConnector.caCertFile | string | `"/run/secrets/ca_cert"` | The path to the "caCertFile" docker secret or a plain file. |
| dovecotConnector.dccAdmAcceptedExitCodes | string | `"0 2 68 75"` | DoveAdm exit codes which will be considered as successful [dovecot specs](https://doc.dovecot.org/admin_manual/error_codes/) |
| dovecotConnector.dccAdmHost | string | `nil` | Host where the doveadm HTTP API is hosted. |
| dovecotConnector.dccAdmPassword | string | `nil` | doveadm password, usually under `doveadm_password` on the `dovecot.conf` file. |
| dovecotConnector.dccAdmPort | string | `"80"` | Host where the doveadm HTTP API is exposed. |
| dovecotConnector.dccAdmUri | string | `"http://{dcc_adm_host}:{dcc_adm_port}/doveadm/v1"` | Template for the python dovecot-connector script. |
| dovecotConnector.dccAdmUsername | string | `nil` | doveadm user, normally `doveadm` or specified under `doveadm_username` at `dovecont.conf`. |
| dovecotConnector.dccDcVmailTemplate | string | `"/var/spool/dovecot/private/{domain}/{username}"` | doveadm password, usually under `doveadm_password` on the `dovecot.conf` file, with options `domain`, `username`, `email`, `uuid`. |
| dovecotConnector.dccLoglevel | string | `"INFO"` | Log level |
| dovecotConnector.debugLevel | int | `3` | UDL-Debug level (1-5) |
| dovecotConnector.ldapBaseDn | string | `nil` | LDAP Base Distinguished Name |
| dovecotConnector.ldapHost | string | `nil` | LDAP Server Domain Name |
| dovecotConnector.ldapHostDn | string | `nil` | LDAP Host Distinguished Name |
| dovecotConnector.ldapHostIp | string | `nil` | Will add a mapping from "ldapHost" to "ldapHostIp" into "/etc/hosts" if set |
| dovecotConnector.ldapPassword | string | `nil` | LDAP password for `cn=admin`. Will be written to "ldapPasswordFile" if set. |
| dovecotConnector.ldapPasswordFile | string | `"/run/secrets/ldap_secret"` | The path to the "ldapPasswordFile" docker secret or a plain file |
| dovecotConnector.ldapPort | int | `389` | LDAP Server Port |
| dovecotConnector.notifierServer | string | `nil` | Defaults to "ldapHost" if not set. |
| dovecotConnector.tlsMode | string | `"secure"` | Whenever to start encryption and validate certificates. Chose from "off", "unvalidated" and "secure". |
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
| probes.liveness.enabled | bool | `true` |  |
| probes.liveness.failureThreshold | int | `3` |  |
| probes.liveness.initialDelaySeconds | int | `120` |  |
| probes.liveness.periodSeconds | int | `30` |  |
| probes.liveness.successThreshold | int | `1` |  |
| probes.liveness.timeoutSeconds | int | `3` |  |
| probes.readiness.enabled | bool | `true` |  |
| probes.readiness.failureThreshold | int | `30` |  |
| probes.readiness.initialDelaySeconds | int | `30` |  |
| probes.readiness.periodSeconds | int | `15` |  |
| probes.readiness.successThreshold | int | `1` |  |
| probes.readiness.timeoutSeconds | int | `3` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `""` |  |
| tolerations | list | `[]` |  |
