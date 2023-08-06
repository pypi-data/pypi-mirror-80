[![PyPI version](https://badge.fury.io/py/json-schema-for-humans.svg)](https://badge.fury.io/py/json-schema-for-humans)

# JSON Schema for Humans

Quickly generate a beautiful HTML static page documenting a JSON schema

[Documentation (with visual examples)](https://coveooss.github.io/json-schema-for-humans)

## Installation
```
pip install json-schema-for-humans
```

## Usage

[Options for generation of the doc are documented using this very library](https://coveooss.github.io/json-schema-for-humans/assets/config_schema.html)

They can be supplied in various ways:
- Using a JSON or YAML configuration file with the CLI option `--config-file`
- Using the CLI option `--config`
- Using a `ConfigurationOption` from code

More details are available in the appropriate sections below.

### From CLI

```
generate-schema-doc [OPTIONS] SCHEMA_FILE [RESULT_FILE]
```

`SCHEMA_FILE` must be a valid JSON Schema (in JSON or YAML format)

The default value for `RESULT_FILE` is `schema_doc.html`

#### CLI options

#### --config
Supply generation config parameters. The parameters are documented in the JSON schema `config_schema.json` at the root of the repo.

Each parameter is in the format `--config parameter_name=parameter_value`. Example: `--config expand_buttons=true`. The parameter value must be valid JSON.

For flags, you can also omit the value for `true` or prefix the parameter name with `no_` for `false`. Example: `--config expand_buttons` or `--config no_expand_buttons`.

#### --config-file
Path to a JSON or YAML configuration file respecting the schema `config_schema.json`.

Example: `--config-file jsfh-conf.yaml` where `jsfh-conf.yaml` is in the current directory and contains the following:

```yaml
description_is_markdown: false
expand_buttons: true
copy_js: false
```

##### --expand-buttons
*Deprecated* Use `--config expand_buttons` or a config file

Off by default

Add an `Expand all` and a `Collapse all` button at the top of the generated documentation

##### --link-to-reused-ref/--no-link-to-reused-ref
*Deprecated* Use `--config no_link_to_reused_ref` or a config file

On by default

If several `$ref` points to the same definition, only render the documentation for this definition the first time.
All other occurrences are replaced by an anchor link to the first occurrence.

##### --minify/--no-minify
*Deprecated* Use `--config no_minify` or a config file

On by default

Minify the output HTML document

##### --deprecated-from-description
*Deprecated* Use `--config deprecated_from_description` or a config file

Off by default

Mark a property as deprecated (with a big red badge) if the description contains the string `[Deprecated`

##### --default-from-description
*Deprecated* Use `--config default_from_description` or a config file

Off by default

Extract the default value of a property from the description like this: ``[Default `the_default_value`]``

The default value from the "default" attribute will be used in priority

##### --copy-css/--no-copy-css
*Deprecated* Use `--config no_copy_css` or a config file

On by default

Copy `schema_doc.css` to the same directory as `RESULT_FILE`.

##### --copy-js/--no-copy-js
*Deprecated* Use `--config no_copy_js` or a config file

On by default.

Copy `schema_doc.min.js` to the same directory as `RESULT_FILE`.

This file contains the logic for the anchor links

### From code

There are 3 methods that one could use:

Method Name | Schema input | Output | CSS and JS copied?
--- | --- | --- | ---
generate_from_schema | `schema_file` as str, Path (from pathlib) or a file object | Rendered HTML as a str | No
generate_from_filename | `schema_file_name` as a str or Path | Rendered HTML written to the file at path `result_file_name` | Yes
generate_from_file_object | `schema_file` as an open file object (read mode) | Rendered HTML written to the file at `result_file`, which must be an open file object (in write mode) | Yes

Notes:
- When using file objects, it is assumed that files are opened with encoding "utf-8"
- CSS and JS files are copied to the current working directory with names "schema_doc.css" and "schema_doc.min.js" respectively
- Other parameters of these methods are analogous to the CLI parameters documented above.

#### The GenerationConfiguration object
To reduce the number of parameters to pass from function to function in the code, there is a `GenerationConfiguration` object that should be used for providing options.

Example:

```python
from json_schema_for_humans.generate import GenerationConfiguration, generate_from_filename


config = GenerationConfiguration(copy_css=False, expand_buttons=True)

generate_from_filename("my_schema.json", "schema_doc.html", config=config)

# Your doc is now in a file named "schema_doc.html". Next to it, "schema_doc.min.js" was copied, but not "schema_doc.css"
# Your doc will contain a "Expand all" and a "Collapse all" button at the top

```

#### Pre-load schemas
`generate_from_schema` has a `loaded_schemas` parameter that can be used to pre-load schemas. This must be a dict with the key being the real path of the schema file and the value being the result of loading the schema (with `json.load` or `yaml.safe_load`, for example).

This should not be necessary in normal scenarios.

## What's supported

See the excellent [Understanding JSON Schema](https://json-schema.org/understanding-json-schema/index.html) to understand what are those checks

The following are supported:
- Types
- Regular expressions
- String length
- Numeric types multiples and range
- Constant and enumerated values
- Required properties
- Pattern properties
- Default values
- Array `minItems`, `maxItems`, `uniqueItems`, `items` (schema that must apply to all of the array items), and `contains`
- Combining schema with `oneOf`, `allOf`, `anyOf`, and `not`
- Examples
- Conditional subschemas

These are **not** supported at the moment (PRs welcome!):
- String format
- Property names and size
- Array items at specific index (for example, first item must be a string and second must be an integer)
- Property dependencies
- Media

## References

References are supported:

- To another part of the schema, e.g. `{ $ref: "#/definitions/something" }`
- To a local file, `{"$ref": "references.json"}`, `{"$ref": "references.json#/definitions/something"}`
- To a URL, `{"$ref": "http://example.com/schema.json"}`, `{"$ref": "http://example.com/schema.json#/definitions/something"}`


You _can_ have a `description` next to a `$ref`, it will be displayed in priority to the description from the referenced element.

If you have several attributes using the same definition, the definition will only be rendered once.
All other usages of the same definition will be replaced with an anchor link to the first render of the definition.
This can be turned off using `--config no_link_to_reused_ref`. See `With references` in the examples.

## Anchor links
Clicking on a property or tab in the output documentation will set the hash of the current window. Opening this anchor link will expand all needed properties and scroll to this section of the schema. Useful for pointing your users to a specific setting.

For this feature to work, you need to include the Javascript file (`schema_doc.min.js`) that is automatically copied next to the output HTML file (`schema_doc.html` by default).

## Development

### Testing
Just run tox

`tox`

### Modifying Javascript
`schema_doc.js` is not minified automatically, you are responsible for doing it yourself

### Generating doc
The documentation is generated using jekyll and hosted on GitHub Pages

- Change your current working directory to `docs`
- Run ``python generate_examples.py``. This will get all examples from `tests/cases`, render the resulting HTML and
 include it in the appropriate folders in the jekyll site.
- If you have added an example, add the file name (without `.json`), the display name and description in `_data/examples.yaml`