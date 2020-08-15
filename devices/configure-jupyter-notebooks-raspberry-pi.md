# Configure Jupyter Notebooks on a Raspberry Pi

[Jupyter notebooks](https://jupyter-notebook.readthedocs.io/en/stable/index.html) are interactive notebooks that mix code and documentation. They are often used by data scientists and AI developers running against powerful cloud-based machines.

They can also be run locally on a Raspberry Pi and provide a convenient way to run Python code.

## Install Jupyter notebooks

To install Jupyter notebooks, run the following code from the terminal:

```sh
sudo apt install python3-numpy python3-pandas python3-matplotlib --yes
sudo apt install jupyter-notebook --yes
```

## Run Jupyter notebooks

Jupyter notebooks run in the browser. To run them on the Pi, use the following command in the terminal:

```sh
jupyter notebook
```

The notebook server will start, and Chromium will launch running the Jupyter notebook app.

> The notebook server runs in the Terminal, so you will need to keep the terminal running whilst you use Jupyter notebooks.
