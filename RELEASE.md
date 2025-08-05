# GNSS-A Data Analysis Workshop

**Release Date:** 2025-08-06

**Workshop Website**: [gnatss-workshop.readthedocs.io](https://gnatss-workshop.readthedocs.io)

## Overview

This release contains materials and resources for the GNSS-A Data Analysis Workshop, a short course developed as part of the Near-trench Community Geodetic Experiment (supported by the National Science Foundation). The workshop provides a comprehensive introduction to analyzing Global Navigation Satellite Systems - Acoustic (GNSS-A) data using the GNATSS open-source software package.

## What's Included

### Workshop Materials

- **Instructional Content:** Step-by-step tutorials for GNSS-A data processing
- **Software Package:** GNATSS installation files and dependencies
- **Sample Datasets:** Representative GNSS-A data for hands-on exercises
- **Exercises:** Practical assignments covering seafloor horizontal positioning workflows

### Learning Objectives

Building strong understanding of GNSS-Acoustics for precise point positioning with a focus on the newly collected data associated with the Community Experiment, including:

- Deployment strategies
- Instrument operations
- Data collection and standards
- Data access
- Processing data using the new GNATSS software

Network with other researchers who share common interests

## System Requirements

### Software Dependencies

- Operating System: Linux, macOS
- Software: [pixi](https://pixi.sh/latest/) (v0.48.0 or later)

### Hardware Recommendations

- Memory: Minimum 16 GB RAM
- Disk Space: Minimum 10 GB free space

## Installation Instructions

### Quick Start

The quickest way to get started without manual installation is to use
[GitHub Codespaces](https://github.com/features/codespaces) - "a development environment that's hosted in the cloud". This allows you to run the workshop exercises directly in your browser without needing to set up a local environment.
In order to access the Codespace, you need to register an account with [GitHub](github.com)

[Launch GitHub Codespaces](https://codespaces.new/seafloor-geodesy/gnatss-workshop?quickstart=1)

☝️ Click the link above to go to options window to launch a GitHub Codespace.

## List of Exercises

All exercises can be found in the `docs` directory of this repository. Each exercise is designed to build on the previous one, gradually increasing in complexity and depth of understanding.

Exercise 1: Introduction to GNATSS

Exercise 2: Travel Time Residuals and Residual Flagging

Exercise 3: GNSS-Acoustic Metadata

Exercise 4: GNSS-Acoustic Velocity Calculation

## Data and Examples

### Current Datasets

The current datasets used in the workshop are available
as part of the [release assets](https://github.com/seafloor-geodesy/gnatss-workshop/releases) from latest release named `data.zip`.

## Additional Resources

### External Documentation

- [GNATSS Documentation](https://gnatss.readthedocs.io)

### Support and Community

- **Bug Reports:** If you encounter issues, please open an issue on the [GNATSS Workshop Repository](https://github.com/seafloor-geodesy/gnatss-workshop/issues/new/choose).

## Acknowledgments

This workshop was developed as part of the Near-trench Community Geodetic Experiment, with support from the National Science Foundation. We also thank UW eScience Scientific Software Engineering Center for their contributions to setting up the infrastructure and resources for this workshop.

## License

This workshop content is released under the [BSD 3-Clause License](https://github.com/seafloor-geodesy/gnatss-workshop/blob/main/LICENSE). You are free to use, modify, and distribute the materials as long as you adhere to the license terms.
