================
CompressedLogger
================


.. image:: https://img.shields.io/pypi/v/compressedlogger.svg
        :target: https://pypi.python.org/pypi/compressedlogger


This is a logging handler to be used with the standard `python logging <https://docs.python.org/3/library/logging.html>`_ module. 
The handler creates a log file with the current logs and automatically moves old log files into zipped archives. 
You can set how many uncompressed logfiles you want to hold and what timespan they should cover. 
For example you can set each log file to cover three hours and keep four uncompressed logfiles.
When the limit of uncompressed logfiles is reached, the oldest uncompressed file will be
moved into a zipped archive file for that day. This way, all logentries for a single day are combined into one zipped file. 
You can also set a maximum of days to keep the archive files as well as a general size limit for archives. 
If either one of them is reached, the oldest archives are deleted. 


Behaviour:
----------

Using the following configuration:
.. code-block:: python

   compressed_handler = compressedlogger.CompressedLogger(log_path="logs/", 
   													      filename="mylog", 
   													      header="- - version: 1.2.34 - - -",
   													      live_log_minutes=300,
   													      live_log_count=3,
   													      max_archive_size_mb=3,
   													      archive_days=2)

This will rotate the live log every 300 minutes. When started at 21.9.2020 - 10:33h, the first live log file will be named
mylog-10:33.log. The first rotation will not be at 15:33, but at 15:00. Log rotation timestamp is calculated from 0:00h and 
not from the start of the application. Therefore, the next live log will be named mylog-15:00.log.
So there will be the log files: `mylog-10:33.log`, `mylog-15:00.log`, `mylog-20:00.log`. Because the live logs rotate on
day change, the next rotation will happen at 00:00h and not at 01:00h. 
Once there are more livelogs than in the `max_live_logs` configuration, the latest log will be moved into a compressed archive for that day.
The `header` will be written to the top of every archived log. So in this example, there will be the log archive `mylog2020-09-21.log.gz`
which will contain one logfile `mylog2020-09-21.log` with the content of [header + mylog-10:33.log +  mylog-15:00.log + mylog-20:00.log].



Usage:
------

Parameters:
* log_path: where your logs will be stored
* filename: name of you logfile
* live_log_minutes: timespan that is covered by a single live-log
* live_log_count: maximum number of live logs to keep uncompressed
* max_archive_size_mb: maximum combined size of archived logs, in megabyte
* archive_days: maximum of days to keep log archives
* header: this header will be written on top of every archived log


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage