# GeoSpock CLI

## Release 3.0.0

#### Breaking Changes
 - V3-794 Basic authentication credentials are now stored in the keychain.

## Release 2.3.0

#### Features
 - V3-514 Allow sending of stringified JSON when loading from file and expected type is String


## Release 2.2.0

#### Features
 - V3-779 Pass `TRUE` as value when `--<argument>` has no value set in command-line (i.e. it is either followed by 
 another `--<argument>` or it is the last item) where that argument is of type `enum` and the value `TRUE` is allowed.

#### Bug Fixes
 - V3-774 Provide more helpful error when `--user` provided but no `--password`.


## Release 2.1.0

#### Features
 - V3-477 Enable basic authentication with username and password.
 
#### Bug Fixes
 - V3-551 Ensure `--user` and `--password` arguments are provided when using `geospock login`.


## Release 2.0.0

#### Breaking changes
 - V3-183 Enforce reading of data-source-descriptions from files and enable variable file extensions.

#### Bug fixes
 - V3-325 `geospock help <command>` now shows default values for arguments correctly.
 - V3-327 Allow only integers to be submitted for parameters marked as type `Int`.
 - V3-372 Prevent stacktrace leak when credentials file is missing.


## Release 1.0.1

#### Bug fixes
 - V3-323 Reporting any error now exits with an exit code other than 0. 
 - V3-321 Modify the cleaning of query responses to accept arbitrary type as input.


## Release 1.0.0 
 
#### Features
 - V3-291 `null` values removed from CLI responses when stripNulls specified in CLI template.

#### Bug Fixes
 - V3-237 Will now only save valid credentials, otherwise CLI exits with error message.


## Release 0.1.4

#### Features
 - GS-10984 Can now load schema files from s3.
  
#### Bug fixes
 - V3-172 Add non-zero exit code when exception during display_result.
 
 
## Release 0.1.3

#### Features
 - GS-10983 Add profile-list command to list initialised profiles.
 - GS-10998 Automatically open a web browser with the correct link when running get-credentials.

#### Bug fixes
 - GS-10988 Added check that list item is dict when recursively removing nulls.
 
 
## Release 0.1.2

#### Bug fixes
- GS-10972 Exit code 1 when args missing from command.


## Release 0.1.1

#### Features
 - Improved messaging when we provide an invalid command.


## Release 0.1.0

#### Notes
 - Initial release.