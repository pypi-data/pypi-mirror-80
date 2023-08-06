Changelog
=========

0.0.1.dev10 (2020-09-23)
------------------------

Changed
~~~~~~~
* Include metric type in attributes when sending metrics.


0.0.1.dev9 (2019-02-28)
-----------------------

Changed
~~~~~~~
* Deep merge user config file.


0.0.1.dev8 (2018-09-07)
-----------------------

Changed
~~~~~~~
* Remove mutation of the context passed to ffwd plugin.


0.0.1.dev7 (2018-06-21)
-----------------------

Fixed
~~~~~
* Add support for ulogger configuration.


0.0.1.dev6 (2018-06-20)
-----------------------

Fixed
~~~~~
* Fix routing for handling more than one message at a time.
* Improve warning log messages when loading plugin phase route.


0.0.1.dev5 (2018-06-18)
-----------------------

Fixed
~~~~~
* Provide router setup with correct number of arguments.


0.0.1.dev4 (2018-06-18)
-----------------------

Added
~~~~~
* Add logging-based default metrics plugin.
* Emit basic metrics from core router.
* Add a basic graceful shutdown mechanism.


0.0.1.dev3 (2018-06-14)
-------------------------
Added
~~~~~
* Add ``IRunnable``, ``IMessageHandler``.
* Add route configuration requirement.

Changed
~~~~~~~
* Require ``IEventMessage`` to have ``phase`` and ``msg_id``.

Removed
~~~~~~~
* Remove ``IEventConsumerClient``, ``IEnricherClient``, ``IPublisherClient``.


0.0.1.dev2 (2018-06-13)
-------------------------
Added
~~~~~
* Add logic to start installed + configured plugins.
* Add initial routing logic for event messages.
* Add interface definitions for a metrics plugin.
* Add FFWD-compatible metrics plugin.
* Enable plugin loader to load metrics plugin.

Fixed
~~~~~
* Load config only for active plugins.
