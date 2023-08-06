# Beta-RecSys

Beta-RecSys an open source project for Building, Evaluating and Tuning Automated Recommender Systems.
Beta-RecSys aims to provide a practical data toolkit for building end-to-end recommendation systems in a standardized way.
It provided means for dataset preparation and splitting using common strategies, a generalized model engine for implementing recommender models using Pytorch with a lot of models available out-of-the-box,
as well as a unified training, validation, tuning and testing pipeline. Furthermore, Beta-RecSys is designed to be both modular and extensible, enabling new models to be quickly added to the framework.
It is deployable in a wide range of environments via pre-built docker containers and supports distributed parameter tuning using Ray.

Details of each folder in this repository are

- [beta_rec](beta_rec): data processing, model definition and utility functions
- [configs](configs): configurations of system information, data splitting and automatic hyper-parameter tuning
- [docs](docs): documentation for the Beta-RecSys system
- [examples](examples): practices of training various neural recommendation models
- [tests](tests): testing codes with the Pytest framework

For a more detailed overview of the repository, please see the documents at the [wiki page](https://beta-recsys.readthedocs.io/en/latest/).

## Install and Uninstall

Currently we are supporting Python 3 and PyTorch.

### Install Beta-RecSys using setup.py from github

1. Install Anaconda with Python >= 3.6. [Miniconda](https://conda.io/miniconda.html) is a quick way to get started.

2. Install and record the installed files

   ```
   $ git clone https://github.com/beta-team/beta-recsys.git
   $ cd $project_path$
   $ python setup.py install --record files.txt
   ```

### Uninstall Beta-RecSys completely

To uninstall the Beta-RecSys

```
$ cd $project_path$
$ xargs rm -rf < files.txt
```



## Get Started

1. To train a [Neural Graph Collaborative Filtering](https://arxiv.org/abs/1905.08108) with default configurations, you can run

```
python examples/train_ngcf.py
```

If you want to change training configurations, such as the used dataset and the range of hyper-paramters, you can change the [default NGCF configuration file](configs/ngcf_default.json) or create a new one.

2. To try new datasets, you can ceate a new dataset script in [beta-rec/datasets](beta_rec/datasets) by referring to how the [movielens](beta_rec/datasets/movielens.py) dataset is dealt with.
3. To define a new model,  you can ceate a new model script in [beta-rec/models](beta_rec/models) by referring to how the [NGCF](beta_rec/models/ngcf.py) model is defined.

**Note** - To conveniently check system information during model running, we implement funcnationlities of output logging and system monitoring in [beta-rec/utils](beta-rec/utils).

## Models

The following is a list of recommender models currently available in the repository.

- [MF](beta_rec/models/mf.py) is an implementation of Matrix Factorization
- [NCF](beta_rec/models/ncf.py) is an implementation of [Neural Collaborative Filtering](https://arxiv.org/abs/1708.05031).
- [NGCF](beta_rec/models/ngcf.py) is an implementation of [Neural Graph Collaborative Filtering](https://arxiv.org/abs/1905.08108).
- [Triple2Vec](beta_rec/models/triple2vec.py) is an implementation of [Representing and Recommending Shopping Baskets with Complementarity, Compatibility, and Loyalty](https://www.microsoft.com/en-us/research/uploads/prod/2019/01/cikm18_mwan.pdf).
- [VBCAR](beta_rec/models/vbcar.py) is an implementation of [Variational Bayesian Context-aware Representation for Grocery Recommendation](https://arxiv.org/abs/1909.07705).
- [LightGCN](beta_rec/models/lightgcn.py) is an implementation of [LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation](https://arxiv.org/abs/2002.02126).


## Contributing

This project welcomes contributions and suggestions. Please make sure to read the [Contributing Guide](https://beta-recsys.readthedocs.io/en/latest/contribute/standardization-of-code-format-and-documentation.html#) before creating a pull request. 

## Citation

If you use Beta-RecSys in you research, we would appreciate citations to the following paper:

- Zaiqiao Meng, Richard McCreadie, Craig Macdonald, Iadh Ounis, Shangsong Liang, Siwei Liu, Guangtao Zeng, Junhua Liang, Yucheng Liang, Qiang Zhang, Yaxiong Wu, Xi Wang. BETA-Rec: Build, Evaluate and Tune Automated Recommender Systems. RecSys 2020.

