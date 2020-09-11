from distutils.core import setup
import py2exe
import cx_Freeze

executables = [cx_Freeze.Executable('search-service.py')]

cx_Freeze.setup(
name = 'DSE',
options = {'build_exe':{'packages':['nltk','pandas','math','copy','os','flask','requests'],
                        'include_files':['example_01.csv','result.txt','test_cases.csv','test-case2.txt','test-case2-updated.txt','custom_search_01.py']}},

executables = executables
)
