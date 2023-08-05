Influxdb Pytest Plugin
======================

Influxdb `Pytest <http://pytest.org>`_ Plugin designed for reporting test results to the `InfluxDB <https://www.influxdata.com/>`_
and provide with the live test results report which can be later integrated with a reporting tool.
It's developed as pytest plugin and distributed via `pypi <https://pypi.org/project/pytest-influxdb>`_.

.. image:: https://pypip.in/v/pytest-influxdb/badge.png
        :alt: Release Status
        :target: https://pypi.python.org/pypi/pytest-influxdb
.. image:: https://pypip.in/d/pytest-influxdb/badge.png
        :alt: Downloads
        :target: https://pypi.python.org/pypi/pytest-influxdb

Table of Contents
=================

- `About this documentation <#id1>`_
- `Usage <#id2>`_
- `Add custom fields as an additional data <#id3>`_
- `Send attachment <#send-screenshot-as-attachment>`_

About this documentation
========================
Welcome to the Influxdb Pytest Plugin documentation!

This style guide provides set of editorial guidelines for anyone using Influxdb Pytest Plugin.

Usage
=====

**Installation**

    pip install pytest-influxdb-plugin

**Launching**

To run a test with pytest-influxdb-plugin, the '--pytest-influxdb' flag should be provided.

    pytest -sv --pytest-influxdb

Prepare the config file :code:`pytest.ini` in root directory of tests and/or call next to the run command the mandatory config variables which are mentioned below:


The next mandatory fields should be mentioned in :code:`pytest.ini` or run through command line without '--' prefix:

- :code:`--influxdb_host` - host/url of the influxdb
- :code:`--influxdb_name` - name of influxdb table

And here are the optional fields:

- :code:`--influxdb_port` - port of the influxdb
- :code:`--influxdb_user` - username of influxdb user
- :code:`--influxdb_password` - password of influxdb user
- :code:`--influxdb_project` - project name
- :code:`--influxdb_version` - custom version of project
- :code:`--influxdb_merged` - merge configuration
- :code:`--influxdb_run_id` - run id (Can be passed as CI variable)

Example of :code:`pytest.ini`:

.. code-block:: text

    [pytest]
    influxdb_host = <DB_HOST>
    influxdb_port = <DB_PORT>
    influxdb_name = <DB_NAME>
    influxdb_user = <DB_USER>
    influxdb_password = <DB_PASSWORD>
    influxdb_project = <PROJECT_NAME>
    influxdb_version = <PROJECT_NAME>
    influxdb_run_id = <RUN_ID>

Add custom fields as an additional data
=======================================
**Add custom fields for test result**
For adding custom fields as an additional data for test result the code like below should be added in conftest.py.

Example 1:

.. code-block:: python

    @pytest.fixture(scope='function', autouse=True)
    def test_suite(request):
        from influxdb_pytest_plugin import TestResultDTO
        test_result_dto = TestResultDTO()
        test_name = request.node.nodeid
        TestResultDTO.set_tag_values(test_result_dto, test_name, {'tag1': 'tag_value1', 'tag2': 'tag_value2'})
        TestResultDTO.set_field_values(test_result_dto, test_name, {'field1': 'field_value1', 'field2': 'field_value2'})

**Add custom fields for suite result**
For adding custom fields as an additional data for suite result the :code:`pytest_terminal_summary` pytest plugin like below in conftest.py.

.. code-block:: python

    @pytest.hookimpl(hookwrapper=True)
    def pytest_terminal_summary(config, terminalreporter):
        from influxdb_pytest_plugin import SuiteResultDTO
        suite_result_dto = SuiteResultDTO()
        SuiteResultDTO.set_tag_values(suite_result_dto, {'tag1': 'tag_value1'})
        SuiteResultDTO.set_field_values(suite_result_dto, {'field1': 'field_value1'})
        yield

Example 2:
Add custom fields via :code:`--influxdb_values` config, just fill the below template and set as :code:`--influxdb_values` config:

.. code-block:: python

    {
      "fields": {
        "test_result": {
        },
        "suite_result": {
        }
      },
      "tags": {
        "test_result": {
        },
        "suite_result": {
        }
      }
    }

Send screenshot as attachment
=============================
For sending the screenshot to the influxdb, the :code:`screenshot_url` fixture should be used in function scope like below:

Example 1:

.. code-block:: python

    @pytest.fixture(scope="function")
    def chrome_driver_init(request, screenshot_url, pytestconfig):
    chrome_driver = webdriver.Chrome()
    request.cls.driver = chrome_driver
    yield
    if request.node.rep_call.failed and pytestconfig.getoption('--pytest-influxdb'):
        screenshot_link = 'URL_EXAMPLE'
        chrome_driver.save_screenshot(screenshot_link)
        screenshot_url(screenshot_link)
    chrome_driver.close()

Example 2:

.. code-block:: python

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        outcome = yield
        rep = outcome.get_result()
        if rep.when == 'call':
            try:
                screenshot_path = web_client.current.save_screenshot("Screenshot link")
                item.user_properties = ("screenshot_url", screenshot_path)
            # web_driver.save_screenshot and other magic to add screenshot to your report
            except Exception as e:
                print('Exception while screen-shot creation: {}'.format(e))
