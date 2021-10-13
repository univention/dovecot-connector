# dovecot-connector

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


### Check and debug

* Check installation: `univention-app info` and `univention-app list dovecot-connector`

* Check if the trigger gets updates from user and group changes: `univention-app get dovecot-connector ListenerUDMModules`

* Find the trigger scripts: `ls /var/cache/univention-appcenter/*/*/dovecot-connector_*.listener_trigger`
  (The script has to be changed in the [Provider Portal](https://provider-portal.software-univention.de/univention/management/#module=appcenter-selfservice::0:). It is not in the Docker container)

* Get a shell in the currently assigned Docker container: `univention-app shell dovecot-connector`

* Use a different container: `univention-app dev-set dovecot-connector DockerImage=docker.software-univention.de/dovecot-connector:dev`
  Verify the value with: `univention-app get dovecot-connector DockerImage`


### Use custom image

- The app is already installed.
- Build or load a new container.
- Reference it like `univention-app dev-set dovecot-connector DockerImage=dovecot-connector:test`
- Reinstall the app without the image: `univention-app install dovecot-connector --do-not-pull-image --password univention`


### Mount custom paths to the container

`univention-app dev-set dovecot-connector DockerVolumes=/host-path:/in-container-path,/test:/test`
