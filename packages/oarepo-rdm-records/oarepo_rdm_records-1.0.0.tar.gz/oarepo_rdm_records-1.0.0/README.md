OARepo rdm records model
====================
[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]

Instalation
----------
```bash
    pip install oarepo-rdm-records
```
Usage
-----
The library provides modified Invenio rdm records data model for OARepo. 

Modified fields of data model
-----------------------------
##### titles
- fully required oarepo multilingual data type
##### descriptions
- fully optional oarepo multilingual data type
##### subjects
- ```subject``` is required oarepo multilingual data type
##### locations
- ```description``` is optional oarepo multilingual data type
##### licenses
- ```license``` is required oarepo multilingual data type

 [image]: https://img.shields.io/travis/oarepo-rdm-records/oarepo-rdm-records.svg
  [1]: https://travis-ci.org/oarepo-rdm-records/oarepo-rdm-records
  [2]: https://img.shields.io/coveralls/oarepo-rdm-records/oarepo-rdm-records.svg
  [3]: https://coveralls.io/r/oarepo-rdm-records/oarepo-rdm-records
  [4]: https://img.shields.io/github/license/oarepo-rdm-records/oarepo-rdm-records.svg
  [5]: https://github.com/oarepo-rdm-records/oarepo-rdm-records/blob/master/LICENSE
  [6]: https://img.shields.io/pypi/v/oarepo-rdm-records.svg
  [7]: https://pypi.org/pypi/oarepo-rdm-records