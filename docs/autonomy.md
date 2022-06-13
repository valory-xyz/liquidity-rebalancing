# Open Autonomy CLI tool

`open-autonomy` is a collection of tools from valory stack packaged into a CLI tool.

## Deploy

```
$ autonomy deploy

Usage: autonomy deploy [OPTIONS] COMMAND [ARGS]...

  Deploy an AEA project.

Options:
  --help  Show this message and exit.

Commands:
  build  Build the agent and its components.
```

### Build tools.

1. Deployment

```bash
Usage: autonomy deploy build deployment [OPTIONS] PUBLIC_ID KEYS_FILE

  Build deployment setup for n agents.

Options:
  --o PATH            Path to output dir.
  --n INTEGER         Number of agents.
  --docker            Use docker as a backend.
  --kubernetes        Use docker as a kubernetes.
  --packages-dir PATH  Path to packages folder (For local usage).
  --dev               Create development environment.
  --force             Remove existing build and overwrite with new one.
  --help              Show this message and exit.
```

To create an environment you'll need a service id and a file containing keys with funds for the chain you want to use.

```bash
# create a docker deployment
$ autonomy deploy build deployment valory/oracle_hardhat deployments/keys/hardhat_keys.json
```

This will create a deployment environment with following directory structure

```
abci_build/
├── docker-compose.yaml
├── nodes
│   ├── node0
│   │   ├── config
│   │   └── data
│   ├── node1
│   │   ├── config
│   │   └── data
│   ├── node2
│   │   ├── config
│   │   └── data
│   └── node3
│       ├── config
│       └── data
└── persistent_data
    ├── benchmarks
    ├── dumps
    └── logs
```

To run this deployment go to the `abci_build` and run `docker-compose up`.

2. Deployment images

```bash
Usage: autonomy deploy build image [OPTIONS] PUBLIC_ID

  Build image using skaffold.

Options:
  --packages-dir PATH   Path to packages folder (For local usage).
  --build-dir PATH     Path to build directory.
  --skaffold-dir PATH  Path to directory containing the skaffold config.
  --version TEXT       Image version
  --push               Push image after build.
  --dependencies       To use the dependencies profile.
  --prod               To use the prod profile.
  --dev                To use the dev profile.
  --cluster            To use the cluster profile.
  --help               Show this message and exit.
```

```bash
#To build an image run
$ autonomy deploy build image valory/oracle_hardhat
```

This will create and image with label `valory/open-autonomy-open-aea:oracle_deployable-0.1.0`. Images generated by this command will follow `valory/open-autonomy-open-aea:app_name-version` format for labels.

## Replay

Replay tools can be use the re run the agents using data dumps from previous runs.

**Note: Replay only works for deployments which were ran in dev mode**

```bash
Usage: autonomy replay [OPTIONS] COMMAND [ARGS]...

  Replay tools.

Options:
  --help  Show this message and exit.

Commands:
  agent       Agent runner.
  tendermint  Tendermint runner.
```

### agent

```bash
Usage: autonomy replay agent [OPTIONS] AGENT

  Agent runner.

Options:
  --build PATH     Path to build dir.
  --registry PATH  Path to registry folder.
  --help           Show this message and exit.
```

### tendermint

```bash
Usage: autonomy replay tendermint [OPTIONS]

  Tendermint runner.

Options:
  --build PATH  Path to build directory.
  --help        Show this message and exit.
```


## Replay agents runs from Tendermint dumps

1. Run your preferred app in dev mode, for example run oracle in dev using `make run-oracle-dev` and in a separate terminal run `make run-hardhat`.

2. Wait until at least one reset (`reset_and_pause` round) has occurred, because the Tendermint server will only dump Tendermint data on resets. Once you have a data dump stop the app.

3. Run `autonomy replay tendermint` . This will spawn a tendermint network with the available dumps.

4. Now  you can run replays for particular agents using `autonomy replay agent AGENT_ID`. `AGENT_ID` is a number between `0` and the number of available agents `-1`. E.g. `autonomy replay agent 0` will run the replay for the first agent.


## Analyse


### ABCI apps

```bash
Usage: autonomy analyse abci [OPTIONS] COMMAND [ARGS]...

  Analyse ABCI apps.

Options:
  --help  Show this message and exit.

Commands:
  check-app-specs     Check abci app specs.
  docstrings          Analyse ABCI docstring definitions.
  generate-app-specs  Generate abci app specs.
  logs                Parse logs.
```


**Generate ABCI App specs**

```bash
Usage: autonomy analyse abci generate-app-specs [OPTIONS] APP_CLASS OUTPUT_FILE

  Generate abci app specs.

Options:
  --mermaid  Mermaid file.
  --yaml     Yaml file.
  --json     Json file.
  --help     Show this message and exit.
```

**Check ABCI App specs**

```bash
Usage: autonomy analyse abci check-app-specs [OPTIONS]

  Check abci app specs.

Options:
  --check-all          Check all available definitions.
  --packages-dir PATH  Path to packages directory; Use with `--check-all` flag
  --mermaid            Mermaid file.
  --yaml               Yaml file.
  --json               Json file.
  --app_class TEXT     Dotted path to app definition class.
  --infile PATH        Path to input file.
  --help               Show this message and exit.
```

**Check ABCI app docstrings**

```bash
Usage: autonomy analyse abci docstrings [OPTIONS] [PACKAGES_DIR]

  Analyse ABCI docstring definitions.

Options:
  --check
  --help   Show this message and exit.
```

**Parse logs from a deployment**

```bash
Usage: autonomy analyse abci logs [OPTIONS] FILE

  Parse logs.

Options:
  --help  Show this message and exit.
```

### benchmarks

```bash
Usage: autonomy analyse benchmarks [OPTIONS] PATH

  Benchmark Aggregator.

Options:
  -b, --block-type [local|consensus|total|all]
  -d, --period INTEGER
  -o, --output FILE
  --help                          Show this message and exit.
```

Aggregating results from deployments.

To use this tool you'll need benchmark data generated from agent runtime. To generate benchmark data run

```
$ autonomy deploy build deployment SERVICE_ID PATH_RO_KEYS --dev
```

By default this will create a 4 agent runtime where you can wait until all 4 agents are at the end of the first period (you can wait for more periods if you want) and then you can stop the runtime. The data will be stored in abci_build/persistent_data/benchmarks folder. 

Run deployment using

```bash
$ cd abci_build/
$ docker-compose up
```

You can use this tool to aggregate this data.

```bash
autonomy analyse benchmarks abci_build/persistent_data/benchmarks
```

By default tool will generate output for all periods but you can specify which period to generate output for, same goes for block types as well.