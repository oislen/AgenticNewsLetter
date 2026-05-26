# AgenticNewsLetter

An agentic data-science newsletter generator. A LangGraph pipeline pulls
fresh news on a randomly selected topic, drafts a stylised newsletter with
an AWS Bedrock LLM, and emails it to a subscriber. The whole thing runs on
a scheduled AWS Lambda, with infrastructure managed via the AWS CDK.

## Architecture overview

The pipeline is a three-node LangGraph:

```
researcher  -->  writer  -->  publisher
```

- **researcher** queries the Tavily Search API for recent news on a
  randomly chosen `topic` / `subtopic`.
- **writer** transforms the research into a markdown newsletter draft
  using a Bedrock chat model, applying one of several style guides
  (`academic`, `ELI5`, `tutorial`).
- **publisher** converts the markdown to HTML and sends it via SMTP.

Secrets (Tavily API key, sender SMTP password) live in AWS Secrets
Manager. The Lambda is built and shipped as a container image.

## Directory layout

```
AgenticNewsLetter/
├── aws/
│   ├── cdk/
│   │   ├── app.py                 # CDK app entry point
│   │   ├── cdk.json
│   │   ├── exeCdkTest.cmd
│   │   └── stacks/
│   │       ├── NewsletterStack.py
│   │       └── constructs/        # Lambda, ECR, EventBridge, SecretsManager, ...
│   └── refresh_credentials.cmd
├── doc/
│   ├── agentic_newsletter_graph.drawio   # pipeline flowchart
│   └── aws_cdk_stack.drawio              # infrastructure flowchart
├── newsletter/
│   ├── LambdaHandler.py           # Lambda entry point
│   ├── main.py                    # local entry point
│   ├── graph.py                   # LangGraph wiring
│   ├── state.py                   # NewsletterState TypedDict
│   ├── cons.py                    # paths and constants
│   ├── exeMain.cmd / exeMain.sh   # local run scripts
│   ├── entry.sh                   # container entrypoint
│   ├── nodes/
│   │   ├── researcher.py
│   │   ├── writer.py
│   │   ├── publisher.py
│   │   └── unittests/             # unittest suites for each node
│   └── utils/
│       ├── boto3_session.py
│       ├── bedrock_client.py
│       ├── get_secrets.py
│       ├── random_inputs.py
│       ├── style_guides.py
│       ├── topics.py
│       └── unittests/             # unittest suites for each util
├── Dockerfile
├── compose.yaml
├── buildspec.yml                  # CodeBuild spec
├── exeDocker.cmd                  # local docker build
├── exeUnitTests.cmd               # run all unit tests
├── pyproject.toml / uv.lock       # uv project + lockfile
├── requirements.txt
└── README.md
```

| Path | Purpose |
| --- | --- |
| [newsletter/](newsletter/) | Core application logic — the LangGraph pipeline, nodes, utilities, state, and the Lambda handler. |
| [newsletter/nodes/](newsletter/nodes/) | The three graph nodes (`researcher`, `writer`, `publisher`) plus their unit tests. |
| [newsletter/utils/](newsletter/utils/) | Shared helpers — boto3 session/clients, secret retrieval, style guides, topic taxonomy, random-input generation — plus their unit tests. |
| [aws/](aws/) | AWS infrastructure-as-code. |
| [aws/cdk/](aws/cdk/) | AWS CDK app and stacks that provision the Lambda, ECR image, schedule, IAM roles, and secrets bindings. |
| [doc/](doc/) | Rough draw.io flowcharts for the agentic pipeline ([agentic_newsletter_graph.drawio](doc/agentic_newsletter_graph.drawio)) and the CDK stack ([aws_cdk_stack.drawio](doc/aws_cdk_stack.drawio)). |
| [Dockerfile](Dockerfile) / [compose.yaml](compose.yaml) | Container image definition used by the Lambda. |
| [buildspec.yml](buildspec.yml) | AWS CodeBuild spec for building and pushing the image. |
| [pyproject.toml](pyproject.toml) / [uv.lock](uv.lock) | Python project definition and `uv` lockfile (Python 3.14). |
| [requirements.txt](requirements.txt) | Pinned dependency list (mirrors `pyproject.toml`). |
| [exeDocker.cmd](exeDocker.cmd) | Builds the Docker image locally. |
| [exeUnitTests.cmd](exeUnitTests.cmd) | Runs all unit tests under `newsletter/nodes/unittests` and `newsletter/utils/unittests`. |

## Running locally

The project uses [`uv`](https://docs.astral.sh/uv/) for dependency
management. To run the newsletter pipeline end-to-end:

```cmd
cd newsletter
exeMain.cmd
```

This invokes `uv run main.py`, which calls the Lambda handler with empty
event/context. Credentials are loaded from `.env` plus the `.creds/`
directory referenced in [newsletter/cons.py](newsletter/cons.py).

## Running the unit tests

From the project root:

```cmd
exeUnitTests.cmd
```

This discovers and runs all tests under
[newsletter/nodes/unittests/](newsletter/nodes/unittests/) and
[newsletter/utils/unittests/](newsletter/utils/unittests/) using the
standard `unittest` library via `uv run python -m unittest discover`.

## Deploying

Infrastructure is defined in [aws/cdk/](aws/cdk/). The Lambda runs on a
schedule, pulls its container image from ECR, and reads secrets from
AWS Secrets Manager. See [aws/cdk/app.py](aws/cdk/app.py) and the
stacks under [aws/cdk/stacks/](aws/cdk/stacks/) for the full topology.
