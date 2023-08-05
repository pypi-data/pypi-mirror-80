# Colabext : Some Extended convenient utilities

## What is this about?  

This contains common style you can use for your notebook similar to Google CO-LABS

## How to use it

```
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user

pip install colabexts
```
and load this in your browser


## In your notebook

```
%reload_ext autoreload
%autoreload 2
import colabexts
from colabexts.jcommon import *

jpath=os.path.dirname(colabexts.__file__)
jcom = f'{jpath}/jcommon.ipynb'
%run $jcom

```


# Copyright 2013 Jonathan Miles

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0


Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
