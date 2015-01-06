from __future__ import absolute_import, print_function, division
# N.B., do not import unicode_literals in tests


from petl.util import header, fieldnames, data, records, look, see, \
    itervalues, valuecounter, valuecounts, isunique, lookup, lookupone, \
    dictlookup, dictlookupone, numparser, \
    DuplicateKeyError, rowlengths, stats, typecounts, parsecounts, typeset, \
    valuecount, stringpatterns, diffheaders, diffvalues, \
    datetimeparser, values, columns, facetcolumns, isordered, \
    rowgroupby, lookstr, namedtuples, dicts, recordlookup, recordlookupone, \
    nrows, progress
from petl.test.util import ieq, eq_
from petl.compat import PY2, next, maxint


def test_header():
    table = (('foo', 'bar'), ('a', 1), ('b', 2))
    actual = header(table)
    expect = ('foo', 'bar')
    eq_(expect, actual)
    table = (['foo', 'bar'], ['a', 1], ['b', 2])
    actual = header(table)
    eq_(expect, actual)

    
def test_fieldnames():
    table = (('foo', 'bar'), ('a', 1), ('b', 2))
    actual = fieldnames(table)
    expect = ['foo', 'bar']
    eq_(expect, actual)
    
    class CustomField(object):

        def __init__(self, key, description):
            self.key = key
            self.description = description

        def __str__(self):
            return self.key

        def __repr__(self):
            return 'CustomField(%r, %r)' % (self.key, self.description)
        
    table = ((CustomField('foo', 'Get some foo.'),
              CustomField('bar', 'A lot of bar.')),
             ('a', 1), 
             ('b', 2))
    actual = fieldnames(table)
    expect = ['foo', 'bar']
    eq_(expect, actual)
    
    
def test_data():
    table = (('foo', 'bar'), ('a', 1), ('b', 2))
    actual = data(table)
    expect = (('a', 1), ('b', 2))
    ieq(expect, actual)


def test_dicts():
    table = (('foo', 'bar'), ('a', 1), ('b', 2))
    actual = dicts(table)
    expect = ({'foo': 'a', 'bar': 1}, {'foo': 'b', 'bar': 2})
    ieq(expect, actual)
    
        
def test_dicts_shortrows():
    table = (('foo', 'bar'), ('a', 1), ('b',))
    actual = dicts(table)
    expect = ({'foo': 'a', 'bar': 1}, {'foo': 'b', 'bar': None})
    ieq(expect, actual)
    
    
def test_records():
    table = (('foo', 'bar'), ('a', 1), ('b', 2))
    actual = records(table)
    # access items
    it = iter(actual)
    o = next(it)
    eq_('a', o['foo'])
    eq_(1, o['bar'])
    o = next(it)
    eq_('b', o['foo'])
    eq_(2, o['bar'])
    # access attributes
    it = iter(actual)
    o = next(it)
    eq_('a', o.foo)
    eq_(1, o.bar)
    o = next(it)
    eq_('b', o.foo)
    eq_(2, o.bar)
    
        
def test_records_unevenrows():
    table = (('foo', 'bar'), ('a', 1, True), ('b',))
    actual = records(table)
    # access items
    it = iter(actual)
    o = next(it)
    eq_('a', o['foo'])
    eq_(1, o['bar'])
    o = next(it)
    eq_('b', o['foo'])
    eq_(None, o['bar'])
    # access attributes
    it = iter(actual)
    o = next(it)
    eq_('a', o.foo)
    eq_(1, o.bar)
    o = next(it)
    eq_('b', o.foo)
    eq_(None, o.bar)
 
 
def test_namedtuples():
    table = (('foo', 'bar'), ('a', 1), ('b', 2))
    actual = namedtuples(table)
    it = iter(actual)
    o = next(it)
    eq_('a', o.foo)
    eq_(1, o.bar)
    o = next(it)
    eq_('b', o.foo)
    eq_(2, o.bar)
       
    
def test_namedtuples_unevenrows():
    table = (('foo', 'bar'), ('a', 1, True), ('b',))
    actual = namedtuples(table)
    it = iter(actual)
    o = next(it)
    eq_('a', o.foo)
    eq_(1, o.bar)
    o = next(it)
    eq_('b', o.foo)
    eq_(None, o.bar)
       
    
def test_nrows():
    table = (('foo', 'bar'), ('a', 1), ('b',))
    actual = nrows(table)
    expect = 2
    eq_(expect, actual)
    
    
