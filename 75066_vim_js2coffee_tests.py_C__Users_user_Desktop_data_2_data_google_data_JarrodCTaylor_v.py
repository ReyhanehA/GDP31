import os
import stat
import unittest

import autoload.vim_js2coffee as sut

JS_FILE = "/tmp/file.js"
COFFEE_FILE = "/tmp/file.coffee"
ERROR_LOG = "/tmp/error.log"


def read_file_to_list(file_to_read):
    file_contents = []
    with open(file_to_read, "r") as f:
        for line in f.readlines():
            file_contents.append(line)
        return file_contents


def delete_if_present(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


class VimJS2CoffeeTests(unittest.TestCase):

    def tearDown(self):
        delete_if_present(ERROR_LOG)
        delete_if_present(JS_FILE)
        delete_if_present(COFFEE_FILE)

    def test_get_coffee_from_js_buffer_contents_return_properly_formatted_coffee_script_when_given_valid_input(self):
        contents = ["var example = function() {\n", "    console.log('This is a different example');\n", "}"]
        sut.get_coffee_from_js_buffer_contents(contents)
        expected_result = ['example = ->\n', '  console.log "This is a different example"\n', '  return\n']
        actual_results = read_file_to_list(COFFEE_FILE)
        self.assertEqual(actual_results, expected_result)

    def test_works_with_nested_quotes(self):
        contents = ["var example = function() {\n", "    console.log(\"This is a 'different' example\");\n", "}"]
        sut.get_coffee_from_js_buffer_contents(contents)
        expected_result = ['example = ->\n', '  console.log "This is a \'different\' example"\n', '  return\n']
        actual_results = read_file_to_list(COFFEE_FILE)
        self.assertEqual(actual_results, expected_result)

    def test_get_coffee_from_js_buffer_contents_raises_error_when_given_invalid_input(self):
        contents = ["va = oiuewf{}"]
        with self.assertRaises(Exception):
            sut.get_coffee_from_js_buffer_contents(contents)

    def test_write_js_to_file_writes_correct_contents_to_desired_file(self):
        contents = ["var example = function() {", "    console.log('this is an example');", "}"]
        sut.write_buffer_contents_to_file(JS_FILE, contents)
        with open(JS_FILE, "r") as f:
            self.assertEqual(f.readlines(), [line + "\n" for line in contents])

    def test_run_js_to_coffee_on_js_file_creates_a_proper_coffee_file_when_given_valid_input(self):
        contents = ["var example = function() {\n", "    console.log('This is another example');\n", "}"]
        sut.write_buffer_contents_to_file(JS_FILE, contents)
        sut.run_js_to_coffee_on_js_file()
        expected_coffee_output = ['example = ->\n', '  console.log "This is another example"\n', '  return\n']
        self.assertEqual(read_file_to_list(COFFEE_FILE), expected_coffee_output)

    def test_run_js_to_coffee_on_js_file_populates_an_error_file_when_given_invalid_javascript(self):
        contents = ["va = oiuewf{}"]
        sut.write_buffer_contents_to_file(JS_FILE, contents)
        sut.run_js_to_coffee_on_js_file()
        self.assertTrue(os.stat(ERROR_LOG)[stat.ST_SIZE] > 0)

    def test_check_for_errors_raises_an_exception_if_there_is_a_non_empty_error_log(self):
        contents = ["var bad_example = function() \n", "    console.log('This is another example');\n", "}"]
        sut.write_buffer_contents_to_file(JS_FILE, contents)
        sut.run_js_to_coffee_on_js_file()
        self.assertTrue(os.stat(ERROR_LOG)[stat.ST_SIZE] > 0)
        with self.assertRaises(Exception):
            sut.check_for_errors()

    def test_check_for_errors_does_not_raise_an_exception_if_there_is_an_empty_error_log(self):
        contents = ["var example = function() {\n", "    console.log('This is a different example');\n", "}"]
        sut.write_buffer_contents_to_file(JS_FILE, contents)
        sut.run_js_to_coffee_on_js_file()
        with self.assertRaises(AssertionError):
            with self.assertRaises(Exception):
                sut.check_for_errors()


class VimCoffee2JSTests(unittest.TestCase):

    def tearDown(self):
        delete_if_present(ERROR_LOG)
        delete_if_present(COFFEE_FILE)
        delete_if_present(JS_FILE)

    def test_get_js_from_coffee_buffer_contents_return_properly_formatted_js_when_given_valid_input(self):
        contents = ['for name in ["Toran", "Matt", "Brandon", "Joel"]\n', '  console.log(name)']
        sut.get_js_from_coffee_buffer_contents(contents)
        expected_result = [
            '(function() {\n',
            '  var name, _i, _len, _ref;\n',
            '\n',
            '  _ref = ["Toran", "Matt", "Brandon", "Joel"];\n',
            '  for (_i = 0, _len = _ref.length; _i < _len; _i++) {\n',
            '    name = _ref[_i];\n',
            '    console.log(name);\n',
            '  }\n',
            '\n',
            '}).call(this);\n'
        ]
        actual_results = read_file_to_list(JS_FILE)[1:]
        self.assertEqual(actual_results, expected_result)

    def test_get_js_from_coffee_buffer_contents_raises_error_when_given_invalid_input(self):
        contents = ['for name in ["Toran", "Matt"']
        with self.assertRaises(Exception):
            sut.get_js_from_coffee_buffer_contents(contents)

    def test_write_buffer_contents_to_file_writes_correct_contents_to_desired_file_with_valid_coffee_script(self):
        contents = ['for name in ["Toran", "Matt", "Brandon", "Joel"]', "  console.log('The name' + name)"]
        sut.write_buffer_contents_to_file(COFFEE_FILE, contents)
        with open(COFFEE_FILE, "r") as f:
            self.assertEqual(f.readlines(), [line + "\n" for line in contents])

    def test_run_coffee_to_js_on_coffee_file_creates_a_proper_js_file_when_given_valid_input(self):
        contents = ["for name in ['Toran', 'Matt']\n", "  console.log('The name' + name)"]
        sut.write_buffer_contents_to_file(COFFEE_FILE, contents)
        sut.run_coffee_to_js_on_coffee_file()
        expected_js_output = [
            "(function() {\n",
            "  var name, _i, _len, _ref;\n",
            "\n",
            "  _ref = ['Toran', 'Matt'];\n",
            "  for (_i = 0, _len = _ref.length; _i < _len; _i++) {\n",
            "    name = _ref[_i];\n",
            "    console.log('The name' + name);\n",
            "  }\n",
            "\n",
            "}).call(this);\n",
        ]
        return_value = read_file_to_list(JS_FILE)[1:]
        self.assertEqual(return_value, expected_js_output)

    def test_run_coffee_to_js_on_coffee_file_populates_an_error_file_when_given_invalid_coffeescript(self):
        contents = ['for name in ["Jarrod", Katie"']
        sut.write_buffer_contents_to_file(COFFEE_FILE, contents)
        sut.run_coffee_to_js_on_coffee_file()
        self.assertTrue(os.stat(ERROR_LOG)[stat.ST_SIZE] > 0)

    def test_check_for_errors_raises_an_exception_if_there_is_a_non_empty_error_log(self):
        contents = ['for name in ["Jarrod", "Adam"']
        sut.write_buffer_contents_to_file(COFFEE_FILE, contents)
        sut.run_coffee_to_js_on_coffee_file()
        self.assertTrue(os.stat(ERROR_LOG)[stat.ST_SIZE] > 0)
        with self.assertRaises(Exception):
            sut.check_for_errors()

    def test_check_for_errors_does_not_raise_an_exception_if_there_is_an_empty_error_log(self):
        contents = ['for name in ["Toran", "Matt", "Brandon", "Joel"]\n', "  console.log(name)"]
        sut.write_buffer_contents_to_file(COFFEE_FILE, contents)
        sut.run_coffee_to_js_on_coffee_file()
        with self.assertRaises(AssertionError):
            with self.assertRaises(Exception):
                sut.check_for_errors()
