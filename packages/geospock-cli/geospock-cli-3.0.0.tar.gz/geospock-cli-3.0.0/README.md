# GeoSpock CLI

## Installation

### Installing the CLI from pip
```
    $ python -m pip install geospock-cli
```


### Logging in with your enterprise Identity Provider (GeoSpock v3.1 and above)
The `login` command creates a configuration file with an encoded copy of your username and password along with the 
request address for your deployment.

Alternatively, if you do not want to save your details in a config file: 
 - all geospock commands can be run with the arguments `--user <value> --password <value> --request-address 
<value>`.
 - the CLI will also check for the environment variables `GEOSPOCK_USER` and `GEOSPOCK_PASSWORD` and use these to 
 authenticate. The `--request-address <value>` argument will still need to be added to the command.

An optional `--profile {profileID}` argument can be used to set up configurations for multiple GeoSpock deployments.
All subsequent `geospock` commands can then use this profile flag to specify that deployment.


### Getting credentials for the inbuilt Identity Provider (GeoSpock v3.0)
The `init` command creates a configuration file with the argument values for your your deployment:

`geospock init --clientid abcdefgh1234 --audience https://testaudience.geospock.com --auth0url login.test.com 
--request-address https://testrequest.geospock.com/graphql`

An optional `--profile {profileID}` argument can be used to set up configurations for multiple GeoSpock deployments.
All subsequent `geospock` commands can then use this profile flag to specify that deployment.

To authenticate the CLI to use your GeoSpock account, the following command can be used (alternatively this will be run
automatically when a user first tries to use a command).

`geospock get-credentials [--profile {profileID} --no-browser]`

This will open a web-page in the user's default web browser to authenticate. If the `--no-browser` flag is added, this 
will instead provide a web-address for a user to visit in order to authenticate.
The user should enter their GeoSpock username and password when requested to authorise the CLI.
This process should only be required once per user per profile.

### Running the CLI
The CLI can be activated at the command line using `geospock COMMAND ... [--profile {profileID}]`
A list of commands can be shown by using `geospock help [--profile {profileID}]`. Further information on the 
input types of each command can be obtained by running `geospock help COMMAND [--profile {profileID}]`.