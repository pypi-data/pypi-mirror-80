# sym-cli

Sym CLI

## Shell Completion

Bash:

    eval "$(env _SYM_COMPLETE=source_bash sym)"

Zsh:

    eval "$(env _SYM_COMPLETE=source_zsh sym)"

TODO: Build an [activation script](https://click.palletsprojects.com/en/7.x/bashcomplete/#activation-script) and ship with the code?

## Testing setuptools

This setup is based on [Click's docs](https://click.palletsprojects.com/en/7.x/setuptools/) for setuptools integration.

### pyenv-virtualenv setup

Install `pyenv-virtualenv` so you can create a virtualenv to install the CLI into:

    $ brew install pyenv-virtualenv

Add the following to your `.zshrc`:

    eval "$(pyenv init -)"
    if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi

### Install the CLI

Now install the CLI into a new virtualenv to make sure you've got everything working right:

    $ pyenv activate symcli
    $ pyenv install --editable .
    $ sym --help

### Release

1. Set a PyPI API token in your local env
2. `./scripts/dist.sh`

* Releasing new tagged artifacts should be automated in CI and master should be releasable at any time.

## Quality

We need to have high confidence that when we ship our CLI to customers, it will work. We can achieve that by
improving our testing prior to release, and implementing useful diagnostics and reporting commands into the CLI.

### Testing

We should establish a set of workflows that we can run as acceptance tests to ensure we have confidence in the
product prior to releasing for customers. We need to enumerate these workflows, then work to automate them in CI.

Since we already have a lot of functionality and not a lot of clear acceptance test workflows, we can define some basic
milestones to build towards a better quality state:

* Create static AWS profile with access to a set of ec2 instances. Run `sym ssh`, `sym exec`, and `sym ansible-playbook` using
`--saml-client=aws-profile`.
* Set up a CI flow to simulate MFA with `saml2aws`. Run the above workflow using the `test` sym resource instead of the `aws-profile`.
* Set up scale and resiliency tests to detect transient issues.

### Dump and check

The CLI is particularly challenging because it is integrating a lot of new technologies and it can be easy to get into an unexpected state
or make a wrong assumption about how the infrastructure will behave. We also will have limited visibility into our customer's environment
and want to minimize round-trip debug loops.

We can implement CLI commands that help dump useful information (environment, config, user state, etc) and run health checks (credentials valid,
systems online, dependencies are on the path and the expected version). We could implement complex checks like, given a sym resource, make sure the
user can SSH into every instance.

## Tech Debt

* Limited expertise across the team. We need more people to get involved in contributing new functionality.
* Quality. We need to get existing tests running in CI. We need to implement the testing strategy described above to establish a baseline understanding of quality.
* Unclear release process.
* Complex command line flow. Large use of decorators and recursive subprocesses make it hard to reason about changes to the code.