def test_look():

    table = (('foo', 'bar'), ('a', 1), ('b', 2))
    actual = repr(look(table))
    expect = """+-------+-------+
| 'foo' | 'bar' |
+=======+=======+
| 'a'   |     1 |
+-------+-------+
| 'b'   |     2 |
+-------+-------+
"""
    eq_(expect, actual)

        
def test_look_irregular_rows():
    
    table = (('foo', 'bar'), ('a',), ('b', 2, True))
    actual = repr(look(table))
    expect = """+-------+-------+------+
| 'foo' | 'bar' |      |
+=======+=======+======+
| 'a'   |       |      |
+-------+-------+------+
| 'b'   |     2 | True |
+-------+-------+------+
"""
    eq_(expect, actual)
    
    
def test_look_bool():

    table = (('foo', 'bar'), ('a', True), ('b', False))
    actual = repr(look(table))
    expect = """+-------+-------+
| 'foo' | 'bar' |
+=======+=======+
| 'a'   | True  |
+-------+-------+
| 'b'   | False |
+-------+-------+
"""
    eq_(expect, actual)


def test_look_style_simple():
    table = (('foo', 'bar'), ('a', 1), ('b', 2))
    actual = repr(look(table, style='simple'))
    expect = """=====  =====
'foo'  'bar'
=====  =====
'a'        1
'b'        2
=====  =====
"""
    eq_(expect, actual)
    look.default_style = 'simple'
    actual = repr(look(table))
    eq_(expect, actual)
    look.default_style = 'grid'

    
def test_look_style_minimal():
    table = (('foo', 'bar'), ('a', 1), ('b', 2))
    actual = repr(look(table, style='minimal'))
    expect = """'foo'  'bar'
'a'        1
'b'        2
"""
    eq_(expect, actual)
    look.default_style = 'minimal'
    actual = repr(look(table))
    eq_(expect, actual)
    look.default_style = 'grid'

    
def test_see():
    
    table = (('foo', 'bar'), ('a', 1), ('b', 2))
    actual = repr(see(table))
    expect = """'foo': 'a', 'b'
'bar': 1, 2
"""
    eq_(expect, actual)


def test_see_duplicateheader():

    table = (('foo', 'bar', 'foo'), ('a', 1, 'a_prime'), ('b', 2, 'b_prime'))
    actual = repr(see(table))
    expect = """'foo': 'a', 'b'
'bar': 1, 2
'foo': 'a_prime', 'b_prime'
"""
    eq_(expect, actual)


def test_lookstr():
    
    table = (('foo', 'bar'), ('a', 1), ('b', 2))
    actual = repr(lookstr(table))
    expect = """+-----+-----+
| foo | bar |
+=====+=====+
| a   |   1 |
+-----+-----+
| b   |   2 |
+-----+-----+
"""
    eq_(expect, actual)

        
def test_itervalues():

    table = (('foo', 'bar', 'baz'), 
             ('a', 1, True), 
             ('b', 2), 
             ('b', 7, False))

    actual = itervalues(table, 'foo')
    expect = ('a', 'b', 'b')
    ieq(expect, actual) 

    actual = itervalues(table, 'bar')
    expect = (1, 2, 7)
    ieq(expect, actual) 
    
    actual = itervalues(table, ('foo', 'bar'))
    expect = (('a', 1), ('b', 2), ('b', 7))
    ieq(expect, actual)
    
    actual = itervalues(table, 'baz')
    expect = (True, None, False)
    ieq(expect, actual)

    actual = itervalues(table, ('foo', 'baz'))
    expect = (('a', True), ('b', None), ('b', False))
    ieq(expect, actual)


def test_values():

    table = (('foo', 'bar', 'baz'), 
             ('a', 1, True), 
             ('b', 2), 
             ('b', 7, False))

    actual = values(table, 'foo')
    expect = ('a', 'b', 'b')
    ieq(expect, actual) 
    ieq(expect, actual) 

    actual = values(table, 'bar')
    expect = (1, 2, 7)
    ieq(expect, actual) 
    ieq(expect, actual) 

    # old style signature for multiple fields, still supported
    actual = values(table, ('foo', 'bar'))
    expect = (('a', 1), ('b', 2), ('b', 7))
    ieq(expect, actual) 
    ieq(expect, actual) 

    # as of 0.24 new style signature for multiple fields
    actual = values(table, 'foo', 'bar')
    expect = (('a', 1), ('b', 2), ('b', 7))
    ieq(expect, actual)
    ieq(expect, actual)

    actual = values(table, 'baz')
    expect = (True, None, False)
    ieq(expect, actual)
    ieq(expect, actual) 


