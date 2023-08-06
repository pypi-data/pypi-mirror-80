# workstation-cli

This tool registers a work station given a daas-token generated from DaaS Website.

## prerequisites

- python >=3.6
- openssl

## Install

```bash
pip install sourcesense-vessel
```

## Usage

```bash
Usage: vessel-cli [OPTIONS] COMMAND [ARGS]...

  Vessel cli tool

Options:
  --debug  output debug log [False]
  --help   Show this message and exit.

Commands:
  deploy    Deploy agent and sentinel for given TOKEN
  init      Init vault
  register  Register workstaion to Vessel with the given TOKEN
  unseal    Unseal vault

```

### Register

```bash
Usage: vessel-cli register [OPTIONS] TOKEN

  Register workstaion to Vessel with the given TOKEN

Options:
  --cluster-host TEXT  Hostname of the cluster to control  [required]
  --cluster-ro TEXT    Cluster read-only service-account token  [required]
  --cluster-rw TEXT    Cluster read-write service-account token  [required]
  --vault TEXT         Vault endpoint [http://vault.local]
  --openshift          Cluster is an Openshift distribution [False]
  --init               Initialize Vault [False]
  --deploy             Deploy agent and sentinel container automatically
                       [False]

  --vessel-api TEXT    Vessel API RPC endpoint [http://cloud-
                       api.oc.corp.sourcesense.com/rpc]

  --help               Show this message and exit.
```

### Deploy


### development tests

From inside the vagrant box `workstation-ansible` you can register a cluster this way after obtained the `<TOKEN>` from the webapp:

```bash
vessel-cli init
# choose a password

vessel-cli --debug register \
  --cluster-host https://kubernetes.default:6443 \
  --cluster-ro $DAAS_CLU_READER_TOKEN \
  --cluster-rw $DAAS_MANAGER_TOKEN
  --deploy <TOKEN>


```

## DEBUG

```bash
# setup python environment
brew install pyenv
pyenv install 3.7.7
echo eval "$(pyenv init -)" > ~/.bashrc

pyenv global 3.7.7
pyenv virtualenv vessel
pyenv local vessel

python setup.py develop
```
