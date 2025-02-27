# ZAOWR Package - Windows Tutorial

<br/>

This is a **ZAOWR** (Zaawansowana Analiza Obrazu, Wideo i Ruchu, eng. _Advanced Image, Video, and Motion Analysis_) Python package used by me and my friends at the university.

<br/>

PyPI link to the package: <a href="https://pypi.org/project/zaowr-polsl-kisiel/" target="_blank"><b>MAIN PyPI</b></a>, <a href="https://test.pypi.org/project/zaowr-polsl-kisiel/" target="_blank"><b>TEST PyPI</b></a>.

<br/>
<br/>

## Code quality disclaimer

<div align="center">
  
<div style="font-size: 36px;" color="red">
It seems that the Optical Flow methods are not working on some Windows machines. I won't fix this. Use simple example code if you want to run this yourself - 

[../tests/misc/optical_flow/simple_flow_complete.py](./tests/misc/optical_flow/simple_flow_complete.py).

</div>
</div>
<br/><br/>

This package is not perfect. The code does everything it should, but that is the problem. It does everything...
Functions take too many arguments and offer too many options. Most functions are not broken up into smaller chunks - they are long and sometimes complicated. However, it’s worth noting that most of these options are not mandatory—you can use the package effectively without specifying all of them.

[//]: # (<div style="font-size: 22px; text-transform: uppercase; color: #ff0000;">)

<br/><br/>
<div align="center">
  
<div style="font-size: 22px;" color="red">
I made a genuine effort to balance flexibility with usability. If something feels unnecessarily complex, chances are it is — but with a little patience, you'll likely find a straightforward way to achieve your goal.

</div>

<sub><sub>
Take a look at solutions in <code>./tests/lab_exercise_solutions/</code> to understand how to use the package effectively (maybe). 
</sub></sub>

</div>

<br/>
<br/>

## Table of contents

1. [Linux tutorial](../README.md)

2. [RTFM - Use Cases for zaowr_polsl_kisiel and the importance of docstrings](#rtfm---use-cases-for-zaowr_polsl_kisiel-and-the-importance-of-docstrings)

3. [Installing the package on Windows using `pip`](#installing-the-package-on-windows-using-pip)

4. [Removing the package on Windows using `pip`](#removing-the-package-on-windows-using-pip)

5. [Installing extras (optional dependencies for the package - development)](#installing-extras-optional-dependencies-for-the-package---development)

6. [Creating virtual environment and installing the package](#creating-virtual-environment-and-installing-the-package)

7. [Testing the installation](#testing-the-installation)

8. [TODO for tracking issues / backlog / progress](./TODO.md)

9. [Code requirements](#code-requirements)

10. [Sources](#sources)

<br/>
<br/>

## Linux tutorial

The Linux tutorial can be found [here](../README.md)

<br/>
<br/>

## RTFM - Use Cases for zaowr_polsl_kisiel and the importance of docstrings

<ol>
<li>
<div style="font-size: 22px">

[RTFM v1 here](./USAGE.md) (custom-made explanations with examples)

</div>
</li>
<li>
<div style="font-size: 22px">

[RTFM v2 here (GitHub Pages)](https://revalew.github.io/zaowr-py-package) (auto-generated documentation with `pdoc`)

</div>
</li>
</ol>
<br/>

<br/>

> [!IMPORTANT]
> It is really important to understand how to use the package.
>
> The manual explains the use cases and tells you how to use docstrings.
>
> More examples (exact lab solutions) can be found [here](../tests/lab_exercise_solutions/)

<br/>
<br/>

## Installing the package on Windows using `pip`

<ol>

<li> PyPI MAIN

<br/>
<br/>

```cmd
py -m pip install --upgrade zaowr-polsl-kisiel
```

</li>
<br/>
<li> TestPyPI

<br/>
<br/>
 
```cmd
py -m pip install --index-url https://test.pypi.org/simple/ --upgrade zaowr-polsl-kisiel
```

</li>

</ol>

<br/>
<br/>

## Removing the package on Windows using `pip`

<br/>

```cmd
py -m pip uninstall zaowr-polsl-kisiel
```

<br/>
<br/>

## Installing extras (optional dependencies for the package - development)

```bash
py -m pip install --upgrade "zaowr-polsl-kisiel[dev]"
```

<br/>
<br/>

## Creating virtual environment and installing the package

<ol>
<li> Create project directory and open it (directory where you will create your files and where the venv will be created). Below is an example of how to do it through CMD - you can also do it through file explorer

<br/>
<br/>

```cmd
mkdir C:\path\to\project
```

```cmd
cd C:\path\to\project
```

<br/>

</li>
<li> Create venv

<br/>
<br/>

```cmd
py -m venv ENV_NAME
```

</li>

<li> Activate the venv (while in the project directory)

<br/>
<br/>

```cmd
ENV_NAME\Scripts\activate
```

</li>

<br/>

<li> Install the package from PyPI

<br/>
<br/>

```cmd
py -m pip install --upgrade zaowr-polsl-kisiel
```

</li>

<br/>

<li> <b>(ADDITIONAL COMMAND)</b> If you want to deactivate the currently active venv

<br/>
<br/>

```cmd
deactivate
```

</li>

<br/>

<li> <b>(ADDITIONAL COMMAND)</b> To reactivate the venv, navigate to the path where you created the venv and source it again

<br/>
<br/>

```cmd
ENV_NAME\Scripts\activate
```

</li>

</ol>

<br/>
<br/>

## Testing the installation

<br/>

<ul>
<li> Activate the venv (while in the project directory) - <b>Skip this step if you are not using a virtual environment</b>

<br/>
<br/>

```cmd
ENV_NAME\Scripts\activate
```

</li>

<br/>

<li> Launch python

<br/>
<br/>

```cmd
py
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
# remember to provide the appropriate path to the calibration params
calibrationParams = zw.load_calibration("C:\\path\\to\\calibration_params.json")
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

<br/>
<br/>

## Code requirements

The code fulfills all the requirements necessary to pass the course. Detailed descriptions of the requirements for each lab are provided in the [`./code_requirements/`](./code_requirements/) directory in the form of images (in Polish).

<br/>
<br/>

## Sources

This package has been prepared following [this tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

Workflow for publishing to PyPI was created with [this tutorial](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
