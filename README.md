# fancifier

## Development

### Install development dependencies

```bash
pipx install uv
```

### Install dependencies

```bash
uv pip install -r requirements.txt
```

### Create venv

```bash
uv venv
```

### Initialize Virtual Environment

```bash
source .venv/bin/activate
```

### Add a dependency

```bash
uv pip install <package-name>
```

### Generate requirements.txt

```bash
uv pip freeze | uv pip compile - -o requirements.txt
```

### Sync locked dependencies with venv

```bash
uv pip sync requirements.txt
```
