html_crawler
============

a sample project in Python to crawl and search web pages


Requirements:

- Is called like follows "python WebPageWordCountAnalysis.py url word", where "url" is the webpage of interest and "word" is the word to be searched for.  In web page means between the <body> tags of the retrieved web page html at the url.

- The script must download the web page at the url and provide the number of times the "word" appears between the <body> tags.

- The script should also navigate further into the next web pages by searching for href tags also between the <body> tags.  Use regular expressions to find and follow the href links.  The script at a minimum must go one level into the next href links but I would like to see you use recursion to following the links deeper all the way to their end or at least to a max level as there may be circular references.  You can ignore href links inside <script> tags.

- The script will have a simple output:
  Base Web Page Count for  "word" = XX
  Child 1 Web Page Count for  "word" = XX
  Child 2 Web Page Count for  "word" = XX
  ...
  Child n Web Page Count for  "word" = XX
  Grand Child 1 Web Page Count for  "word" = XX
  Grand Child 2 Web Page Count for  "word" = XX
  ...
  Grand Child n Web Page Count for  "word" = XX
  ...
  ..
  to max level child