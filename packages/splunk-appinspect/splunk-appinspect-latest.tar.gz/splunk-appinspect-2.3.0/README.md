# Splunk AppInspect
![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)
## Overview

AppInspect is a tool for assessing a Splunk App's compliance with Splunk recommended development practices, by using static analysis. AppInspect is open for extension, allowing other teams to compose checks that meet their domain specific needs for semi- or fully-automated analysis and validation of Splunk Apps.

## Documentation

You can find the documentation for Splunk AppInspect at http://dev.splunk.com/goto/appinspectdocs.

## Builds

| Branch     | Status    |
| --------|---------|
| master  | [status](https://jenkins.splunkdev.com/view/AppInspect/job/AppInspect%20CLI/job/master/)|
| development | [status](https://jenkins.splunkdev.com/view/AppInspect/job/AppInspect%20CLI/job/development/)|
|feature/py3_readiness_app_compatible| [status](https://jenkins.splunkdev.com/view/AppInspect/job/AppInspect%20CLI/job/feature%252Fpy3_readiness_app_compatible/)|
## Local Development

Use the following steps to setup AppInspect for local development.
### Install from source
* Checkout the `development` branch
* Create and activate a [virtual env](http://docs.python-guide.org/en/latest/dev/virtualenvs)
* Build and install from source
	- install libmagic (`brew install libmagic` on macOS)
	- `pip install -r (windows|darwin|linux).txt`, it depends on your system platform
	- `make gen_trusted_libs` generate local trusted libs for python check
	- `python setup.py install`, if you see any error like `ValueError: bad marshal data`, try run `find ./ -name '*.pyc' -delete` first.  
	**Caution**: Do not delete the pyc file below which is used for tests.  
	 `test/unit/packages/has_disallowed_file_extensions/has_pyc_file/configuration_parser.pyc`
	- That's it. The `splunk-appinspect` tool is installed into your virtualenv. You can verify this by running the following commands:
   		- `splunk-appinspect`
    	- `splunk-appinspect list version`

### Run CLI directly from codebase
* Install all dependencies, `pip install -r (windows|darwin|linux).txt`, it depends on your system platform
* Add current folder into PYTHONPATH, `export PYTHONPATH=$PYTHONPATH:.`
* Run the CLI, `scripts/splunk-appinspect list version`

### Build the distribution package
* Create a distribution of AppInspect
    - `make gen_trusted_libs` generate local trusted libs for python check
    - `python setup.py sdist`
    - after running the above command, an installation package with name like `splunk-appinspect-<version>.tar.gz` is created under the `dist` folder
* Install the distro previously created
    - `pip install dist/splunk-appinspect-<version>.tar.gz`


### Run tests
Once you have the `splunk-appinspect` tool installed, you can run tests by following the steps below.

* Install the Unit & Integration Test Requirements
    - `pip install -r test/(windows|darwin|linux).txt`, it depends on your system platform
* Ensure the Unit tests pass
    - `pytest -v test/unit/`
* Ensure the Integration tests pass
    - Integration tests uses a library called `boto3` to download packages from AWS S3 for testing
        - Export `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables, you can find the credentials in secret.splunk.com
	- `pytest -v test/integration/test_cli.py`
	- network access is needed because some testing apps will be downloaded online, and this may take some time
	- `splunk-appinspect` CLI is needed in `PATH` so that integration tests can be run correctly

### Speed up integration test
* When running integration tests, boto3 library will automatically download testing app packages from S3,
which could be very slow depending on the network. If you download all the packages once,
you can set environment variable `APPINSPECT_DOWNLOAD_TEST_DATA` to `false` to avoid downloading them every time. For example:
`APPINSPECT_DOWNLOAD_TEST_DATA=false pytest -v --junitxml=test_cli_results.xml ./test/integration -k test_splunk_appinspect_list_works_with_included_and_excluded_tags_filter`   

### Speed up single unit test in a test scenario
Running single test case is time consuming since pytest will collect all tests even if you only plan to run single test case, which is too slow for fast feedback development cycle.
To make it faster, when you run pytest, either in CLI or IDE, you can specify the test scenario name prefix using an env var called `APPINSPECT_TEST`, so that only this test scenario csv will be handled and this makes running single test faster. For example, you can try:
```
APPINSPECT_TEST=test_check_server_configuration_file python -m pytest -v ./test/unit -k check_server_conf
```
You can use the `APPINSPECT_TEST` to fasten test scenario collection and use -k to focus on a specific check in the test scenario.

### Install without building
* Install the latest AppInspect CLI from the development branch.
    - `wget -r -l1 --no-parent --no-directories -A 'splunk-appinspect-*.tar.gz' https://repo.splunk.com/artifactory/Solutions/AppInspect/CLI/develop/builds/latest/ && pip install splunk-appinspect-*.tar.gz`

### `VERSION.txt` naming convention
Each update in `VERSION.txt` should correspond to a package release:

1. If we aim for a major release, we should name the version referring [semver](https://semver.org/) as is, example: `1.6.0`.
2. If we aim for a hotfix release, we should append hotfix version to current version(`${appinspect version}.post${hotfix version}`), example: `1.6.0.post1`.
    - Note: if there is a second hotfix after the first hotfix release finished, the version should be **manually** updated to `1.6.0.post2`, and so on.

## Release strategy
Referring [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow),
now the release strategy of appinspect can be descripted as following:
1. All `feature/` and `bugfix/` branches should be checked out from `development` branch, and merged back to `development` branch.
2. All `hotfix/` branches should be checked out directly from `master` branch, and merged back to `master` and `development` branch.
    - Notes:
        - Each PR from `hotfix/` to `master` branch should contain a updated version, reflected in `VERSION.txt`, as mentioned in naming convention.
3. Once `development` branch has acquired enough features for a release, a `release/` branch should be checked out from `development` branch, implying that we have entered the `release candidate` phase.
    - Notes:
        - Bugfix in `release candidate` phase should be merged to `/release` branch.
        - During the `release candidate` stage,
            we should raise a PR from `release/` to `development` branch **RIGHT AFTER EACH** merge from `bugfix/` to `release/` branch finished,
            and if code conflict exist in the PR from `release/` to `development` branch,
            we should checkout another branch from `release/` to resolve the conflict.
            That's to ensure there would be no code conflict when we merge `release/`  back to `development` branch after the master release ended, which may cause some confusion.
        - Each `release/` branch should be merged back into `development` branch **after** `master` release, since it may have separately progressed from `development` branch since the release was initiated.
4. Jenkins builds for all `feature/` and `bugfix/` branches will generate a stub package naming `splunk-appinspect-1.0.1.prtest.tar.gz` as well, it's just for checking whether the _publish stage_ in Jenkins build can be finished successfully.

## Release version convention

|Branch name | Generate built package | Release to outside world | Package filename example| `requirements.txt` entry example | Notes |
|:---:|:---:|:---:|:---:|:---:|:---:|
| `development` | No | / |   /  | / | only accept PR from `feature/` and normal `bugfix/` branches|
| `master`(normal) |  Yes | Yes | `splunk-appinspect-1.6.0.tar.gz` | `splunk-appinspect==1.6.0` | only accept PR from `release/` branches |
| `master`(hotfix) | Yes | Yes | `splunk-appinspect-1.6.0.post1.tar.gz` | `splunk-appinspect==1.6.0.post1` | only accept PR from `hotfix/` branches |
| `release/{version_number}` | Yes | No | `splunk-appinspect-1.6.0rc2+4ae00b.tar.gz` | `splunk-appinspect==1.6.0rc2+4ae00b` | only for e2e test in `release-candidate` phase |

* To guarantee the PRs' quality, please execute the following steps for once:
    - `chmod +x ./scripts/hooks/install-hooks.sh ./scripts/hooks/pre-commit.sh ./scripts/hooks/pre-push.sh`
    - `./scripts/hooks/install-hooks.sh`

## Release testing
Before releasing a new version, we need to do some final verification.
* Run all the unit/integration/release tests on macOS/Linux/Windows
    * Linux can be easily verified by viewing the built result in Jenkins since we run all our tests on Linux.
    * macOS:
        * Clone the repo
        * Create a fresh virtualenv
        * Install dependencies
        * Run `make unit_test` and `make integration_test`
    * Windows:
        * Launch an EC2 instance with the following parameters:
            * AMI: `ami-021fd4c3adc928916` (community AMI)
            * Instance type: `t3.2xlarge`
            * Network: `vpc-54b03033`(Splunk internal)
            * Region/availability zone: `us-west-2a`
            * Subnet: `subnet-a51abcc2` (bastion)
            * Public IP: `disabled`
            * IAM roles: `appinspect-windows-release-testing`
        * Install the following in the instance:
	        * Google chrome [Optional]
	        * Docker for windows [configure with windows containers]
	        * git & [crlf config](https://confluence.splunk.com/display/~yaxingy/AppInspect+test+on+Windows])
        * Clone this repo in the Windows EC2 instance
        * cd to /path/to/appinspect/
        * Build the image by running the following command: 
            ```
            docker build -t window_appinspect -f .\Dockerfile.windows . 
            ```
        * Create a container with this image: 
            ```
            docker run -it --rm -v C:\path\to\appinspect:C:\appinspect window_appinspect powershell
            ```
        * Run pre-requisites: `make gen_trusted_libs_windows` in PowerShell
        * Run `make unit_test` in PowerShell
        * Run `make integration_test` in PowerShell

        * Helpful reference links:
	        * [Disable Internet Explorer Enhanced Security Configuration](https://medium.com/tensult/disable-internet-explorer-enhanced-security-configuration-in-windows-server-2019-a9cf5528be65)
	        * [Add DNS locally to access git.splunk.com](https://helpdeskgeek.com/networking/edit-hosts-file/)

* Verify the installation package on macOS/Linux/Windows **[optional]**
    1. Create a new virtualenv
    1. Install the package
        ```
        # where 1.6.1rc1+c901a8 is the version you can find verify and you can find it in repo.splunk.com via "simple search", each commit on release/* branch will be built and published to repo.splunk.com
        pip install splunk-appinspect==1.6.1rc1+c901a8 --extra-index-url https://repo.splunk.com/artifactory/api/pypi/pypi-virtual/simple
        ```
    1. Run some simple commands to verify the installed package for the following cases, including:
        * `splunk-appinspect list version`
        * `splunk-appinspect list checks`
        * `splunk-appinspect inspect /path/to/some/app`
        * `splunk-appinspect inspect /path/to/some/app --mode precert`

## Git workflow setup
1. `pip install -r requirements-dev.txt`
2. `pre-commit install -t pre-commit -t pre-push`

# Copyright

Copyright 2017 Splunk Inc. All rights reserved.
