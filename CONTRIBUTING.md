# Contributing to GNATSS Workshop

To contribute to the GNATSS Workshop, you must have [Pixi](https://pixi.sh) installed.

## Setting Up Your Environment

1. **Clone the Repository**: Start by cloning the GNATSS Workshop repository to your local machine.

   ```bash
   git clone https://github.com/seafloor-geodesy/gnatss-workshop.git
   ```

2. **Install Pixi Environment**: Ensure you have the Pixi environment set up. You can do this by running the following command in your terminal:

   ```bash
   pixi install --all
   ```

At this point, you should have all the necessary dependencies installed for the GNATSS Workshop.

## Contributing to the content

All of the content for the GNATSS Workshop is stored in the `docs` directory.
You can edit the content using your preferred text editor or IDE.
The technology we use to render the content is [Jupyter Book v2](https://next.jupyterbook.org) and you can add content in the form of [Myst Markdown](https://next.jupyterbook.org/tutorial/mystmd)
or [Jupyter Notebooks](https://mystmd.org/guide/quickstart-jupyter-lab-myst).

You can preview your changes locally by running the following command in the root of the repository:

```bash
pixi run -e site start
```

This will start a local jupyterbook server, and you can view the workshop at the url given in the terminal output, typically `http://localhost:3000`.
*This server will automatically reload when you make changes to the content*.

After you are satisfied with your changes, you can commit them,
and then create a pull request to the `main` branch of the repository.
This will allow [ReadtheDocs](https://readthedocs.org) to generate a preview of your changes.
