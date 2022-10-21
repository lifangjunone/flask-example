import pytest
import time
import os
import sys


# defined constant
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


# -------------------------------------------------------------------#
# -------------------------筛选测试-----------------------------------#
# -------------------------------------------------------------------#
# Case01
# ------------------显式指定函数名，通过 :: 标记------------------------#
# run: pytest tests/api/v1/test_example.py::test_specific_name
def test_specific_name():
    assert (1, 2, 3) == (1, 2, 3)


# Case02
# ------------------使用模糊匹配，使用 -k 选项标识------------------------#
# run: pytest -k test_aa tests/api/v1/test_example.py
def test_aa_1():
    assert (1, 2, 3) == (1, 2, 3)


def test_aa_2():
    assert (1, 2, 3) == (1, 2, 3)


def test_aa_3():
    assert (1, 2, 3) == (1, 2, 3)


# run: pytest -k test_bb tests/api/v1/test_example.py
def test_bb_1():
    assert (1, 2, 3) == (1, 2, 3)


def test_bb_2():
    assert (1, 2, 3) == (1, 2, 3)


def test_bb_3():
    assert (1, 2, 3) == (1, 2, 3)


# Case03
# ------------------使用 pytest.mark 在函数上进行标记------------------------#
# run: pytest -m finished tests/api/v1/test_example.py
@pytest.mark.finished
def test_mark_1():
    assert (1, 2, 3) == (1, 2, 3)


# run: pytest -m unfinished tests/api/v1/test_example.py
@pytest.mark.unfinished
def test_mark_2():
    assert (1, 2, 3) == (1, 2, 3)


# Case04
# ------------------使用 pytest.mark 在函数上进行标记------------------------#
# run: pytest -m finished tests/api/v1/test_example.py
@pytest.mark.failed
def test_mark_3():
    assert (1, 2, 3) == (1, 2, 3)


# Case05
# ------------------特定的标记 pytest.mark.skip跳过测试------------------------#
# run: pytest  tests/api/v1/test_example.py
@pytest.mark.skip(reason="Features have not yet been developed")
def test_skip_1():
    assert (1, 2, 3) == (1, 2, 3)


# run: pytest  tests/api/v1/test_example.py
@pytest.mark.skip(reason="Features have not yet been developed")
def test_skip_2():
    assert (1, 2, 3) == (1, 2, 3)


# run: pytest  tests/api/v1/test_example.py
@pytest.mark.skip(reason="Features have not yet been developed")
def test_skip_3():
    assert (1, 2, 3) == (1, 2, 3)


# Case06
# ------------------执行失败，但又不想直接跳过，而是希望显示的提示 pytest.mark.xfail-------------------#
# run: pytest  tests/api/v1/test_example.py
@pytest.mark.xfail(reason="execute failed, but not want skip")
def test_show_fail_1():
    assert (1, 2, 3) == (1, 2, 2)


# Case07
# ------------------函数传递多组参数且每组参数都独立执行一次测试pytest.mark.parametrize(arg_name, arg_values)-------------#
# run: pytest -v tests/api/v1/test_example.py::test_passwd_length
@pytest.mark.parametrize('passwd',
                         ['123456234',
                          'abcdefghijklmn',
                          '3434kjklsjdfisf'
                          ])
def test_passwd_length(passwd):
    assert len(passwd) >= 8


# run: pytest -v tests/api/v1/test_example.py::test_passwd_md5_id
@pytest.mark.parametrize(
    'user, passwd',
    [pytest.param('jack', 'abcdefgh', id='User<Jack>'),
     pytest.param('tom', 'a123456a', id='User<Tom>')
     ]
)
def test_passwd_md5_id(user, passwd):
    db = {
        'jack': 'e8dc4081b13434b45189a720b77b6818',
        'tom': '1702a132e769a623c1adb78353fc9503'
    }
    import hashlib
    assert hashlib.md5(passwd.encode()).hexdigest() == db[user]


# Case08
# ------------------固件（Fixture）, 使用pytest.fixture()---------------------------------------------------#
# run: pytest -v tests/api/v1/test_example.py::test_postcode
@pytest.fixture()
def postcode():
    return '010'


def test_postcode(postcode):
    assert postcode == '010'


# Case09
# ------------------固件（Fixture）, 使用pytest.fixture() + yield ---------------------------------------------------#
# 使用 yield 关键词将固件分为两部分，yield 之前的代码属于预处理，会在测试前执行；yield 之后的代码属于后处理，将在测试完成后执行
# run: pytest -v tests/api/v1/test_example.py::test_postcode
@pytest.fixture()
def db():
    print("Connection db is successful")
    yield
    print("Connection closed")


