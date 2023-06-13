# dovecot-connector on SouvAP

This document extends the files already existing as `README.md` and
`README.develop.md` with some information learnt and needed for SouvAP
development and deployment.

### Provisioning

While the code under `app/listener_trigger` was developed with the AppCenter
provisioning in mind, SouvAP has no Univention AppCenter.

> AppCenter provisioning places files under `/var/lib/univention-appcenter/apps/dovecot-connector/data`
> such as creation, deletion and changes on LDAP objects. The AppCenter
> provisioning service then calls the `dovecot-connector` which runs on a
> container until it finishes processing the changes found on this directory.
> More info on this topic can be found [here](https://docs.software-univention.de/app-center/5.0/en/identity_management.html#provisioning)

> SouvAP, on the other hand has access to
> [Univention Directory Listener](https://docs.software-univention.de/developer-reference/5.0/en/listener/index.html)
> , which can be adapted to work with the base code of the `dovecot-connector`
and runs on a container continuously.


### Variables

In the file `.env.souvap.example` you will find some variables you can change.
* `DCC_ADM_URI`: `http://{dcc_adm_host}:{dcc_adm_port:d}/doveadm/v1` as template for the python connector.
* `DCC_ADM_HOST`: host where the doveadm HTTP API is hosted.
* `DCC_ADM_PORT`: port where the doveadm HTTP API is exposed.
* `DCC_ADM_USERNAME`: doveadm user, normally `doveadm` or specified under `doveam_username` at `dovecot.conf`.
* `DCC_ADM_PASSWORD`: doveadm password, usually under `doveadm_password` on the `dovecot.conf` file.
* `DCC_DC_VMAIL_TEMPLATE`: the path to the mail folders as a python template, like `/var/spool/dovecot/private/{domain}/{username}` with the following options available:
    * `domain`: the domain where the folders are located (email domain, like `example.org`)
    * `username`: the username at the domain (before the `@`)
    * `email`: the whole email, conformed by the user and the domain joined by the `@`
    * `uuid`: a unique id
    > This depends on how the dovecot server is configured, specially the auth part
    > (using LDAP, PAM or passwd-file as drivers on the passdb setting in `dovecot.conf`)
    > The home path for email is set under `mail_home` and `mail_location` also on that file.
    > Details [here](https://doc.dovecot.org/configuration_manual/mail_location/#mail-location-settings)
* `DCC_ADM_ACCEPTED_EXIT_CODES`: [dovecot specs](https://doc.dovecot.org/admin_manual/error_codes/)
* `DCC_LOGLEVEL`: DEBUG


### SouvAP development setup

1. Run the steps on `README.develop.md` to get the `python-doveadm.zip` package.
2. Run the steps on `README.md` on the [listener-container-base](https://git.knut.univention.de/univention/customers/dataport/upx/container-listener-base) and ensure `ssl`, `secret` and `docker-compose.override.yaml` have been created.
3. Configure additional domains if needed under the `docker-compose.override.yaml` to ensure doveadm HTTP API is reachable from within the container.
4. Happy development!

### Known issues

If dovecot is using the `user` part on `user@example.org` there seems to be
currently no way of removing its mailbox, unless the `user` is also the LDAP uid.

> Example: my user on ldap is `jnice` but my email id `john@example.org`, my
> mailbox could be located under `john` folder, thus not being deleted by
> any possible template on `DCC_DC_VMAIL_TEMPLATE` variables.

### Frequent issues

> Frequent in the sense of I found out the hard way 😃

##### doveadm is not running

Found when setting up a dovecot server.

1. Ensure it is not running on the port you expect it by `netstat -l --tcp -np | grep dovecot`
2. Visit the logs at `/var/log/dovecot.log` an check for messages by the doveadm service.
3. You probably have specified `doveadm_port` on your `dovecot.conf`, but that is not enough. Make sure something like this is on the `dovecot.conf`:
    ```
    service doveadm {{
    chroot =
    client_limit = 1
    drop_priv_before_exec = no
    executable = doveadm-server
    extra_groups = $default_internal_group
    group =
    idle_kill = 0
    privileged_group =
    process_limit = 0
    process_min_avail = 0
    protocol =
    service_count = 1
    type =
    unix_listener doveadm-server {{
    group =
    mode = 0600
    user =
    }}
    inet_listener {{
    port = 2425
    }}
    inet_listener http {{
    port = {doveadm_port:d}
    #ssl = yes # uncomment to enable https
    }}
    user =
    vsz_limit = 18446744073709551615 B
    }}
    ```
    > Double brackets are there for python templating. If you are not using the
    > configuration file as such template, please remove the duplicates.

##### python-doveadm not available

Due to the expiration time of artifacts on the python-doveadm repository,
the artifacts may have expired and the zip file containing the package may not
be downloaded.
1. Rerun the pipeline on python-doveadm repository.
2. Fix any failing tests if there are errors.

##### No connection from dovecot-connector container to doveadm HTTP API

1. Make sure you have a `docker-compose.override.yaml` file on the root folder. Else, you can find more details on how to get it on the [listener-container-base repo](https://git.knut.univention.de/univention/customers/dataport/upx/container-listener-base) and its playbooks.

> For this case, you may try the following command:
```
curl -u doveadm:<some_pass> http://domain.example.org:8080/doveadm/v1
```
or try out a full command for more specific cases
```
curl -u doveadm:<some_pass> http://domain.example.org:8080/doveadm/v1 -X POST -H "Content-Type: application/json" -d '[["fsDelete",{"recursive":true,"maxParallel":1,"fsDriver":"posix","fsArgs":"dirs","path":"/var/spool/dovecot/private/<some_domain>/<some_user>"},"tag1"]]'
```
