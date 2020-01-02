## Contributing


### Contribution rules
- The code must be tested with molecule.
- Python test package: `pytest` (with possibility to use unittest mocks) with `testinfra` module.
- Code style: PEP8
- Programming language for code and comments: english


### Coding conventions in Python
- 120 character max per line
- Use python 3.6 `fstring` instead of `format()` or `%s`
- Directories and filenames in `snake_case`
- Class names in `UpperCamelCase`
- Function and method names in `snake_case`
- Private and protected function and method names prefixed with `_`
- Please implement private function and method under the corresponding public for more readability
- Variables name in `snake_case`, constants `MAJ_SNAKE_CASE`

### Coding convention in Ansible
- file and folder permisions are specified using the letter permission format (example: `u=rwX,g=r,o=r`). Please note that `X` gives the executable permission only on directory, not on files.
- all the Ansible variables used in the role must be declared in the `defaults/main.yaml` file. 