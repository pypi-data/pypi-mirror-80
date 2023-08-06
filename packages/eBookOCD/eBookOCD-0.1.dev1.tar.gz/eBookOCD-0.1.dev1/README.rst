eBookOCD
========

Extensible utility to rewrite eBook content. Useful for fixing common mistakes
made by authors and publishers alike.

Motivation
----------

While I like ebooks a lot, I am often disappointed with their technical quality, or lack thereof.
For example, I recently purchased a bundle of ebooks in a bout of nostalgia, to replace paper
editions long lost. Alas, the files are full of repeated typos, misspelled names, and so forth,
telling a sad tale of a publisher scanning in source material and not proofreading the result.

Faced with this, I used to fix the errors I find manually, mostly using regular expressions.
This is a pain in the bum, even when employing Edit Books (a part of Kovid Goyal's excellent
Calibre_). I therefore decided to write a piece of software to perform certain content rewrites
automatically. I also wanted to make the mechanism extensible by dynamically loading content
transformers at run-time. The result is eBookOCD. I hope that other people come up with either
their own ideas for transformers or with actual code that can be shared.

.. _Calibre: https://calibre-ebook.com

Basic usage
-----------

* ``ebookocd source.epub -d destination.epub``

  Rewrite source.epub content into a new file called destination.epub. The source file
  will be unaffected. This is the recommended method of rewriting files.

* ``ebookocd file.epub``

  Rewrite the file *in place*, overwriting the existing content. You should only use this
  method if your source file is version controlled, or if you have a backup available.

* ``ebookocd file.epub -x destination_directory``

  Create the specified directory and extract the source file's content into it.
  If the destination path already exists, execution will be aborted.

* ``ebookocd -z directory destination.epub``

  Bundle the directory's content as a compressed EPUB file. If the destination
  file already exists, execution will be aborted.

Advanced usage
--------------

* ``ebookocd source.epub -d destination.epub -t mymodule.myfile.MyTransformer``

  Rewrites source.epub content into a new file called destination.epub, using
  the specified transformer class for content filtering.

Content transformers
--------------------

Content transformers are Python classes used to process ebook content. They are loaded
dynamically at run-time, providing a mechanism to expand the functionality of eBookOCD
with third party transformer classes.

If no transformer class is specified, the internal DefaultTransformer will be used. It
is primarily concerned with removing unnecessary spaces from text-type files, like HTML
and CSS.

Transformers can modify the content in any desired fashion, the only condition being
that all methods of ``TransformerMixin`` (see API_) are implemented. The transformer
``ebookocd.transform.monty.WonderfulSpam`` is provided as a simple reference. This
example extends the ``DefaultTransformer`` class, but you can opt to write code that
references ``ebookocd.api.TransformerMixin`` directly.

.. _API: https://gitlab.com/ebookocd/ebookocd/-/blob/master/ebookocd/api.py

Requirements
------------

eBookOCD requires Python 3.8 or higher. This is not an arbitrary decision, because
it uses features introduced in this particular Python release.

License
-------

Copyright © 2020 Ralph Seichter. Please see the LICENSE_ file for details.

.. _LICENSE: https://gitlab.com/ebookocd/ebookocd/-/blob/master/LICENSE
