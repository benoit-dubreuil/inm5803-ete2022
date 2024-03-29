# Development


## Configuration

The version of Python is defined in the file [.python-version](../.python-version).

Install the dependencies :

```sh
sudo apt update
sudo apt install -y mpich libmpich-dev libxml2-dev libxslt1-dev
python -m pip install --user --upgrade pip setuptools wheel
```

`mpich`, `libmpich-dev`, `libxml2-dev` and `libxslt1-dev` are necessary for Simulation Generator.

Set up the `venv` and install the requirements :

```sh
python3 -m venv env &&  # Create the `venv`, if necessary
source ./env/bin/activate &&
pip install -r requirements.txt &&
pip install --editable .  # Install the project in develop mode
```


## Conventions

See [conventions](dev-conventions.md)


## GitHub workflows

### Create Issue Branch

The [Create Issue Branch](https://github.com/robvanderleek/create-issue-branch) GitHub Action and actual GitHub workflow
automates the creation of issue branches after assigning an issue.

Its workflow is located at `.github/workflows/create-issue-branch.yml`. Its configuration is located
at `.github/issue-branch.yml`.

The issue branches created are named with the following
pattern: `${lowercased label}/issue-${number}/${lowercased issue title in which unsafe characters are replaced by the character "-"}`
.

The supported labels are `bug`, and `feature`, `doc` and `QA`. As an exception, the `bug` label actually generates the
prefix `fix` in created branches. Any other label exclude the assigned issue from automatic branch creation.

The Create Issue Branch GitHub Action also automatically closes issue which its PR was merged to the `dev/` branch.

The GitHub Action creates an open draft PR when an issue is assigned and labelled correctly. The issue's description and
labels are copied to the automatically created PR.


### Dependent Issues

The [Dependent Issues](https://github.com/z0al/dependent-issues) GitHub Action and actual GitHub workflow allows issues
and PRs dependency management through keywords in descriptions.

Its workflow and configuration is located at `.github/workflows/dependent-issues.yml`.

The keywords are `depends on` and `blocked by`, according to the configuration. Also, the Dependent Issues GitHub Action
labels issues and PRs that are dependent on others with the label `dependent`, according to the configuration. Finally,
the GitHub Action adds itself to the list of status checks required to pass before merging PRs.


### Sync LINUM mirror repository

#### Project repository

When a _push_ event is triggered on the `prod` branch, the repository is synchronized with
its [respective LINUM mirror repository](https://github.com/linum-uqam/inm5803-ete2022-benoit-dubreuil). Once the remote
is synchronized, every git `refs`, `tags` and `branches` from that repository are pruned and replaced by the ones from
this repository.


#### Simulation Generator temporary fork

When a _push_ event is triggered on the `master` branch of the Simulation Generator temporary fork, the repository is
synchronized with
its [respective LINUM mirror repository](https://github.com/linum-uqam/voxsim). Once the remote
is synchronized, every git `refs`, `tags` and `branches` from that repository are pruned and replaced by the ones from
this repository.


## Tools

### Simulation Generator

[Simulation Generator](https://github.com/AlexVCaron/voxsim) runs only on Linux due to its dependency
to [Singularity](https://sylabs.io/singularity).
See [benoit-dubreuil / inf6200-h2022 / guides / outils.md # simulation generator](https://github.com/benoit-dubreuil/inf6200-h2022/blob/main/guides/outils.md#simulation-generator)
.