def test_valuecount():

    table = (('foo', 'bar'), ('a', 1), ('b', 2), ('b', 7))
    n, f = valuecount(table, 'foo', 'b')
    eq_(2, n)
    eq_(2./3, f) 
    
        
def test_valuecounter():

    table = (('foo', 'bar'), ('a', 1), ('b', 2), ('b', 7))
    actual = valuecounter(table, 'foo')
    expect = {'b': 2, 'a': 1}
    eq_(expect, actual) 
    
        
def test_valuecounter_shortrows():

    table = (('foo', 'bar'), ('a', 7), ('b',), ('b', 7))
    actual = valuecounter(table, 'foo')
    expect = {'b': 2, 'a': 1}
    eq_(expect, actual)
    actual = valuecounter(table, 'bar')
    expect = {7: 2, None: 1}
    eq_(expect, actual)
    actual = valuecounter(table, 'foo', 'bar')
    expect = {('a', 7): 1, ('b', None): 1, ('b', 7): 1}
    eq_(expect, actual)


def test_valuecounts():

    table = (('foo', 'bar'), ('a', 1), ('b', 2), ('b', 7))
    actual = valuecounts(table, 'foo')
    expect = (('foo', 'count', 'frequency'), ('b', 2, 2./3), ('a', 1, 1./3))
    ieq(expect, actual) 
    ieq(expect, actual) 


def test_valuecounts_shortrows():
    
    table = (('foo', 'bar'), 
             ('a', True), 
             ('x', True), 
             ('b',), 
             ('b', True), 
             ('c', False), 
             ('z', False))
    actual = valuecounts(table, 'bar')
    expect = (('bar', 'count', 'frequency'),
              (True, 3, 3./6), 
              (False, 2, 2./6), 
              (None, 1, 1./6))
    ieq(expect, actual) 
    ieq(expect, actual) 


def test_valuecounts_multifields():
    
    table = (('foo', 'bar', 'baz'), 
             ('a', True, .12), 
             ('a', True, .17),
             ('b', False, .34),
             ('b', False, .44),
             ('b',),
             ('b', False, .56))
    actual = valuecounts(table, 'foo', 'bar')
    expect = (('foo', 'bar', 'count', 'frequency'),
              ('b', False, 3, 3./6),
              ('a', True, 2, 2./6),
              ('b', None, 1, 1./6))
    ieq(expect, actual) 
    ieq(expect, actual) 

    
def test_isunique():

    table = (('foo', 'bar'), ('a', 1), ('b',), ('b', 2), ('c', 3, True))
    assert not isunique(table, 'foo')
    assert isunique(table, 'bar')
    

def test_lookup():

    t1 = (('foo', 'bar'), ('a', 1), ('b', 2), ('b', 3))
    
    # lookup one column on another
    actual = lookup(t1, 'foo', 'bar')
    expect = {'a': [1], 'b': [2, 3]}
    eq_(expect, actual)

    # test default value - tuple of whole row
    actual = lookup(t1, 'foo')  # no value selector
    expect = {'a': [('a', 1)], 'b': [('b', 2), ('b', 3)]}
    eq_(expect, actual)
    
    t2 = (('foo', 'bar', 'baz'),
          ('a', 1, True),
          ('b', 2, False),
          ('b', 3, True),
          ('b', 3, False))
    
    # test value selection
    actual = lookup(t2, 'foo', ('bar', 'baz'))
    expect = {'a': [(1, True)], 'b': [(2, False), (3, True), (3, False)]}
    eq_(expect, actual)
    
    # test compound key
    actual = lookup(t2, ('foo', 'bar'), 'baz')
    expect = {('a', 1): [True], ('b', 2): [False], ('b', 3): [True, False]}
    eq_(expect, actual)
    
    
def test_lookupone():

    t1 = (('foo', 'bar'), ('a', 1), ('b', 2), ('b', 3))
    
    # lookup one column on another under strict mode
    try:
        lookupone(t1, 'foo', 'bar', strict=True)
    except DuplicateKeyError:
        pass  # expected
    else:
        assert False, 'expected error'
        
    # lookup one column on another under, not strict 
    actual = lookupone(t1, 'foo', 'bar', strict=False)
    expect = {'a': 1, 'b': 2}  # first value wins
    eq_(expect, actual)

    # test default value - tuple of whole row
    actual = lookupone(t1, 'foo', strict=False)  # no value selector
    expect = {'a': ('a', 1), 'b': ('b', 2)}  # first wins
    eq_(expect, actual)
    
    t2 = (('foo', 'bar', 'baz'),
          ('a', 1, True),
          ('b', 2, False),
          ('b', 3, True),
          ('b', 3, False))
    
    # test value selection
    actual = lookupone(t2, 'foo', ('bar', 'baz'), strict=False)
    expect = {'a': (1, True), 'b': (2, False)}
    eq_(expect, actual)
    
    # test compound key
    actual = lookupone(t2, ('foo', 'bar'), 'baz', strict=False)
    expect = {('a', 1): True, ('b', 2): False, ('b', 3): True}  # first wins
    eq_(expect, actual)
    

def test_dictlookup():

    t1 = (('foo', 'bar'), ('a', 1), ('b', 2), ('b', 3))
    
    actual = dictlookup(t1, 'foo')
    expect = {'a': [{'foo': 'a', 'bar': 1}],
              'b': [{'foo': 'b', 'bar': 2}, {'foo': 'b', 'bar': 3}]}
    eq_(expect, actual)
    
    t2 = (('foo', 'bar', 'baz'),
          ('a', 1, True),
          ('b', 2, False),
          ('b', 3, True),
          ('b', 3, False))
    
    # test compound key
    actual = dictlookup(t2, ('foo', 'bar'))
    expect = {('a', 1): [{'foo': 'a', 'bar': 1, 'baz': True}], 
              ('b', 2): [{'foo': 'b', 'bar': 2, 'baz': False}], 
              ('b', 3): [{'foo': 'b', 'bar': 3, 'baz': True}, 
                         {'foo': 'b', 'bar': 3, 'baz': False}]}
    eq_(expect, actual)
    
    
def test_dictlookupone():

    t1 = (('foo', 'bar'), ('a', 1), ('b', 2), ('b', 3))
    
    try:
        dictlookupone(t1, 'foo', strict=True)
    except DuplicateKeyError:
        pass  # expected
    else:
        assert False, 'expected error'
        
    # relax 
    actual = dictlookupone(t1, 'foo', strict=False)
    # first wins
    expect = {'a': {'foo': 'a', 'bar': 1}, 'b': {'foo': 'b', 'bar': 2}}
    eq_(expect, actual)

    t2 = (('foo', 'bar', 'baz'),
          ('a', 1, True),
          ('b', 2, False),
          ('b', 3, True),
          ('b', 3, False))
    
    # test compound key
    actual = dictlookupone(t2, ('foo', 'bar'), strict=False)
    expect = {('a', 1): {'foo': 'a', 'bar': 1, 'baz': True}, 
              ('b', 2): {'foo': 'b', 'bar': 2, 'baz': False}, 
              ('b', 3): {'foo': 'b', 'bar': 3, 'baz': True}}  # first wins
    eq_(expect, actual)
    

def test_recordlookup():

    t1 = (('foo', 'bar'), ('a', 1), ('b', 2), ('b', 3))

    lkp = recordlookup(t1, 'foo')
    eq_([1], [r.bar for r in lkp['a']])
    eq_([2, 3], [r.bar for r in lkp['b']])


def test_recordlookupone():

    t1 = (('foo', 'bar'), ('a', 1), ('b', 2), ('b', 3))

    try:
        recordlookupone(t1, 'foo', strict=True)
    except DuplicateKeyError:
        pass  # expected
    else:
        assert False, 'expected error'

    # relax
    lkp = recordlookupone(t1, 'foo', strict=False)
    eq_(1, lkp['a'].bar)
    eq_(2, lkp['b'].bar)  # first wins


def test_rowlengths():

    table = (('foo', 'bar', 'baz'),
             ('A', 1, 2),
             ('B', '2', '3.4'),
             ('B', '3', '7.8', True),
             ('D', 'xyz', 9.0),
             ('E', None),
             ('F', 9))
    actual = rowlengths(table)
    expect = (('length', 'count'), (3, 3), (2, 2), (4, 1))
    ieq(expect, actual) 


def test_stats():

    table = (('foo', 'bar', 'baz'),
             ('A', 1, 2),
             ('B', '2', '3.4'),
             ('B', '3', '7.8', True),
             ('D', 'xyz', 9.0),
             ('E', None))

    result = stats(table, 'bar')    
    assert result['min'] == 1.0
    assert result['max'] == 3.0
    assert result['sum'] == 6.0
    assert result['count'] == 3
    assert result['errors'] == 2
    assert result['mean'] == 2.0