def user_info(user_id):
    d = {
        "001": "zhang"
    }
    return d[user_id]


def test_query_user(db):
    assert user_info('001') == 'zhang'


# Case10
# ----------------------------固件作用域------------------------------------ #
"""
在定义固件时，通过 scope 参数声明作用域，可选项有：
function: 函数级，每个测试函数都会执行一次固件；
class: 类级别，每个测试类执行一次，所有方法都可以使用；
module: 模块级，每个模块执行一次，模块内函数和方法都可使用；
session: 会话级，一次测试只执行一次，所有被找到的函数和方法都可用
"""


@pytest.fixture(scope='session')
def sess_scope():
    print("session level fixture")


@pytest.fixture(scope='module')
def mod_scope():
    print("module level fixture")


@pytest.fixture(scope='class')
def class_scope():
    print("class level fixture")


@pytest.fixture(scope='function')
def func_scope():
    print("function level fixture")


def test_multi_scope(sess_scope, mod_scope, class_scope, func_scope):
    print("test multi scope")


# 对于类使用作用域，需要使用 pytest.mark.usefixtures （对函数和方法也适用）
@pytest.mark.usefixtures('class_scope')
class TestclassScope:
    def test_01(self):
        print(1)

    def test_02(self):
        print(2)


# Case11
# ----------------------------固件自动执行------------------------------------ #
# 1, 用于统计每个函数运行时间 (function scope)
# 2, 用于统计测试总耗时 (session scope)
@pytest.fixture(scope='session', autouse=True)
def timer_session_scope():
    start = time.time()
    print('\n start: {}'.format(time.strftime(DATE_FORMAT), time.localtime(start)))

    yield

    finished = time.time()
    print('finished: {}'.format(time.strftime(DATE_FORMAT, time.localtime(finished))))
    print('Total time cost: {:.3f}s'.format(finished - start))


@pytest.fixture(scope='function', autouse=True)
def timer_function_scope():
    start = time.time()

    yield

    print('Time cost: {:.3f}s'.format(time.time() - start))


def test_not_show_use_fixture_01():
    print('not show use fixture 01')
    time.sleep(1)


def test_not_show_use_fixture_02():
    print('not show use fixture 02')
    time.sleep(1)


# Case12
# ----------------------------固件重命名------------------------------------ #
@pytest.fixture(name='age')
def calculate_average_age():
    return 25


def test_age(age):
    assert age == 25


# Case13
# ----------------------------参数化------------------------------------ #
@pytest.fixture(params=[
    ('redis', '6379'),
    ('mysql', '3600')
])
def param(request):
    return request.param


@pytest.fixture(autouse=True)
def db(param):
    print('\n Succeed to connect %s:%s' % param)

    yield

    print('\nSucceed to close %s:%s' % param)


def test_db():
    assert 1 == 1


# Case14
# ----------------------------内置固件------------------------------------ #
# ----------tmpdir 只有 function 作用域
# ----------tmpdir_factory 可以在所有作用域使用，包括 function, class, module, session
def test_tmpdir(tmpdir):
    my_tmp_dir = tmpdir.mkdir('my_tmp_dir')
    my_tmp_file = my_tmp_dir.join('tmp_file.txt')
    my_tmp_file.write('hello pytest')
    assert my_tmp_file.read() == 'hello pytest'


@pytest.fixture(scope='module')
def my_tmpdir_factory(tmpdir_factory):
    factory_dir = tmpdir_factory.mktemp('factory_dir')
    f_file = factory_dir.join('factory_file.txt')
    f_file.write('hello factory')
    return factory_dir, f_file


def test_factory_dir(my_tmpdir_factory):
    factory_dir, factory_file = my_tmpdir_factory
    new_file = factory_dir.join('new.txt')
    new_file.write('new file')
    assert sorted(list(os.listdir(factory_dir))) == sorted(['factory_file.txt', 'new.txt']) \
           and factory_file.read() == 'hello factory'


# Case15
# ----------------------------使用 pytestconfig 读取命令行参数和配置文件------------------------------------ #
def test_command_param(pytestconfig):
    print('host: %s' % pytestconfig.getoption('host'))
    print('port: %s' % pytestconfig.getoption('port'))


# Case16
# ----------------------------capsys 用于捕获 stdout 和 stderr 的内容，并临时关闭系统输出---------------------- #
def ping(output):
    print('Pong...', file=output)


def test_stdout(capsys):
    ping(sys.stdout)
    out, err = capsys.readouterr()
    assert out == 'Pong...\n'
    assert err == ''


def test_sterr(capsys):
    ping(sys.stderr)
    out, err = capsys.readouterr()
    assert out == ''
    assert err == 'Pong...\n'

















































