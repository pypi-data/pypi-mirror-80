Changelog
=========

v0.4.0 / 2020-09-22
-------------------

  * fixes error with auto inserting discovered accountId argument
  * converts list items to appropriate typed classes
  * model setters now use transforms to set descriptors
  * transforms updated to include min and max values for int and str
  * adds serialize() function to Array class
  * adds update() method to models Base class
  * fixes issue with child models failing to load properly


v0.3.0 / 2020-09-13
-------------------

  * Added describe() function to recreate entire model schema
  * Fixed documentation formating issue (#16)
  * Remove unused setting `pureport.defaults.account_id`
  * Refactor bindings system to make functions session-aware
  * Automatically determine account ID for a session
  * Automatically inject session account id into function arguments
  * Remove `pureport.defaults.automake_bindings` setting
  * Add automake_bindings keyword argument to session init
  * The `make_bindings()` function is now a session method
  * Create session object to make models if no session is passed


v0.2.0 / 2020-09-07
-------------------

  * Add support for passing query string to API call
  * Add support for accepting query parameters for auto generated functions


v0.1.0 / 2020-09-04
-------------------

  * Initial release of python-pureport
