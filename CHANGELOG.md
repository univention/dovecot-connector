# Changelog

## [1.1.0](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/compare/v1.0.2...v1.1.0) (2023-11-29)


### Features

* add TLS_MODE variable ([44520cf](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/44520cf62b6b2ea0f66484bfd59d5694aed2fc08)), closes [univention/customers/dataport/team-souvap#91](https://git.knut.univention.de/univention/customers/dataport/team-souvap/issues/91)
* **base:** souvap based on univention directory listener base image ([2cf2cfe](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/2cf2cfececedfe4f066d17594c0c18a8ef6ebdb2))
* **compose:** move dotenv variables to compose-file ([7e414bc](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/7e414bccd9ba9831952c0f7e52b2ae67e6587a5b)), closes [univention/customers/dataport/team-souvap#91](https://git.knut.univention.de/univention/customers/dataport/team-souvap/issues/91)
* **docs:** added documentation for souvap development ([fb75831](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/fb758316b5ca3ce783a7587f5d08013d14a679e5))
* **helm:** don't set examples as defaults ([5412e62](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/5412e62ed5cb0534d09636297161a53626902242)), closes [univention/open-xchange/provisioning#22](https://git.knut.univention.de/univention/open-xchange/provisioning/issues/22)
* **helm:** enable probes by default ([b725a55](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/b725a5502f51a80fcf8081c08786833804188320)), closes [univention/open-xchange/provisioning#22](https://git.knut.univention.de/univention/open-xchange/provisioning/issues/22)
* **helm:** helm charts ([fda4dcb](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/fda4dcbbe9cecd80e1e2953bfab8a84fcbde4834))
* **images:** migrate dovecot-connector appcenter and opendesk images to ucs-base ([dcde85f](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/dcde85f2cb97bcdb0a37789ee0ed7f5a79c2f3b6))


### Bug Fixes

* **ci:** set common-ci version to v1.9.7 ([ceef023](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/ceef0230bdebd4b307a2fe234e5181039186b4ad))
* **ci:** use souvap common-ci and push to souvap registry ([7ddc87d](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/7ddc87dfc440c434659ce08f980e1002db7499e1))
* **env:** syntax error ([60dce09](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/60dce092aaafffe55c4fdf5cd0c6bdaf38b57dd1))
* **helm:** only quote once ([7b5a794](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/7b5a7943731b687115cee9b893058aec907e6efb))
* **listener:** fix typo in dcc_adm_accepted_exit_codes ([b477bf8](https://git.knut.univention.de/univention/customers/dataport/upx/dovecot-connector/commit/b477bf8bc9d3108a63004da98e54d9317ac0802a))
