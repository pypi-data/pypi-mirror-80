![img](https://img.shields.io/gitlab/pipeline/ymd_h/b4tf.svg)
![img](https://img.shields.io/pypi/v/b4tf.svg)
![img](https://img.shields.io/pypi/l/b4tf.svg)
![img](https://img.shields.io/pypi/status/b4tf.svg)
[![img](https://gitlab.com/ymd_h/b4tf/badges/master/coverage.svg)](https://ymd_h.gitlab.io/b4tf/coverage/)


# Overview

b4tf is a Python module providing a set of bayesian neural network on
[TensorFlow](https://www.tensorflow.org/).


# Installation

b4tf requires following softwares before installation

-   TensorFlow 2.x
-   [TnesorFlow Probability](https://www.tensorflow.org/probability)
-   Python 3.x


## Install from [PyPI](https://pypi.org/) (Recommended)

The following command installs b4tf together with other dependancies.

    pip install b4tf

Depending on your environment, you might need `sudo` or `--user` flag
for installation.


## Install from source code

First, download source code manually or clone the repository;

    git clone https://gitlab.com/ymd_h/b4tf.git

Then you can install same way;

    cd b4tf
    pip install .


# Implemented Algorithms

Currently, b4tf implements following algorithms. We will implements
more.

-   Probabilistic Backpropagation (PBP) ([Paper](https://arxiv.org/abs/1502.05336))


# Lisence

b4tf is available under MIT lisence.

    MIT License
    
    Copyright (c) 2020 Yamada Hiroyuki
    
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

