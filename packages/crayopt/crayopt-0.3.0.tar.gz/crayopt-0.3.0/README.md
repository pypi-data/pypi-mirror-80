# CrayNN

Yet Another toolkit for Neural Network slightly flavoured by Ultra-High Energy Cosmic Rays. 

## Philosophy

`CrayNN` is highly influenced by [Lasange](https://github.com/Lasagne/Lasagne):

> 
    Simplicity: Be easy to use, easy to understand and easy to extend, to facilitate use in research
    Transparency: Do not hide Theano behind abstractions, directly process and return Theano expressions or Python / numpy data types
    Modularity: Allow all parts (layers, regularizers, optimizers, ...) to be used independently of Lasagne
    Pragmatism: Make common use cases easy, do not overrate uncommon cases
    Restraint: Do not obstruct users with features they decide not to use
    Focus: "Do one thing and do it well"

Just replace `theano` with `tensorflow`.

## Installation

### via PyPi

`pip install craynn`

### via git

`CrayNN` can be installed directly from `gitlab.com`:
`pip install git+https://gitlab.com/craynn/craynn.git`
however, as repository updates quite often, it is recommend to clone the repository
and install the package in development mode:
```
git clone git@gitlab.com:craynn/craynn.git
cd craynn/
pip install -e .
```

## Usage

Check out jupyter notebooks in `examples/`.