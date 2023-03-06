All contributions are welcome – especially:

- documentation,
- bug reports and issues,
- code contributions.

### Code

If you'd like to actively develop or help maintain this project then there are existing tests against which you can test the library with. Typically, this looks like

- `git clone git@github.com:aliev/aioshutdown.git`
- `cd aioshutdown`
- `python -mvenv env`
- `source env/bin/activate`
- `make dev-install`

`make dev-install` will also install all the required packages that will allow you to adhere to the code styling guide of `aioshutdown`.

Basically we use the `black` and `flake8` packages for code formatting, `pre-commit` package will check the code formatting before your first commit is made.

To automatically correct the formatting you can run the command inside the repository root:

```
make lint
```
