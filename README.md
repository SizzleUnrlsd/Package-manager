
# PACKAGE-MANAGER

This project is a small building block in a larger project. It aims to create a packet manager and organise code updates for projects such as "TekSH" and "TekOS".
## Run the server

Clone the project

```bash
  git clone https://github.com/SizzleUnrlsd/Package-manager
```

Go to the project directory

```bash
  cd Package-manager/
```

Install dependencies

```bash
  make
```

Start the server

```bash
  make run
```

Entry into the server
```bash
  make it
```

Retrieve the data.json file manually 
```bash
  make data_cp
```

Stop the server
```bash
  make stop
```

## Run the client

Shows all available packets
```bash
  ./client.py get
```

Retrieves a packet file
```bash
  ./client.py get --get-files --package-files {packet name}
```

Adds a packet and its version without a file
```bash
  ./client.py add --name {packet name} --version {package_version}
```

Adds a packet and its version with a file
```bash
  ./client.py add --name {packet name} --version {package_version} --file {packet_file}
```

Delete a packet
```bash
  ./client.py delete --name {packet name}
```

## Authors

- [@SizzleUnrlsd](https://github.com/SizzleUnrlsd)

