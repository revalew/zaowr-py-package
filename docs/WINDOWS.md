# ZAOWR Package - Windows Tutorial

This is a **ZAOWR** (Zaawansowana Analiza Obrazu, Wideo i Ruchu, eng. _Advanced Image, Video, and Motion Analysis_) Python package used by me and a friend at the university.

PyPI link to the package: [MAIN PyPI](https://pypi.org/project/zaowr-polsl-kisiel/), [TEST PyPI](https://test.pypi.org/project/zaowr-polsl-kisiel/).

<br/>
<br/>

## Table of contents

1. [Linux tutorial](../README.md)

2. [Installing the package on Windows using `pip`](#installing-the-package-on-windows-using-pip)

3. [Removing the package on Windows using `pip`](#removing-the-package-on-windows-using-pip)

4. [Creating virtual environment and installing the package](#creating-virtual-environment-and-installing-the-package)

5. [Testing the installation](#testing-the-installation)

6. [TODO for tracking issues / backlog / progress](./TODO.md)

7. [Code requirements](#code-requirements)

8. [Sources](#sources)

<br/>
<br/>

## Linux tutorial

The Linux tutorial can be found [here](../README.md)

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
from zaowr_polsl_kisiel import load_calibration
```

</li>
<br/>

<li> Locate the file with calibration params or create new file with structure shown below

<br/>
<br/>

```json
{
    "mse": 5.984166144997382,
    "rms": 0.5399844606283781,
    "objPoints": [
        [1272.011234078766, 0.0, 1058.4537673810164],
        [0.0, 1266.8726860857762, 617.7592332273604],
        [0.0, 0.0, 1.0]
    ],
    "imgPoints": [
        [1272.011234078766, 0.0, 1058.4537673810164],
        [0.0, 1266.8726860857762, 617.7592332273604],
        [0.0, 0.0, 1.0]
    ],
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
<br/>

```python
# remember to provide the appropriate path to the calibration params
# you can simply create a json file with the structure shown above
calibrationParams = load_calibration("C:\\path\\to\\calibration_params.json")
```

</li>
<br/>

<li> Display the <code>MSE</code> value to test if the load succeeded

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

This package has been prepared following [this tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

The publishing to PyPI was created with [this tutorial](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/).
```