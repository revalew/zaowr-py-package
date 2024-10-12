# ZAOWR Package

<br/>

This is a **ZAOWR** (Zaawansowana Analiza Obrazu, Wideo i Ruchu, eng. _Advanced Image, Video, and Motion Analysis_) Python package used by me and a friend at the university.

PyPI link to the package

<ul>
<li><a href="https://pypi.org/project/zaowr-polsl-kisiel/" target="_blank">MAIN PyPI</a></li>
<br/>
<li><a href="https://test.pypi.org/project/zaowr-polsl-kisiel/" target="_blank">TEST PyPI</a></li>
</ul>

<br/>
<br/>

## Installing the package using `pip`

<ol>

<li> PyPI MAIN

<br/>

<ul>

<li> Linux

<br/>

```bash
python3 -m pip install --upgrade zaowr-polsl-kisiel
```

</li>
<br/>
<li> Windows

<br/>

```bash
py -m pip install --upgrade zaowr-polsl-kisiel
```

</li>
</ul>
</li>
<br/>
<li> TestPyPI

<br/>

<ul>

<li> Linux

<br/>

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --upgrade zaowr-polsl-kisiel
```

</li>
<br/>
<li> Windows

<br/>

```bash
py -m pip install --index-url https://test.pypi.org/simple/ --upgrade zaowr-polsl-kisiel
```

</li>
</ul>
</li>
</ol>

<br/>
<br/>

## Removing the package using `pip`

<br/>

```bash
python3 -m pip uninstall zaowr-polsl-kisiel
```

<br/>
<br/>

## Creating virtual environment and installing the package

<br/>

> [!NOTE]
>
> Complete instructions on managing Python virtual environments
>
> can be found [here](https://github.com/revalew/Python-Venv).

<br/>
<ol>
<li> Create project directory and open it (directory where you will create your files and where the venv will be created)

<br/>

```bash
testDir=/home/user/test
```

```bash
mkdir -p $testDir
```

```bash
cd $testDir
```

<br/>

</li>
<li> Create venv

<br/>

```bash
python -m venv ENV_NAME
```

</li>
<br/>

> [!NOTE]
>
> `ENV_NAME` is the name of your venv, so you can change it however you like

<br/>

<li> Activate the venv (while in the project directory)

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

<li> Install the package from PyPI

<br/>

```bash
python3 -m pip install --upgrade zaowr-polsl-kisiel
```

</li>

<br/>

<li> <b>(ADDITIONAL COMMAND)</b> If you want to deactivate the currently active venv

<br/>

```bash
deactivate
```

</li>

<br/>

<li> <b>(ADDITIONAL COMMAND)</b> To reactivate the venv, navigate to the path where you created the venv and source it again (command shown above in section number 3)
</li>

</ol>

<br/>
<br/>

## Automate building and uploading with `Makefile` - DEV Tutorial

In the project directory run <code>make</code>. This command will run the <code>Makefile</code>, which performs actions listed below:

<ul>
<li>remove old version of the package,</li>
<li>ask which version we want to update (major, minor, patch) and increment it automatically, <code>push</code> the changes to GitHub with new tag,</li>
<li>build a new version,</li>
<li>upload the package to PyPI,</li>
<li>upload the package to TestPyPI.</li>
</ul>

<br/>

<ol>
<li> Test the <code>Makefile</code>

<br/>

```bash
make --dry-run
```

</li>

<br/>

<li> Run the <code>Makefile</code>

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

<li> Install pip

<br/>

```bash
python3 -m pip install --upgrade pip
```

</li>
<br/>

<li> Prepare files and directories

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

```bash
python3 -m pip install --upgrade setuptools
```

</li>
<br/>

<li> Prepare <code>pyproject.toml</code> file (this package's configuration as an example)

<br/>

```bash
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "zaowr_polsl_kisiel"
dynamic = ["version", "dependencies"]
authors = [
  { name="Maksymilian Kisiel" },
]
description = "A simple Python package used by me and a friend at the university in the course 'Advanced Image, Video and Motion Analysis'"
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
keywords = ["polsl", "zaowr", "2024", "IGT", "ZAOWR"]

[tool.setuptools.dynamic]
version = {attr = "zaowr_polsl_kisiel.__version__"}  # any module attribute compatible with ast.literal_eval
dependencies = {file = ["requirements.txt"]}

[project.urls]
Homepage = "https://github.com/revalew/zaowr-py-package"
Issues = "https://github.com/revalew/zaowr-py-package/issues"
```

</li>
<br/>

> [!NOTE]
>
> `requirements.txt` file listed as "dependencies" was created using `pip freeze > requirements.txt` command
>
> which was executed in active python `venv` prepared for this uni course.
>
> Check my tutorial on managing venvs [here](https://github.com/revalew/Python-Venv).

<br/>
<li> Prepare <code>README.md</code> file (customize this as you’d like) </li>
<br/>

<li> Prepare <code>LICENSE</code> file (MIT license shown below, more licenses can be found <a href="https://choosealicense.com/" target="_blank">here</a>)

<br/>

```bash
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

```bash
python3 -m pip install --upgrade build
```

</li>
<br/>

<li> Navigate to the folder where the <code>pyproject.toml</code> file is located </li>
<br/>

<li> Generate distribution archives

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

```bash
python3 -m twine upload dist/*
```

</li>

<br/>

<li> TestPyPI

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

```bash
python3 -m pip install --upgrade zaowr-polsl-kisiel
```

</li>

<br/>

<li> TestPyPI

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

```bash
python3
```

</li>

<br/>

<li> Import the package

<br/>

```python
from zaowr_polsl_kisiel import load_calibration
```

</li>
<br/>

<li> Locate the file with calibration params or create new file with structure shown below

<br/>

```json
{
	"mse": 5.984166144997382,
	"rms": 0.5399844606283781,
	"cameraMatrix": [
		[1272.011234078766, 0.0, 1058.4537673810164],
		[0.0, 1266.8726860857762, 617.7592332273604],
		[0.0, 0.0, 1.0]
	],
	"distortionCoefficients": [
		[-0.39935647747478337, 0.18200290247627665, 0.0020154085712910707, -0.012190829753206725, -0.04648398598417859]
	],
	"rotationVectors": [
		[[0.014376302442723948], [0.1667778841470017], [0.018832348485715023]],
		[[-0.3405035725192283], [0.526867552280327], [-0.13373157952652456]]
	],
	"translationVectors": [
		[[71.27846898868391], [50.76036240921024], [1400.9402673825555]],
		[[-476.2081267995082], [-120.35757569213392], [803.862414335442]]
	]
}
```

</li>
<br/>

<li> Try reading the params from file

<br/>

```python
# remember to provide appropriate path to the calibration params
# you can simply create a json file with structure shown above
calibrationParams = load_calibration("../../tests/calibration_params/calibration_params.json")
```

</li>
<br/>

<li> Display the <code>MSE</code> value to test if the load succeeded

<br/>

```python
print(calibrationParams["mse"])
```

</li>
</li>

</ol>

<br/>
<br/>

## Sources

This package has been prepared following [this tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/).
