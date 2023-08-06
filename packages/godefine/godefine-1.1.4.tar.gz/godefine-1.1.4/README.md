# Godefine

replace marco in template,and generate output

## License

![license](https://img.shields.io/badge/license-MIT-brightgreen.svg)


## FIRST: THIS SCRIPT BASED ON PYTHON3!

## Install Guide

```bash
pip3 install -U godefine
```

to get latest version from `pypi`,you should add `--isolated` on command-line

## ThirdPart Modules

|Module|IsRequired?|
|---|--- |
|wcwidth|❗|
|tabulate|✅|

although `wcwidth` is optional, but it's higly recommended to install.

`wcwidth` help `tabulate` handle pagecode issue.



## Get Start


we have a template file such as **"sample.go.template"**

it's contains code like:

```go
const Foo =  ${foo} // foo??? no idea @default="simple";
const Bar =  ${bar} // some bar...whatever @default=1231;
```

run script:

```bash
godefine.py -t sample.go.template -o sample.go 
```

sample.go:

```go
const Foo =  "simple" // foo??? no idea @default="simple";
const Bar =  1231 // some bar...whatever @default=1231;
```

## Script Syntax

### default:

`godefine` will replace '${something}' with the value user provide.

if var's value not specified, `godefine` will look for the `default value` 
in the comment after `//`

default value should apply syntax as follows : '@default=your value;'

### include:

like `#include <cstdio>` we often used in Cpp language`.

you can use `@include()` to put an exist config file into current config file.

for example:

we have `foo/bar/base.in` and `foo/someone_debug.in` 

foo/bar/base.in:

```ini
foo=bar
bar=foo
```

foo/someone_debug.in:

```ini
@include(bar/base.in)
name=someone
foo=override bar
```

`godefine` will see vars below:

```ini
bar=foo
name=someone
foo=override bar
```

godefine support both `relative`  and `absolute` path

## Advance

### pass vars from command-line (Simple, but `not suggest` :bangbang:)

pass your custom vars after `-v` option


```bash
godefine.py -v foo=11 bar=222 -t sample.go.template -o sample.go 
```

this way is not suggested.
if your value have such special char eg: `blank str`,`"`, 
it's hard to handle with it.

### use vars form specified file (Suggest :smirk: :thumbsup:)

define your vars in `config.in`

```ini
foo="abc 112 333"
bar=    bar
web site=https://www.google.com
handsome author=ooopSnake 🎉

```

template file `env.go.template`:

```go
package env

const Foo =  "abc 112 333" // foo??? @default="中文~";
var Website = "https://www.google.com" // homepage
const Bar = "    bar" // barss
var Author =  ooopSnake 🎉 // author name @default=snake!;

```

run `godefine`

```bash
godefine.py -i config.in -t env.go.template -o env.go 
```

output `env.go`:

```go
package env

const Foo =  "abc 112 333" // foo??? @default="中文~";
var Website = "https://www.google.com" // homepage
const Bar = "    bar" // barss
var Author =  "ooopSnake 🎉" // author name @default=snake!;
```

as you can see ,foo's value has some `space(blank)` char.

`godefine` script will handle them correctly.


### override vars in config


godefine always override that vars if they have been defined previously.

for example:
if var below  `@include` declare, vars will override vars that defined in `@include`
 
if var above `@include` declare,
`@include` defined vars will override vars that pervious defined.


### error handling :interrobang:

if you forgot to assign any one vars ,an error will be raised.

anyway, you still want to generate output, `-f` will be useful.

if `-f` applied, any error will be ignored,
the var who not assigned with value,will keep itself original state 
.
