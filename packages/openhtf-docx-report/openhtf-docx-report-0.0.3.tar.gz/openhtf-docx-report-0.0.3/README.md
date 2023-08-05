# openhtf-docx-report Package

This is a simple Openhtf/Spintop-Openhtf report callback to generate a MS-WORD
test report. 


To use it you have to add an import statement
from openhtf_docx_report import docx_report_callback

and then a callback in your main test sequence
  test.add_output_callbacks(docx_report_callback)

and to add the test description, etc fields you have to add them as metadata

  test = htf.Test(hello_world, test_name='MyTest', test_description='OpenHTF Example Test',
      test_version='1.0.0', user_id = 'operator', path = '\\reports')

And if you want the docx test documents in a certain directory then add a path field. (e.g. path = '\\reports')

Sample template is included in tests; template.docx
