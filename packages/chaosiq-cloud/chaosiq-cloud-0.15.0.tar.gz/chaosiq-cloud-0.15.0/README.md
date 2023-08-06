# ChaosIQ extension for the Chaos Toolkit

[![Build Status](https://travis-ci.com/chaosiq/chaosiq-cloud.svg?branch=master)](https://travis-ci.com/chaosiq/chaosiq-cloud)
[![Python versions](https://img.shields.io/pypi/pyversions/chaosiq-cloud.svg)](https://www.python.org/)
[![Has wheel](https://img.shields.io/pypi/wheel/chaosiq-cloud.svg)](http://pythonwheels.com/)
[![Docker Pulls](https://img.shields.io/docker/pulls/chaosiq/chaostoolkit)](https://hub.docker.com/r/chaosiq/chaostoolkit)

This is the ChaosIQ extension package for the [Chaos Toolkit][chaostoolkit].

[chaostoolkit]: https://chaostoolkit.org

## Purpose

The purpose of this package is to communicate with [ChaosIQ][chaosiq] in
order to:

* Publish experiments
* Publish executions of these experiments
* Safely guard the execution via a set of controls

[chaosiq]: https://chaosiq.io

## Install

Install this package as any other Python packages:

```
$ pip install -U chaosiq-cloud
```

## Usage

Once installed, `signin`, `org`, `publish`, `enable`, `disable`, `team` and `verify` will be added
to the `chaos` command.

```console
$ chaos
Usage: chaos [OPTIONS] COMMAND [ARGS]...

Options:
  --version                   Show the version and exit.
  --verbose                   Display debug level traces.
  --no-version-check          Do not search for an updated version of the
                              chaostoolkit.
  --change-dir TEXT           Change directory before running experiment.
  --no-log-file               Disable logging to file entirely.
  --log-file TEXT             File path where to write the command's log.
                              [default: chaostoolkit.log]
  --log-format [string|json]  Console logging format: string, json.
  --settings TEXT             Path to the settings file.  [default:
                              ~/.chaostoolkit/settings.yaml]
  --help                      Show this message and exit.

Commands:
  disable   Disable a ChaosIQ feature
  discover  Discover capabilities and experiments.
  enable    Enable a ChaosIQ feature
  info      Display information about the Chaos Toolkit environment.
  init      Initialize a new experiment from discovered capabilities.
  org       Set ChaosIQ organisation
  publish   Publish your experiment's journal to ChaosIQ
  run       Run the experiment loaded from SOURCE, either a local file or a...
  signin    Sign-in with your ChaosIQ credentials
  team      Set ChaosIQ team
  validate  Validate the experiment at PATH.
  verify    Run the verification loaded from SOURCE, either a local file or...
```

### Sign-in with ChaosIQ

In order to work, you first need to authenticate with your account on
[ChaosIQ][chaosiq]. First, go there and generate a new token. Copy that
token and paste it when asked from the next command:


```console
$ chaos signin
ChaosIQ url [https://console.chaosiq.io]: 
ChaosIQ token: 
Here are your known organizations:
1) yourorg
2) TeamA
3) TeamB
Default organization to publish to: 2
Experiments and executions will be published to organization 'TeamA'
ChaosIQ details saved at ~/.chaostoolkit/settings.yaml
```

This is now ready to be used.

### Change ChaosIQ Organization

[ChaosIQ][chaosiq] has support for multiple organizations. You can 
specify which of the organizations that you want the ChaosIQ extension to use
by  executing the `org` command:

```console
$ chaos org
Here are your known organizations:
1) yourorg
2) TeamA
3) TeamB
Default organization to publish to: 3
Experiments and executions will be published to organization 'TeamB'
ChaosIQ details saved at ~/.chaostoolkit/settings.yaml
```

This is now ready to be used.

### Publish experiments and executions as you run

Once this extension is installed, it starts transmitting the experiments
and their executions to the [ChaosIQ][chaosiq] in your selected organization.

```console
$ chaos run test.json
[2019-09-25 14:42:34 INFO] Validating the experiment's syntax
[2019-09-25 14:42:34 INFO] Experiment looks valid
[2019-09-25 14:42:34 INFO] Running experiment: EC2 instances are self-healing
[2019-09-25 14:42:35 INFO] Execution available at https://console.chaosiq.io/TeamB/executions/f2133988-a6c0-4c48-ac29-c167cea078c5
[2019-09-25 14:42:35 INFO] Steady state hypothesis: EC2 instance self-heals
[2019-09-25 14:42:36 INFO] Probe: there-should-be-one-running-instance
[2019-09-25 14:42:39 INFO] Steady state hypothesis is met!
[2019-09-25 14:42:40 INFO] Action: stopping-instance-now
[2019-09-25 14:42:41 INFO] Pausing after activity for 5s...
[2019-09-25 14:42:47 INFO] Steady state hypothesis: EC2 instance self-heals
[2019-09-25 14:42:48 INFO] Probe: there-should-be-one-running-instance
[2019-09-25 14:42:50 CRITICAL] Steady state probe 'there-should-be-one-running-instance' is not in the given tolerance so failing this experiment
[2019-09-25 14:42:50 INFO] Let's rollback...
[2019-09-25 14:42:50 INFO] Rollback: starting-instance-again
[2019-09-25 14:42:51 INFO] Pausing before next activity for 15s...
[2019-09-25 14:43:06 INFO] Action: starting-instance-again
[2019-09-25 14:43:08 INFO] Experiment ended with status: deviated
[2019-09-25 14:43:08 INFO] The steady-state has deviated, a weakness may have been discovered

```

### Publish existing execution

The `publish` command enables you to manually push your experimental 
findings, typically recorded in the `journal.json`, to your ChaosIQ
organization.

### Disable safe guards checking

During development time of your experiment, you may wish to disable checking
for safeguards as they can slow your work down. They aren't always relevant
either. To disable the extension from requesting if the execution is allowed
to carry on:

```console
$ chaos disable safeguards
```

Obviously, run the mirroring command to enable them back:

```console
$ chaos enable safeguards
```

### Disable publishing experiments and executions

If you need to disable publishing for a little while:

```console
$ chaos disable publish
```

Note, when you disable publishing, you essentialy disable the entire extension.

Obviously, run the mirroring command to enable publishing again:

```console
$ chaos enable publish
```

### Run a system verification

A system verification is a chaos experiment with an extension block added such as the following:

```javascript
...

  "extensions": [
        {
            "name": "chaosiq",
            "verification": {
                "id": "SOME_GUID",
                "warm-up-duration": 2,
                "frequency-of-measurement": 2,
                "duration-of-conditions": 10,
                "cool-down-duration": 2
            }
        }
    ],
...

```

Typically you would create a verification in your [ChaosIQ console][console]. You can execute a verification in exactly the same way as the [`chaos run`][run] default command in the Chaos Toolkit, but instead of `chaos run` you will use `chaos verify`:

[console]: https://console.chaosiq.io
[run]: https://docs.chaostoolkit.org/reference/usage/run/

```console
$ chaos verify my-excellent-verification.json
```

As with Chaos Toolkit experiments, system verifications may be specified in JSON or YAML formats.

## Contribute

Contributors to this project are welcome as this is an open-source effort that
seeks [discussions][join] and continuous improvement.

[join]: https://join.chaostoolkit.org/

From a code perspective, if you wish to contribute, you will need to run a 
Python 3.5+ environment. Then, fork this repository and submit a PR. The
project cares for code readability and checks the code style to match best
practices defined in [PEP8][pep8]. Please also make sure you provide tests
whenever you submit a PR so we keep the code reliable.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt
```

Then, point your environment to this directory:

```console
$ pip install -e .
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

Don't forget to run the linter regularly:

```
$ pylama chaoscloud
```

### Test

To run the tests for the project execute the following:

```
$ pytest
```

### Release

In order to release this package, you must first bump its version in
`chaoscloud/__init__.py` as well as the CHANGELOG. Commit and push these
changes. Then run the followings:

```
$ git tag VERSION
$ git push origin VERSION
```

where `VERSION` is the semantic version you set in `chaoscloud/__init__.py`.

Once the tag was built, it should have released the package on Pypi.