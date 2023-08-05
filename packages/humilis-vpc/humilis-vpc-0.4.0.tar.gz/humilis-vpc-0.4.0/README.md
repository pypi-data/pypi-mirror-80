Humilis plug-in to deploy a VPC
===================================================

[![PyPI](https://img.shields.io/pypi/v/humilis-vpc.svg?style=flat)](https://pypi.python.org/pypi/humilis-vpc)

A [humilis][humilis] plug-in layer that deploys a [VPC][vpc].

[vpc]: https://aws.amazon.com/vpc/
[humilis]: https://github.com/humilis/humilis


## Installation


```
pip install humilis-vpc
```


To install the development version:

```
pip install git+https://github.com/humilis/humilis-vpc
```


## Development

Assuming you have [virtualenv][venv] installed:

[venv]: https://virtualenv.readthedocs.org/en/latest/

```
make develop
```

Configure humilis:

```
make configure
```


## Testing

You can test the deployment of a VPC with:

```
make test
```

The test suite should destroy the deployed VPC automatically, but you 
can make sure you are not leaving any infrastructure behind by manually 
running:

```bash
make delete
```


## More information

See [humilis][humilis] documentation.


## Contact

If you have questions, bug reports, suggestions, etc. please create an issue on
the [GitHub project page][github].

[github]: http://github.com/humilis/humilis-vpc


## License

This software is licensed under the [MIT license][mit].

[mit]: http://en.wikipedia.org/wiki/MIT_License

See [License file][LICENSE].

[LICENSE]: https://github.com/humilis/humilis-vpc/blob/master/LICENSE.txt


© 2017 German Gomez-Herrero, [Find Hotel][fh].

[fh]: http://company.findhotel.net
