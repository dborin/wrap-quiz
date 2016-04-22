# wrap-quiz
Wrap code challenge

----------

###Notes

* For purposes of this exercise, I used `find_element_by_link_text` in several places, but if this site is in multiple languages, I'd have to find a way to use CSS, class or some other method to identify elements.
* The site doesn't utilize unique identifiers in the DOM.  To make tests more robust, I'd work with Dev to add unobtrusive identifiers (`data_attributes`) to elements to encourage more robust test automation (see above).
* Since this is a simple code test, I put all tests into one module.  If this were a sustainable and scalable test framework, modules would have been broken up and workarounds for the browser open/close at the start/end of each test would have been created.
* The use of `time.sleep()` is expedient for this challenge, but time permitting, a refactor to detect for the presence of the green "throbber" and then its removal might be a better way to wait for longer parts of the workflow.

###Running the test

This was developed and tested using Python 2.7.4 on Ubuntu 15.10

You will need to install the `selenium` Python module (suggested to use either `pip` or `easy_install`)

`$ pip install selenium`
or
`$ easy_install install selenium`

Then just run it from the command line.

`$ ./test.py`