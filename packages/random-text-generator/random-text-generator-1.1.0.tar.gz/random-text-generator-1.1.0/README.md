# <div align=center><span>About this repository<img align="right" width=100 height=100 src=https://logos-download.com/wp-content/uploads/2016/10/Python_logo_icon.png></span></div>

## Simple Code Generator

---

### Description

> **Generate string codes for django or flask or any web development python framework or any python project generally**

---

> **Use this script as an extension of your project whenever you want to generate random codes.**

### Usage

---

**Follow the following: !**
**They are very important**

```txt
1. call the function generate()

2. pass in the arguments, they are: [
        'length_minimal', 'length_maximal', 'int_min_length',
        'int_max_length'
    ], they are optional and the default values will be given to them. So the
        output will be like

   generate_code_simple(length_minimal=int, length_maximal=int,
                        int_min_length=int, int_max_length=int).

3. then leave the rest to the packge to generate the type of code for you

4. then make a variable like the example
   `code = generate_code_simple()` | don't add the the symbol `|` just write the
   what is inside the variables backticks.

5. then at runtime the generated code will be run

```

**This written in python code**

**Obviously use the statement `from text_generator import generate` for the 1st line**

---

<br>

**Code without parameters**

```python
code = generate()
print(f"Generated code is -> {code}")
```

```text
>>> Generated code is -> 552405550765069469025

The result is not fixed it changes at the next runtime
```

---

**Code with parameters**

```python
code = generate(length_minimal=10, length_maximal=50,
                             int_min_length=1, int_max_length=99999)
print(f"Generated code is -> {code}")
```

```text
>>> Generated code is -> 6051772282112626082611874181

? Don't rely on this code is not yet fully tested and results may differ.
Working on it
```

---

## Configuration

---

**To configure the project all you need to do is pass in `params` to the `generate()` function**

## Changelog

[CHANGELOG](CHANGELOG.md)

## Authors

[AUTHORS](AUTHORS.md)

## Contributing

[CONTRIBUTING](CONTRIBUTING.md)

## Folder Structure Structure

---

<pre>
<code>
DIR  +----------------------|> dist
DIR  +----------------------|> tests
DIR  +----------------------|> text_generator
FILE  +----------------------|> __init.py__
FILE  +----------------------|> .gitignore
FILE  +----------------------|> LICENSE
FILE  +----------------------|> README.md
FILE  +----------------------|> setup.py
</code>
</pre>
