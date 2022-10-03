Introduction
============



.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/CedarGroveStudios/CircuitPython_PaletteFader/workflows/Build%20CI/badge.svg
    :target: https://github.com/CedarGroveStudios/CircuitPython_PaletteFader/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

A CircuitPython color palette and list brightness setter and normalizer tool.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install palettefader

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: py

    # For CircuitPython versions without ulab (such as the MatrixPortal)
    from cedargrove_palettefader.palettefader import PaletteFader

    # Instantiate PaletteFader
    faded_object = PaletteFader(source_palette=object_palette, brightness=0.5)

.. code-block:: py

    # For CircuitPython version with ulab
    from cedargrove_palettefader.palettefader_ulab import PaletteFader

    # Instantiate PaletteFader
    faded_object = PaletteFader(source_palette=object_palette, brightness=0.5)

``palettefader_simpletest.py`` and other examples can be found in the ``examples`` folder.

Documentation
=============
`PaletteFader API Class Description <https://github.com/CedarGroveStudios/CircuitPython_PaletteFader/blob/main/media/pseudo_readthedocs_palettefader.pdf>`_

.. image:: https://github.com/CedarGroveStudios/CircuitPython_PaletteFader/blob/main/media/PaletteFader_Class_description.jpeg

.. image:: https://github.com/CedarGroveStudios/CircuitPython_PaletteFader/blob/main/media/PaletteFader_Class_internals.jpeg


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/CedarGroveStudios/Cedargrove_CircuitPython_PaletteFader/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming to everyone.
