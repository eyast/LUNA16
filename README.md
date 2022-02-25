# The LUNA-16 Tutorial

Lung cancer is the leading cause of cancer-related death worldwide. Screening high risk individuals for lung cancer with low-dose CT scans is now being implemented in the United States and other countries are expected to follow soon. In CT lung cancer screening, many millions of CT scans will have to be analyzed, which is an enormous burden for radiologists. Therefore there is a lot of interest to develop computer algorithms to optimize screening.

The [LUNA 16 challenge](https://luna16.grand-challenge.org/) is an online challenge open to data-scientists in which participants build models that can detect nodules automatically on a dataset publicly available

## Approach

This tutorial will walk you through the typical workflow that you will be using to build a model for the LUNA 16 challenge.
This is the first of several tutorials. While I have tried to make the whole process as simple as I can, I have decided to maintain the iterative approach that is inherent to data science.
Data science is, by nature, very iterative.

> This repository is not perfect by any means. Instead, I am trying to document my journey and learning. For example, you will see at the very beginning stages of my work that I rely on Python's `multiprocessing` package to perform parallelism, but at a later stage transition to `dask`. I have not attempted to fix my earlier work, but instead keep it as it is. This way, I hope I will be able to embed the logic that I have followed throughout the project.

The approach that I take is to simply instructions as much as possible. Therefore, in many cases, I will be experimenting with new functions and ideas on a small scale (for example, a single file) before trying to find out how to automate this at a larger scale. I hope this can help you in your data science journey.

## Context and TOC

Broadly speaking, this tutorial will follow the iterative approach found in many data science projects. At a high level, this tutorial aims at:

1. Acquiring the data successfully.
2. Explore the files downloaded.
3. Explore the contents of the RAW data .
4. Explore the metadata downloaded.
5. Experiment with fitting different models to achieve the desired goal.

The Jupyter notebooks provided in this repository are listed in the order of the tasks you will probably perform as a data scientist. Each file represents a single task, and I recommend you follow these notebooks in order.

## The LUNA16 package

I have decided to create a package that includes utilities and several other functions that I am reusing throughout projects. You will therefore see references to custom utilities and functions that I have developed for this challenge, and I recommend you visit these utilities to understand their inner workings. This was also an experimentation for me to learn styling, typing, formatting and documenting of my code.

