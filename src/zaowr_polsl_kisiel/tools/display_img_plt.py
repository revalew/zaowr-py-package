import os
import matplotlib.pyplot as plt
import numpy as np
from colorama import Fore, Style, init as colorama_init  # , Back

colorama_init(autoreset=True)

def display_img_plt(
        img: np.ndarray,
        pltLabel: str = 'Map',
        show: bool = False,
        save: bool = False,
        savePath: str = None
) -> None:
    """
    Display the image using matplotlib and optionally save it (single image).

    :param np.ndarray img: The image to be displayed
    :param str pltLabel: The label for the plot
    :param bool show: If True, show the plot
    :param bool save: If True, save the plot
    :param str savePath: The path to save the plot if `save` is True

    :raises TypeError: Raises TypeError if:
        - **`img`** is not a numpy array
        - **`pltLabel`** is not a string
        - **`show`** is not a boolean
        - **`save`** is not a boolean
        - **`savePath`** is not a string

    :return: None
    """
    if not isinstance(img, np.ndarray):
        raise TypeError(Fore.RED + "\nImage must be a numpy array!\n")

    if not isinstance(pltLabel, str):
        raise TypeError(Fore.RED + "\n`pltLabel` must be a string!\n")

    if not isinstance(show, bool):
        raise TypeError(Fore.RED + "\n`show` must be a boolean!\n")

    if not isinstance(save, bool):
        raise TypeError(Fore.RED + "\n`save` must be a boolean!\n")

    if savePath is None or not isinstance(savePath, str) or len(savePath) == 0:
        raise ValueError(Fore.RED + "\n`savePath` must be a non-empty string!\n")

    # Create the parent directory if it does not exist
    saveDir = os.path.dirname(savePath)
    # baseName = os.path.basename(savePath)
    if saveDir and not os.path.exists(saveDir):
        os.makedirs(saveDir)
        print(Fore.BLUE + f"Directory '{saveDir}' created.")

    # Create the plot
    plt.figure(figsize=(10, 8))
    plt.imshow(img, cmap='grey')
    plt.title(pltLabel)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    if save:
        if savePath is None or not isinstance(savePath, str) or len(savePath) == 0:
            raise TypeError(Fore.RED + "\n`savePath` must be provided if `saveComparison` is set to True\n")

        plt.savefig(savePath, format='png', bbox_inches='tight')
        print(Fore.GREEN + f"\nPlot successfully saved at {savePath}")

    if show:
        plt.show()

    plt.close()