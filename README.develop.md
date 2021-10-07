
# The `develop` helper script

The script can build the image and push the code directly to a remote ucs-server.

## Prerequisites

1. An [AppCenter][1] app with a dummy-image

2. A UCS-Server

3. Configure simple, non-interactive ssh authentication
   i.e. with `ssh-copy-id`, `ssh-add` and `Host` in `~/.ssh/config`

4. Get the doveadm artifact

    1. Download from Gitlab with the helper-script
      ```
      export GLDL_CA_PATH=/etc/docker/certs.d/artifacts.knut.univention.de/CA.crt
      export GLDL_DL_PATH="python-doveadm.zip"
      export GLDL_PROJECT_ID='univention%2Fcustomers%2Fdataport%2Fupx%2Fpython-doveadm'
      export GLDL_TOKEN='<secret-gitlab-access-token>'
      python3 get-artifact.py
      ````

    2. Download from Gitlab with a Webbrowser
      Find the latest successful run off the main-branch, by clicking on [Pipelines][2].
      Then click on the three dots and select "Download artifacts" -> "build-job:archive"
      Rename "build-job-build-stage-main.zip" to "python-doveadm.zip" and
      move it to the root of this repo.

    3. Build and zip it yourself
      ```
      cd python-doveadm
      ./build-builder.sh
      ./build-deb.sh
      cd dist/deb_dist/
      zip python-doveadm.zip doveadm_*.* python3-doveadm_*_all.deb
      mv python-doveadm.zip ../../../dovecot-connector
      ```

## Configuration

- Copy the `develop.cfg.example` to `develop.cfg`.
- Set `ucs_host` in the file to the UCS-Server.
- Install the [sh][3] python module with a minimum version of `1.13`
  See `requirements.develop.txt`!
- Execute `./develop.py --help`.
  All parameters shown can also be configured in the config-file.

## Run

Open an ssh-root-shell to the ucs-server and execute
`tail --follow /var/log/univention/*.log /var/log/univention/listener_modules/*.log`.

Execute `./develop.py all` to deploy trigger and image.

[1]: https://provider-portal.software-univention.de/univention/management/#module=appcenter-selfservice::0:
[2]: https://git.knut.univention.de/univention/customers/dataport/upx/python-doveadm/-/pipelines?scope=branches&ref=main&status=success
[3]: https://pypi.org/project/sh/
