# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_faucet_pipeline',
 'django_faucet_pipeline.templatetags',
 'django_faucet_pipeline.tests',
 'django_faucet_pipeline.tests.testapp']

package_data = \
{'': ['*'], 'django_faucet_pipeline.tests.testapp': ['templates/*']}

install_requires = \
['Django>=2.2']

setup_kwargs = {
    'name': 'django-faucet-pipeline',
    'version': '1.0.0b1',
    'description': 'A Django integration for faucet-pipeline',
    'long_description': '# Django Faucet Pipeline\n\n[![Build Status](https://dev.azure.com/glaux/update-broker/_apis/build/status/ngrewe.django-faucet-pipeline?repoName=ngrewe%2Fdjango-faucet-pipeline&branchName=main)](https://dev.azure.com/glaux/update-broker/_build/latest?definitionId=8&repoName=ngrewe%2Fdjango-faucet-pipeline&branchName=main)\n\ndjango-faucet-pipeline integrates [faucet-pipeline](https://www.faucet-pipeline.org) with Django. It allows you to\ntransparently reference assets created by faucet-pipeline in Django templates and operate on them using the [django.contrib.staticfiles](https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/) app.\n\n## Usage\n\n### Configuring Django and faucet-pipeline\n\nTo start using faucet-pipeline in Django, you need to make sure that both the staticfiles and the django_faucet_pipeline app are mentioned in the `INSTALLED_APPS` section of `settings.py`:\n\n```py\nINSTALLED_APPS = [\n    …,\n    \'django.contrib.staticfiles\',\n    \'django_faucet_pipeline\',\n]\n```\n\nfaucet-pipeline needs to be configured to write a `manifest.json` file for integrating with Django. By default,\ndjango-faucet-pipeline will look for this file in the `BASE_DIR` of the Django project (as specified\nby `settings.py`). You can customise the search path using `FAUCET_PIPELINE_MANIFEST` setting.\n\nThe manifest configuration needs to align with the Django configuration in two\nrespects: The `STATIC_URL` in settings by needs to be the same as the `baseURI` in the manifest config.\nAlso, all assets need to be output into the `webRoot`, which also needs to be configured as one of the\n`STATICFILES_DIRS` in Django. For example, if you were to have the following configuration in Django:\n\n```py\nBASE_DIR = Path(__file__).resolve().parent.parent\nSTATIC_URL = \'/static/\'\nSTATICFILES_DIRS = [\n    BASE_DIR / "dist/"\n]\n```\n\nA compatible `faucet.config.js` might look as follows:\n\n```js\nmodule.exports = {\n    js: {\n        input: \'app/index.js\',\n        output: \'dist/bundle.js\'\n    },\n    manifest: {\n        target: "./manifest.json",\n        key: "short",\n        baseURI: "/static/",\n        webRoot: "./dist"\n    }\n};\n```\n\ndjango-faucet-pipeline will emit an error message if it cannot read the manifest file, but it will not check\nwhether your webRoot and and `STATICFILES_DIRS` configuration is correct.\n\n### Referencing assets\n\nIn order to reference an asset, you simply use the `static_faucet` template tag from the `faucet_pipeline`\nlibrary. This behaves similarly to the "standard" `static` tag, but automatically expands the canonical name\nof the asset to the current (potentially fingerprinted) name.\n\n```html\n{% load static_faucet from faucet_pipeline %}\n<!doctype html>\n<html>\n  <head>\n    <meta charset="utf-8">\n    <title>Hello World</title>\n  </head>\n  <body> \n  <script src="{% static_faucet "bundle.js" %}" type="text/javascript"></script>\n  </body>\n</html>\n```\n\n### Debug vs. Production\n\nThe behaviour of django-faucet-pipeline will change depending on whether the Django settings `DEBUG` is set\nto true or not. If debug mode is enabled, the manifest file will be re-read when ever a template is rendered.\nIn production, you should have `DEBUG` set to `False`, in which case `manifest.json` will be read once on first\naccess and then cached indefinitely.\n',
    'author': 'Niels Grewe',
    'author_email': 'niels.grewe@halbordnung.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ngrewe/django-faucet-pipeline',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
