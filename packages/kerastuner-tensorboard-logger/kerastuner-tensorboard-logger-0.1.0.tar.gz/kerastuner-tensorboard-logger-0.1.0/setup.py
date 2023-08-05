# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kerastuner_tensorboard_logger']

package_data = \
{'': ['*']}

install_requires = \
['keras-tuner>=1.0,<2.0', 'tensorflow>=2.0,<3.0']

setup_kwargs = {
    'name': 'kerastuner-tensorboard-logger',
    'version': '0.1.0',
    'description': 'Simple integration of keras-tuner (hyperparameter tuning) and tensorboard dashboard (interactive visualization).',
    'long_description': '# Keras-tuner Tensorboard logger\n\n![](https://github.com/tokusumi/kerastuner-tensorboard-logger/workflows/Tests/badge.svg)\n\nkeras-tuner logger for streaming search report to Tensorboard plugins Hparams, beautiful interactive visualization tool.\n\n## Requirements\n\n* Python 3.6+\n* keras-tuner 1.0.0+\n* Tensorboard 2.1+\n\n## Example\n\nsimple and incomplete code is introduced.\n\nSee details about how to use keras-tuner in [here](https://github.com/keras-team/keras-tuner).\n\nAdd only one argument in tuner class and search it, then you can go to see search report in Tensorboard.\n\n```python\n# import this\nfrom kerastuner_tensorboard_logger import TensorBoardLogger\n\ntuner = Hyperband(\n    build_model,\n    objective="val_acc",\n    max_epochs=5,\n    directory="logs/tuner",\n    project_name="tf_test",\n    logger=TensorBoardLogger(\n        metrics=["val_acc"], logdir="logs/hparams"\n    ),  # add only this argument\n)\n\ntuner.search(x, y, epochs=5, validation_data=(val_x, val_y))\n```\n\n### Tensorboard\n\n```bash\n$ tensorboard --logdir ./logs/hparams\n```\n\nGo to http://127.0.0.1:6006.\n\nYou will see the interactive visualization (provided by Tensorboard).\n\n![Table View](https://raw.githubusercontent.com/tokusumi/kerastuner-tensorboard-logger/main/docs/src/table_view.jpg)\n\n![Parallel Coordinates View](https://raw.githubusercontent.com/tokusumi/kerastuner-tensorboard-logger/main/docs/src/parallel_coordinates_view.jpg)\n',
    'author': 'tokusumi',
    'author_email': 'tksmtoms@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tokusumi/kerastuner-tensorboard-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
