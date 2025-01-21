## Automation: building and uploading with `Makefile` - DEV Tutorial

In the project directory run <code>make</code>. This command will run the <code>Makefile</code>, which performs actions listed below:

<ul>
<li>remove old version of the package,</li>
<li>ask which version we want to update (major, minor, patch) and increment it automatically, <code>push</code> the changes to GitHub with new tag,</li>
<li>build a new version,</li>
<li>upload the package to PyPI,</li>
<li>upload the package to TestPyPI.</li>
</ul>

At this moment the Makefile is configured to only delete the old release, create a new tag and push it to GitHub. The custom workflow handles building and uploading the package on new tag push.

<br/>

<ol>
<li> Test the <code>Makefile</code>

<br/>
<br/>

```bash
make --dry-run
```

</li>

<br/>

<li> Run the <code>Makefile</code>

<br/>
<br/>

```bash
make
```

</li>
</ol>

<br/>
<br/>

## Building package - DEV Tutorial based on official DOCS

<ol>

<li> Upgrade pip

<br/>
<br/>

```bash
python3 -m pip install --upgrade pip
```

</li>
<br/>

<li> Prepare files and directories

<br/>
<br/>

```bash
directory_used_for_package/
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   └── name_of_the_package/
│       ├── __init__.py
│       └── example.py
└── tests/
```

</li>
<br/>

<li> Choose build backend (I chose <code>setuptools</code>)

<br/>
<br/>

```bash
python3 -m pip install --upgrade setuptools
```

</li>
<br/>

