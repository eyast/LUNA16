# The LUNA-16 Tutorial

Lung cancer is one of the leading causes of cancer-related death worldwide. Screening high risk individuals for lung cancer with low-dose CT scans is now being implemented in the United States and other countries are expected to follow soon. In CT lung cancer screening, many millions of CT scans will have to be analyzed, which is an enormous burden for radiologists. Therefore there is a lot of interest to develop computer algorithms to optimize screening.

The [LUNA 16 challenge](https://luna16.grand-challenge.org/) is an online challenge open to data-scientists in which participants build models that can detect nodules automatically on a dataset publicly available. The challenge is extremely interesting to tackle for multiple reasons (beyond the impact a model might have to humanity, of course).

Personally, the challenge that I have been facing has been related to building a portfolio. I have been explaining to peers and potential hiring managers how my curious and inquisitive mind allows me to tackle machine learning problems exhaustively, but i have never had anything to show for it. I've therefore decided to apply myself solving this challenge, and I have documented my ever steps and published them in this repo.

## Motivation: Having a portfolio

How do you get a job in data science? This has been my objective for few years and I have discovered that knowing enough statistics, machine learning, programming, etc is all necessary, but not a sufficient one to demonstrate my ability to tackle different data science problems. I have been spending a tremendous amount of time reading and consuming self-paced training (Coursera, Leetcode, Datacamp, and the like) in hope to increase my chancesof getting my dream job.
I have had the opportunity to participate in few interviews lately but never had the chance to demonstrate I have the required skills for the job.

While there have been a tremendous quantity of posts on Medium explaining the importance of building an interesting data science portfolio, I have decided to diverge from the common recommendation and instead build a portfolio of notebooks in which I explain how to tackle a data science project, from envisioning to validation. Explaining the concepts that I am learning is the most powerful method to communicate my reasoning and will also serve as a way to get (hopefully) external validation. I'd love to know if i'm on the right track or not, and I invite you to submit issues if you would like to see more content (or a Pull Request, if you believe you can do a better job).

My purpose is not to show you a working model, nor is it to hide away from you the iterative approach that I am employing. I will not be prebaking anything and I will not assume anything from your part, except that you know how to use Python/Pytorch and that you are curious. The Level of Detail I will provide will be based on my level of interest - which means that I will not dig deep into the low level data structures or operations, unless I feel interested to do so for some practice related to the project at hand.

## Approach

This tutorial will walk you through the typical workflow that you will be using to build a model for the LUNA 16 challenge, or at least the one i have followed - I then decided to document my journey as a tutorial. Think of it as a way for you to follow along a data science challenge: instead of observing the final result, you are being presented with logical steps to take, each in its own Jupyter notebook, each building a little bit on top of the previous ones, but some leading no where: some ideas turn out to be either incorrect, or non-beneficial. In the spirit of traceability, I have opted to keep all the notebooks that were non conclusive to our task.

This is the first of several tutorials. While I have tried to make the whole process as simple as I can, I have decided to maintain the iterative approach that is inherent to data science.

> This repository is not perfect by any means. Instead, I am trying to document my journey and learning. For example, you will see at the very beginning stages of my work that I rely on Python's `multiprocessing` package to perform parallelism, but at a later stage transition to `dask`. I have not attempted to fix my earlier work, but instead keep it as it is. This way, I hope I will be able to embed the logic that I have followed throughout the project.

The approach that I take is to simply instructions as much as possible. Therefore, in many cases, I will be experimenting with new functions and ideas on a small scale (for example, a single file) before trying to find out how to automate this at a larger scale. I hope this can help you in your data science journey.

## Linearity of notebooks: Questions are as important as their answers

As a data scientist, you will ask several questions about your data, some of which are initial (before the task even starts) such as objective, purpose, etc... and others as you progress and discover more about what you are dealing with. I will not try to preempt any of those questions. In other words, you will see these questions and answers progressing chronologically the same way i have had them.
Each Jupyter notebook is concluded with a section called "Our journey so far". This section includes two views:

- What are the open questions we have been asking so far.
- What are the questions we've answered so far.

Progressing through the notebooks should help you understand my methodology, but it is equally important for you to wonder if there are questions i have missed, and if so - do they need their own notebooks?

## Context and TOC

Broadly speaking, this tutorial will follow the iterative approach found in many data science projects. At a high level, this tutorial aims at:

1. [Acquiring the data successfully.](00%20-%20Downloading%20files.ipynb), in which:
   - I will show you where to get the files from and why `multiprocessing` is fantastic.
   - Feel free to skip this if you're not interested in any of these topics.
   > We will not analyze the contents of the file in this notebook. By the end of this notebook, you will have a script that downloads and unzips the files. This script can run interactively from the console, or from within a pipeline.
2. [Explore the files downloaded.](01%20-%20Understanding%20files%20and%20folders%20EDA.ipynb), in which we will try to answer:
    - What have we downloaded, exactly? How many files are there, what are their extensions, what do they include?
3. [Explore the contents of the MHD files - part 1](02%20-%20Exploring%20MHD%20files%20-%20part%201.ipynb), in which:
    - We will learn a little bit about the `SimpleITK` library, and how to access a single randomly selected .MHD file.
    - We attempt visualizing the array in the randomly selected .MHD file.
    - We explore the contents of the randomly selected MHD file, and visualize the distribution of values on a histogram.
    - We learn that our MHD files contain arrays of shape C, H, W (Channel, Heigh, and Width). We count the number of Channels in each and every CT scan.
4. [Dask basics](03%20-%20Dask%20basics.ipynb). At this stage, it became apparent to me that I can not perform Exploratory Data Analysis (EDA) on all the CT scans the way I usually do (using `numpy`) due to the fact that these files are *massive* and it is impossible to load them all in memory.
   - To overcome this (and future) challenges, I explore the popular `dask` library. There is (almost) no learning curve if you know a bit of numpy.
   - I show the structure of `dask` operations on a single file. This acts as a unit test to validate my approach.
   - Feel free to skip this notebook if you are already familiar with `dask`.
5. [Explore the contents of the MHD files - part 2](04%20-%20Exploring%20MHD%20files%20-%20part%202.ipynb), which builds on the work we've done previously. This time, instead of handling a single random MHD file, we will load all the CT scans in memory and perform more analysis of them (as a whole). We will
   - Learn how to load all the CT scans in memory using dask's advanced Directed Acyclic Graph approach.
   - Compute descriptive statistics (find minimum, maximum values) and try to determine the boundary by which we will deem certain points to be outliers.
6. [Explore the contents of MHD files - part 3](05%20-%20Exploring%20MHD%20files%20-%20part%203.ipynb). In the final installment of file exploration, we build on what we have discovered so far. We will perform a single step in this notebook, which is the projection of 'the outlier values' of all 3D CT scans, into a single 2D plane. While this step is not necessary, it was simply something i was wondering about through my journey.
7. [Find out if we are using the correct data type](06%20-%20is%20float32%20the%20right%20datatype.ipynb). Up until now, all the array information that's been loaded has been `np.float32` to make sure i don't cause mistakes. But this data type will consume twice the size of `np.float16`, and unless it is storing detailed values that will be needed later on, it is useless. In this notebook, I will attempt at discovering if the array data retrieved from `SimpleITK` can be stored in a 16 bit floating point value or not, without losing any precision to the data).
8. [Visualize a CT scan, in 3D](07%20-%20Visualizing%201%20CT%20scan.ipynb). I don't think this step is necessary at all, but i am very curious to see a CT scan in 3D

The Jupyter notebooks provided in this repository are listed in the order of the tasks you will probably perform as a data scientist. Each file represents a single task, and I recommend you follow these notebooks in order.

## The LUNA16 package

I have decided to create a package that includes utilities and several other functions that I am reusing throughout projects. You will therefore see references to custom utilities and functions that I have developed for this challenge, and I recommend you visit these utilities to understand their inner workings. This was also an experimentation for me to learn styling, typing, formatting and documenting of my code.
