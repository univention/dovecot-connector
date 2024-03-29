# dovecot-connector (DCC)

## Installation

Install DCC using the following commandline
```
univention-app install dovecot-connector \
   --set DCC_ADM_PASSWORD='<password_for_doveadm>' \
         DCC_ADM_HOST=<hostname_for_doveadm_http_endpoint> \
         DCC_ADM_PORT=<port_for_doveadm_http_endpoint> \
         DCC_DC_VMAIL_TEMPLATE='/data/usr/local/dovecot/vmail/{domain}/{uuid}'
```

The following settings usually can stay with their default values:
```
DCC_ADM_URI='https://{dcc_adm_host}:{dcc_adm_port:d}/doveadm/v1'
DCC_ADM_USERNAME='doveadm'
DCC_ADM_ACCEPTED_EXIT_CODES='68 75'
```

### Placeholders

#### DCC_DC_VMAIL_TEMPLATE

Within the path definition you can make use of the following placeholders that are filled with the respective values based on the object that is being processed:

- {uuid}: entryUUID
- {email}: the mailPrimaryAddress
- {domain}: domain part (everything after the `@`-sign) from mailPrimaryAddress
- {username}: username

If required you can make use of single characters out of the above placeholders by addressing them explicitly, that especially makes sense when it comes to mail directories that need to be distributed on the storage, so you may want to use a setup similar to the following example also in order to get rid of the dependency to the maildomain in the file-system:
```
DCC_DC_VMAIL_TEMPLATE='/data/usr/local/dovecot/vmail/{uuid[0]}{uuid[1]}/{uuid}'
```

#### DCC_ADM_URI

Placeholders are also available for `DCC_ADM_URL` but are currently restricted referencing the values of `dcc_adm_host` and `dcc_adm_port`.

### Multiple Hosts

`DCC_ADM_HOST` supports multiple, comma or space separated hostnames, e.g. `endpoint.myhost.tld,alsoendpoint.myhost2.tld`

If multiple hostnames are given the request will be executed sequentially against all hosts based on the `DCC_ADM_URI`, so it will make use of the same path (e.g. `/doveadm/v1`), port (from `DCC_ADM_PORT`) and doveadm credentials.

## Operations / Troubleshooting

* Logfile is written to `/var/log/univention/listener_modules/dovecot-connector.log`

* Check installation:
  * `univention-app info`
  * `univention-app list dovecot-connector`
  * `univention-app configure dovecot-connector --list`

* Check if the trigger gets updates from user and group changes: `univention-app get dovecot-connector ListenerUDMModules`

* Find the trigger scripts: `ls /var/cache/univention-appcenter/*/*/dovecot-connector_*.listener_trigger`
  (The script has to be changed in the [Provider Portal](https://provider-portal.software-univention.de/univention/management/#module=appcenter-selfservice::0:). It is not in the Docker container)

* Get a shell in the currently assigned Docker container: `univention-app shell dovecot-connector`

* Use a different container: `univention-app dev-set dovecot-connector DockerImage=docker.software-univention.de/dovecot-connector:dev`
  Verify the value with: `univention-app get dovecot-connector DockerImage`


## Development

Please download this repo with `git clone --recursive ...`.
If you already cloned it before, add the submodule with `git submodule update --init`.
Now make sure to get all updates with `git pull --recurse-submodules`.


### Prepare the UCS server

Install an UCS 5.x server.
I.e. by downloading an image from [univention.de/download](https://www.univention.de/download/download-ucs/)

Finish the server configuration and
copy the `ucs.license` file from the registration mail to the server.
Install it with `univention-license-import ucs.license`.

Install the development appcenter: `apt-get install univention-appcenter-dev`.

Configure the appcenter to run in develpment mode: `univention-app dev-use-test-appcenter`

Install the app: `univention-app install dovecot-connector --noninteractive --password univention`


### Use custom image

- The app is already installed.
- Build or load a new container.
- Reference it like `univention-app dev-set dovecot-connector DockerImage=dovecot-connector:test`
- Reinstall the app without the image: `univention-app install dovecot-connector --do-not-pull-image --password univention`


### Mount custom paths to the container

`univention-app dev-set dovecot-connector DockerVolumes=/host-path:/in-container-path,/test:/test`


## SouvAP

In this repository you can also find an image on `Dockerfile.souvap` which
consists of the same code shipped on Univention AppCenter with some glue code
to make it work with [Univention Directory Listener](https://docs.software-univention.de/developer-reference/5.0/en/listener/index.html),since [AppCenter provisioning](https://docs.software-univention.de/app-center/5.0/en/identity_management.html#provisioning)
is not available in the SouvAP environment.

### Development setup

Please look into the [base container image](https://git.knut.univention.de/univention/customers/dataport/upx/container-listener-base#preparation)
on which Univention Directory Listener is installed. An ansible playbook is
provided there to ease the development setup.

> Note a `docker-compose.override.yaml` will be created, as well as a `secret`
and a `ssl` folder. All of them are needed for development on this repository.
