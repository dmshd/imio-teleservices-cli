# iA.Téléservices CLI (imio-teleservices-cli)

## Overview

The iA.Téléservices CLI is a command-line interface designed to manage Teleservices instances efficiently. This tool allows users to list, filter, and connect to various Teleservices instances.

## Use Cases

- List all Teleservices instances.
- List Teleservices instances filtered by name or package.
- SSH into a Teleservices instance via provided arguments.
- Display the URL of Teleservices instances.

## Requirements

- Python 3.x
- Click library
- Requests library

## Usage

### List All Teleservices Instances

```sh
$ python3 cli.py list
```

### List Teleservices Instances by Name

```sh
$ python3 cli.py list --name saint
```

### List Teleservices Instances by Package

```sh
$ python3 cli.py list --package imio_ts_aes
```

### Connect to a Teleservices Instance

```sh
$ python3 cli.py ssh etalle
```

### Connect to a Teleservices Instance by Name

```sh
$ python3 cli.py ssh saint
```

### List URLs of All Teleservices Instances

```sh
$ python3 cli.py list --url-only
```

### List Teleservices Instances by Package and Display Only the URL

```sh
$ python3 cli.py list --package imio_townstreet --url-only
```

### List Teleservices Instances by Host

```sh
$ python3 cli.py list --host ts021
$ python3 cli.py list --host ts021 --url-only
```

## Options

### Global Options

- `--verbose`: Enables verbose mode for detailed logging.

### List Command Options

- `--name, -n`: Filter instances by name. Part of the name is sufficient.
- `--package, -p`: Filter instances by package.
- `--url-only`: Display only the URL of the Teleservices.
- `--host, -h`: Filter instances by host.

## Example Commands

- List all instances:

  ```sh
  $ python3 cli.py list
  ```

- List instances containing "saint" in the name:

  ```sh
  $ python3 cli.py list --name saint
  ```

- List instances with the package "imio_ts_aes":

  ```sh
  $ python3 cli.py list --package imio_ts_aes
  ```

- SSH into an instance named "etalle":

  ```sh
  $ python3 cli.py ssh etalle
  ```

- Display only URLs of instances:
  ```sh
  $ python3 cli.py list --url-only
  ```

## Implementation Details

The CLI script is implemented using the `Click` library for command-line parsing and `Requests` for HTTP requests to the infrastructure API. The configuration settings and user details are managed through a `Config` class, with support for verbose logging to provide detailed feedback during execution.

For more detailed information about each function and its usage, please refer to the inline documentation within the script.

## Make the script accessible from anywhere

To make the `cli.py` script accessible from anywhere, you can add an alias to your `~/.bashrc` (for Bash users) or `~/.zshrc` (for Zsh users) file.

1. Open your `~/.bashrc` or `~/.zshrc` file in a text editor.
   ```sh
   vi ~/.bashrc
   # or
   vi ~/.zshrc
   ```
2. Add the following line to create an alias for the script:

   ```sh
   alias ts_cli='python3 /path/to/your/repository/cli.py'
   ```

   Replace `/path/to/your/repository` with the actual path to your cloned repository.

3. Save the file and exit the editor.

4. Reload your shell configuration to apply the changes:

   ```sh
   source ~/.bashrc
   # or
   source ~/.zshrc
   ```

5. Now you can use `ts_cli` from anywhere:
   ```sh
   ts_cli list
   ts_cli ssh etalle
   ```
