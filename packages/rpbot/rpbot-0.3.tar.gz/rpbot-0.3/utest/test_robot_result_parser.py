import pytest
import io
from rpbot.reader.robot_results_parser import RobotResultsParser


@pytest.fixture
def reporter(mocker):
    reporter = mocker.MagicMock()
    yield reporter


@pytest.fixture
def parser(reporter):
    parser = RobotResultsParser(reporter)
    yield parser


simple_output_xml = """<?xml version="1.0" encoding="UTF-8"?>
<robot generator="Robot 3.2.1 (Python 3.8.2 on linux)" generated="20200926 15:33:43.760" rpa="false">
<suite id="s1" name="Test Rp" source="/p4_ws/doyou89.jung/workspace/projects/cosmos/atest/example/test_rp.robot">
<test id="s1-t1" name="test1">
<kw name="Log" library="BuiltIn">
<doc>Logs the given message with the given level.</doc>
<arguments>
<arg>test1</arg>
</arguments>
<msg timestamp="20200926 15:33:43.777" level="INFO">test1</msg>
<status status="PASS" starttime="20200926 15:33:43.777" endtime="20200926 15:33:43.777"></status>
</kw>
<status status="PASS" starttime="20200926 15:33:43.776" endtime="20200926 15:33:43.777" critical="yes"></status>
</test>
<status status="PASS" starttime="20200926 15:33:43.761" endtime="20200926 15:33:43.777"></status>
</suite>
<statistics>
<total>
<stat pass="1" fail="0">Critical Tests</stat>
<stat pass="1" fail="0">All Tests</stat>
</total>
<tag>
</tag>
<suite>
<stat pass="1" fail="0" id="s1" name="Test Rp">Test Rp</stat>
</suite>
</statistics>
<errors>
</errors>
</robot>
"""

simple_failed_output_xml = """<?xml version="1.0" encoding="UTF-8"?>
<robot generator="Robot 3.2.1 (Python 3.8.2 on linux)" generated="20200926 15:34:56.754" rpa="false">
<suite id="s1" name="Test Rp" source="/p4_ws/doyou89.jung/workspace/projects/cosmos/atest/example/test_rp.robot">
<test id="s1-t1" name="test1">
<kw name="Log" library="BuiltIn">
<doc>Logs the given message with the given level.</doc>
<arguments>
<arg>test1</arg>
</arguments>
<msg timestamp="20200926 15:34:56.771" level="INFO">test1</msg>
<status status="PASS" starttime="20200926 15:34:56.771" endtime="20200926 15:34:56.771"></status>
</kw>
<kw name="Fail" library="BuiltIn">
<doc>Fails the test with the given message and optionally alters its tags.</doc>
<arguments>
<arg>test fail message</arg>
</arguments>
<msg timestamp="20200926 15:34:56.771" level="FAIL">test fail message</msg>
<status status="FAIL" starttime="20200926 15:34:56.771" endtime="20200926 15:34:56.771"></status>
</kw>
<status status="FAIL" starttime="20200926 15:34:56.770" endtime="20200926 15:34:56.771" critical="yes">test fail message</status>
</test>
<status status="FAIL" starttime="20200926 15:34:56.755" endtime="20200926 15:34:56.772"></status>
</suite>
<statistics>
<total>
<stat pass="0" fail="1">Critical Tests</stat>
<stat pass="0" fail="1">All Tests</stat>
</total>
<tag>
</tag>
<suite>
<stat pass="0" fail="1" id="s1" name="Test Rp">Test Rp</stat>
</suite>
</statistics>
<errors>
</errors>
</robot>
"""


def test_xml_to_db(reporter, parser):
    """test xml_to_db"""
    parser.xml_to_db(io.StringIO(simple_output_xml))

    assert reporter.start_suite.call_count == 1
    assert reporter.start_suite.call_args[0][0] == 'Test Rp'
    assert reporter.start_suite.call_args[0][1]['id'] == 's1'
    assert reporter.start_suite.call_args[0][1]['status'] == 'PASS'

    assert reporter.start_test.call_count == 1
    assert reporter.start_test.call_args[0][0] == 'test1'
    assert reporter.start_test.call_args[0][1]['id'] == 's1-t1'
    assert reporter.start_test.call_args[0][1]['status'] == 'PASS'

    assert reporter.start_keyword.call_count == 1
    assert reporter.start_keyword.call_args[0][0] == 'BuiltIn.Log'
    assert reporter.start_keyword.call_args[0][1]['type'] == 'kw'
    assert reporter.start_keyword.call_args[0][1]['kwname'] == 'Log'
    assert reporter.start_keyword.call_args[0][1]['libname'] == 'BuiltIn'
    assert reporter.start_keyword.call_args[0][1]['status'] == 'PASS'

    assert reporter.end_keyword.call_count == 1
    assert reporter.end_test.call_count == 1
    assert reporter.end_suite.call_count == 2


def test_xml_to_db_with_fail(reporter, parser):
    """test xml_to_db with failed test"""
    parser.xml_to_db(io.StringIO(simple_failed_output_xml))

    assert reporter.start_suite.call_count == 1
    assert reporter.start_suite.call_args[0][0] == 'Test Rp'
    assert reporter.start_suite.call_args[0][1]['id'] == 's1'
    assert reporter.start_suite.call_args[0][1]['status'] == 'FAIL'

    assert reporter.start_test.call_count == 1
    assert reporter.start_test.call_args[0][0] == 'test1'
    assert reporter.start_test.call_args[0][1]['id'] == 's1-t1'
    assert reporter.start_test.call_args[0][1]['status'] == 'FAIL'

    assert reporter.start_keyword.call_count == 2
    assert reporter.start_keyword.call_args_list[0][0][0] == 'BuiltIn.Log'
    assert reporter.start_keyword.call_args_list[0][0][1]['type'] == 'kw'
    assert reporter.start_keyword.call_args_list[0][0][1]['kwname'] == 'Log'
    assert reporter.start_keyword.call_args_list[0][0][1]['libname'] == 'BuiltIn'
    assert reporter.start_keyword.call_args_list[0][0][1]['status'] == 'PASS'

    assert reporter.end_keyword.call_count == 2
    assert reporter.end_test.call_count == 1
    assert reporter.end_suite.call_count == 2