def test_typecounts():

    table = (('foo', 'bar', 'baz'),
             (b'A', 1, 2.),
             (b'B', u'2', 3.4),
             (u'B', u'3', 7.8, True),
             (b'D', u'xyz', 9.0),
             (b'E', 42))

    actual = typecounts(table, 'foo')
    if PY2:
        expect = (('type', 'count', 'frequency'),
                  ('str', 4, 4./5),
                  ('unicode', 1, 1./5))
    else:
        expect = (('type', 'count', 'frequency'),
                  ('bytes', 4, 4./5),
                  ('str', 1, 1./5))
    ieq(expect, actual)

    actual = typecounts(table, 'bar')
    if PY2:
        expect = (('type', 'count', 'frequency'),
                  ('unicode', 3, 3./5),
                  ('int', 2, 2./5))
    else:
        expect = (('type', 'count', 'frequency'),
                  ('str', 3, 3./5),
                  ('int', 2, 2./5))
    ieq(expect, actual)

    actual = typecounts(table, 'baz') 
    expect = (('type', 'count', 'frequency'), 
              ('float', 4, 4./5), 
              ('NoneType', 1, 1./5))
    ieq(expect, actual)


def test_typeset():

    table = (('foo', 'bar', 'baz'),
             (b'A', 1, u'2'),
             (b'B', '2', u'3.4'),
             (b'B', '3', u'7.8', True),
             (u'D', u'xyz', 9.0),
             (b'E', 42))

    actual = typeset(table, 'foo')
    if PY2:
        expect = set([str, unicode])
    else:
        expect = set([bytes, str])
    eq_(expect, actual)


def test_parsecounts():

    table = (('foo', 'bar', 'baz'),
             ('A', 'aaa', 2),
             ('B', '2', '3.4'),
             ('B', '3', '7.8', True),
             ('D', '3.7', 9.0),
             ('E', 42))

    actual = parsecounts(table, 'bar') 
    expect = (('type', 'count', 'errors'), ('float', 3, 1), ('int', 2, 2))
    ieq(expect, actual)
    
    
def test_numparser():

    parsenumber = numparser()
    assert parsenumber('1') == 1
    assert parsenumber('1.0') == 1.0
    assert parsenumber(str(maxint + 1)) == maxint + 1
    assert parsenumber('3+4j') == 3 + 4j
    assert parsenumber('aaa') == 'aaa'
    assert parsenumber(None) is None
    
    
def test_numparser_strict():

    parsenumber = numparser(strict=True)
    assert parsenumber('1') == 1
    assert parsenumber('1.0') == 1.0
    assert parsenumber(str(maxint + 1)) == maxint + 1
    assert parsenumber('3+4j') == 3 + 4j
    try:
        parsenumber('aaa')
    except ValueError:
        pass  # expected
    else:
        assert False, 'expected exception'
    try:
        parsenumber(None)
    except TypeError:
        pass  # expected
    else:
        assert False, 'expected exception'
    
    
def test_stringpatterns():
    
    table = (('foo', 'bar'),
             ('Mr. Foo', '123-1254'),
             ('Mrs. Bar', '234-1123'),
             ('Mr. Spo', '123-1254'),
             ('Mr. Baz', '321 1434'),
             ('Mrs. Baz', '321 1434'),
             ('Mr. Quux', '123-1254-XX'))
    
    actual = stringpatterns(table, 'foo')
    expect = (('pattern', 'count', 'frequency'), 
              ('Aa. Aaa', 3, 3./6), 
              ('Aaa. Aaa', 2, 2./6), 
              ('Aa. Aaaa', 1, 1./6))
    ieq(expect, actual) 
    
    actual = stringpatterns(table, 'bar')
    expect = (('pattern', 'count', 'frequency'), 
              ('999-9999', 3, 3./6), 
              ('999 9999', 2, 2./6),
              ('999-9999-AA', 1, 1./6))
    ieq(expect, actual) 
    

def test_diffheaders():
    
    table1 = (('foo', 'bar', 'baz'),
              ('a', 1, .3))

    table2 = (('baz', 'bar', 'quux'),
              ('a', 1, .3))
    
    add, sub = diffheaders(table1, table2)
    eq_(set(['quux']), add)
    eq_(set(['foo']), sub)
    
    