<li> Prepare <code>pyproject.toml</code> file (this package's configuration as an example)

<br/>
<br/>

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "zaowr_polsl_kisiel"
license = {file = "LICENSE"}
dynamic = ["version", "readme", "dependencies", "optional-dependencies"]
authors = [
  { name="Maksymilian Kisiel" },
]
description = "A simple Python package used by me and my friends at university in the 'Advanced Image, Video and Motion Analysis' course."
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
keywords = ["polsl", "zaowr", "2024/2025", "IGT", "ZAOWR"]

[tool.setuptools.dynamic]
version = {attr = "zaowr_polsl_kisiel.__version__"}  # any module attribute compatible with ast.literal_eval
readme = {file = ["README.md",[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "zaowr_polsl_kisiel"
license = {file = "LICENSE"}
dynamic = ["version", "readme", "dependencies", "optional-dependencies"]
authors = [
  { name="Maksymilian Kisiel" },
]
description = "A simple Python package used by me and a friend at the university in the course 'Advanced Image, Video and Motion Analysis'"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
keywords = ["polsl", "zaowr", "2024", "IGT", "ZAOWR"]

[tool.setuptools.dynamic]
version = {attr = "zaowr_polsl_kisiel.__version__"}  # any module attribute compatible with ast.literal_eval
readme = {file = ["README.md", "./docs/WINDOWS.md", "./docs/USAGE.md"], content-type = "text/markdown"}
dependencies = {file = ["requirements.txt"]}
optional-dependencies.dev = {file = ["dev-requirements.txt"]}

[project.urls]
Repository = "https://github.com/revalew/zaowr-py-package"
Issues = "https://github.com/revalew/zaowr-py-package/issues"
Changelog = "https://github.com/revalew/zaowr-py-package/releases"
Documentation = "https://github.com/revalew/zaowr-py-package/blob/master/docs/USAGE.md" "./docs/USAGE.md"], content-type = "text/markdown"}
dependencies = {file = ["requirements.txt"]}
optional-dependencies.dev = {file = ["dev-requirements.txt"]}

[project.urls]
Repository = "https://github.com/revalew/zaowr-py-package"
Issues = "https://github.com/revalew/zaowr-py-package/issues"
Changelog = "https://github.com/revalew/zaowr-py-package/releases"
Documentation = "https://github.com/revalew/zaowr-py-package/blob/master/docs/USAGE.md"
```

</li>
<br/>

> [!NOTE]
>
> `requirements.txt` file listed as "dependencies" was created using `pip freeze > requirements.txt` command
>
> which was executed in active python `venv` prepared for this uni course.
> 
> Examine the file [here](../requirements.txt) and adjust it if needed.
>
> Check my tutorial on managing venvs [here](https://github.com/revalew/Python-Venv).

<br/>
<li> Prepare <code>README.md</code> file (customize this as you’d like) </li>
<br/>

<li> Prepare <code>LICENSE</code> file (MIT license shown below, more licenses can be found <a href="https://choosealicense.com/" target="_blank">here</a>)

<br/>
<br/>

```
Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</li>
<br/>

<li> Instal the build tool (if you encounter errors see <a href="https://packaging.python.org/en/latest/tutorials/installing-packages/" target="_blank">official tutorial</a>)

<br/>
<br/>

```bash
python3 -m pip install --upgrade build
```

</li>
<br/>

<li> Navigate to the folder where the <code>pyproject.toml</code> file is located </li>
<br/>

<li> Generate distribution archives

<br/>
<br/>

```bash
python3 -m build
```

</li>
<br/>

<li> Verify that the build was successful

<br/>

In the package there should now be `dist/` directory. The `tar.gz` file is a source distribution whereas the `.whl` file is a built distribution. Newer pip versions preferentially install built distributions, but will fall back to source distributions if needed. You should always upload a source distribution and provide built distributions for the platforms your project is compatible with.

<br/>

```bash
dist/
├── zaowr_polsl_kisiel-0.0.0-py3-none-any.whl
└── zaowr_polsl_kisiel-0.0.0.tar.gz
```

</li>

<br/>

<li> Register the account in <a href="https://test.pypi.org/account/register/">TestPyPI</a> or <a href="https://pypi.org/account/register/">PyPI</a> (just follow the given instructions)
</li>

<br/>

<li> Generate API token for <a href="https://test.pypi.org/manage/account/#api-tokens">TestPyPI</a> or <a href="https://pypi.org/manage/account/#api-tokens">PyPI</a> (just follow the given instructions, I added the credentials to <code>$HOME/.pypirc</code> using <code>[pypi]</code> and <code>[testpypi]</code> headers)
</li>

<br/>

<li> Instal <code>twine</code> to upload the package

<br/>
<br/>

```bash
python3 -m pip install --upgrade twine
```

</li>
<br/>

<li> Upload the package

<br/>

<ul>
<li>If you didn't add the credentials to <code>$HOME/.pypirc</code>, you will be prompted for username and password. Use <code>__token__</code> for username and <code>pypi-*</code> (your API token) for password

</li>

<br/>

<li> PyPI

<br/>
<br/>

```bash
python3 -m twine upload dist/*
```

</li>

<br/>

<li> TestPyPI

<br/>
<br/>

```bash
python3 -m twine upload --repository testpypi dist/*
```

</li>
</ul>
</li>

<br/>
<li> After the upload succeeded, the package should be vievable on <a href="https://pypi.org/project/zaowr-polsl-kisiel/" target="_blank">PyPI</a> or <a href="https://test.pypi.org/project/zaowr-polsl-kisiel/" target="_blank">TestPyPI</a>
</li>

<br/>
<li> Installing the package

<br/>

<ul>
<li> PyPI

<br/>
<br/>

```bash
python3 -m pip install --upgrade zaowr-polsl-kisiel
```

</li>

<br/>

<li> TestPyPI

<br/>
<br/>

```bash
python3 -m pip install --upgrade --index-url https://test.pypi.org/simple/ --no-deps zaowr-polsl-kisiel
```

</li>

<br/>

</ul>
</li>

> [!NOTE]
>
> Here we additionally use `--no-deps` flag.
>
> Since TestPyPI doesn’t have the same packages as the live PyPI, it’s possible that attempting to install dependencies may fail or install something unexpected.

<br/>

<li> Test the installation

<br/>

<ul>
<li> Activate the venv (while in the project directory) - <b>Skip this step if you are not using a virtual environment</b>

<br/>
<br/>

```bash
source ENV_NAME/bin/activate
```

or

```bash
. ENV_NAME/bin/activate
```

</li>

<br/>

<li> Launch python

<br/>
<br/>

```bash
python3
```

</li>

<br/>

<li> Import the package

<br/>
<br/>

```python
import zaowr_polsl_kisiel as zw
```

</li>
<br/>

<li> Locate the file with calibration params in tests folder and download it (link below)

<br/>
<br/>

[`../tests/misc/calibration_params/calibration_params.json`](../tests/misc/calibration_params/calibration_params.json)

</li>
<br/>

<li> Try reading the params from file

<br/>
<br/>

```python
# remember to provide appropriate path to the calibration params
calibrationParams = zw.load_calibration("/path/to/calibration_params.json")
```

</li>
<br/>

<li> Display the <code>MSE</code> value to test if the load succeeded (other keys should be suggested automatically)

<br/>
<br/>

```python
print(calibrationParams["mse"])
```

</li>

</ul>
</li>

</ol>

<br/>
<br/>

## Sources

This package has been prepared following [this tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

The publishing to PyPI was created with [this tutorial](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
