# HTMLMaker

*Disclaimer:* Is awful and probably shouldn't be used

The HTML file can only contain tags which have been defined in `BaseTags.py` or `VoidTags.py` (or elsewhere if you want to start creating your own modules and/or extensions). It should have most of the HTML tags commonly used (i.e. `<div/>` `<a/>` `<h/>` etc.)

Basic use involves creating an instance of the `HTMLGenerator` class and then start creating instances of tag classes (e.g. `DivisionTag()`) that you want to add to your html file. When done, call the `HTMLGenerator.saveHTML(some_name,some_dir)` method and it will save it to the corresponding file, you can also use the `HTMLGenerator.dumpHTML()` to have the HTML text printed to stdout.

A basic HTML file is generally composed of two main tags, the `<head>` tag and the `<body>` tag. The `<head>` tag is kind of like a pre-amble where you can define basic global properties, and the `<body>` tag is where you put the stuff you want to get displayed on the page. The `HTMLGenerator` class has special methods for adding stuff to the `<head>` (`.addHeadTag(new_tag)`) and `<body>` (`.addBodyTag(new_tag)`)tags respectively, as it always creates them (i.e. you don't need to make those tags explicitly). Instances of the `<head>` and `<body>` tags can also be accessed via the corresponding `.getTag()` methods.

The `make_html.py` script shows an example implementation of the `HTMLGenerator` class.