def test_diffvalues():
    
    table1 = (('foo', 'bar'),
              ('a', 1),
              ('b', 3))

    table2 = (('bar', 'foo'),
              (1, 'a'),
              (3, 'c'))
    
    add, sub = diffvalues(table1, table2, 'foo')
    eq_(set(['c']), add)
    eq_(set(['b']), sub)
    
    
def test_laxparsers():
    
    p1 = datetimeparser('%Y-%m-%dT%H:%M:%S')
    try:
        p1('2002-12-25 00:00:00')
    except ValueError:
        pass
    else:
        assert False, 'expected exception'
    
    p2 = datetimeparser('%Y-%m-%dT%H:%M:%S', strict=False)
    try:
        v = p2('2002-12-25 00:00:00')
    except ValueError:
        assert False, 'did not expect exception'
    else:
        eq_('2002-12-25 00:00:00', v)
    
    
def test_columns():
    
    table = [['foo', 'bar'], ['a', 1], ['b', 2], ['b', 3]]
    cols = columns(table)
    eq_(['a', 'b', 'b'], cols['foo'])
    eq_([1, 2, 3], cols['bar'])


def test_facetcolumns():
    
    table = [['foo', 'bar', 'baz'], 
             ['a', 1, True], 
             ['b', 2, True], 
             ['b', 3]]
    
    fc = facetcolumns(table, 'foo')
    eq_(['a'], fc['a']['foo'])
    eq_([1], fc['a']['bar'])
    eq_([True], fc['a']['baz'])
    eq_(['b', 'b'], fc['b']['foo'])
    eq_([2, 3], fc['b']['bar'])
    eq_([True, None], fc['b']['baz'])
    
    
def test_isordered():
    
    table1 = (('foo', 'bar', 'baz'), 
              ('a', 1, True), 
              ('b', 3, True), 
              ('b', 2))
    assert isordered(table1, key='foo')
    assert not isordered(table1, key='foo', reverse=True)
    assert not isordered(table1, key='foo', strict=True)

    table2 = (('foo', 'bar', 'baz'), 
              ('b', 2, True), 
              ('a', 1, True), 
              ('b', 3))
    assert not isordered(table2, key='foo')

    table3 = (('foo', 'bar', 'baz'), 
              ('a', 1, True), 
              ('b', 2, True), 
              ('b', 3))
    assert isordered(table3, key=('foo', 'bar'))
    assert isordered(table3)

    table4 = (('foo', 'bar', 'baz'), 
              ('a', 1, True), 
              ('b', 3, True), 
              ('b', 2))
    assert not isordered(table4, key=('foo', 'bar'))
    assert not isordered(table4)

    table5 = (('foo', 'bar', 'baz'), 
              ('b', 3, True), 
              ('b', 2),
              ('a', 1, True)) 
    assert not isordered(table5, key='foo')
    assert isordered(table5, key='foo', reverse=True)
    assert not isordered(table5, key='foo', reverse=True, strict=True)


def test_rowgroupby():
    
    table = (('foo', 'bar', 'baz'), 
             ('a', 1, True), 
             ('b', 2, True), 
             ('b', 3))
    
    # simplest form

    g = rowgroupby(table, 'foo')

    key, vals = next(g)
    vals = list(vals)
    eq_('a', key)
    eq_(1, len(vals))
    eq_(('a', 1, True), vals[0])

    key, vals = next(g)
    vals = list(vals)
    eq_('b', key)
    eq_(2, len(vals))
    eq_(('b', 2, True), vals[0])
    eq_(('b', 3), vals[1])

    # specify value
    
    g = rowgroupby(table, 'foo', 'bar')
    
    key, vals = next(g)
    vals = list(vals)
    eq_('a', key)
    eq_(1, len(vals))
    eq_(1, vals[0])

    key, vals = next(g)
    vals = list(vals)
    eq_('b', key)
    eq_(2, len(vals))
    eq_(2, vals[0])
    eq_(3, vals[1])

    # callable key
    
    g = rowgroupby(table, lambda r: r['foo'], lambda r: r['baz'])
    
    key, vals = next(g)
    vals = list(vals)
    eq_('a', key)
    eq_(1, len(vals))
    eq_(True, vals[0])

    key, vals = next(g)
    vals = list(vals)
    eq_('b', key)
    eq_(2, len(vals))
    eq_(True, vals[0])
    eq_(None, vals[1])  # gets padded


def test_progress():
    # make sure progress doesn't raise exception
    table = (('foo', 'bar', 'baz'),
             ('a', 1, True),
             ('b', 2, True),
             ('b', 3))
    nrows(progress(table))