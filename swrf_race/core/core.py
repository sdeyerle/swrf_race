from datetime import datetime

class DBField(object):

  def __init__(self, db_conn, name, dtype='std', cls=None, value=None):

    self.name  = name 
    self.dtype = dtype
    self.cls = cls
    self.db_conn = db_conn

    if value != None:
      self._value = value
    else:
      self._value = None

    self.modified = False

  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, value):
    set_value(self, value, modified=True)

  def set_value(self, value, modified=True):
    if self.dtype == 'std':
      if self._value != value:
        self._value = value
        self.modified = True
    elif self.dtype == 'foreign_key':
      self._value = self.cls(self.db_conn, value)
      self.modified = True
    elif self.dtype == 'date':
      self._value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
      self.modified = True
    else:
      raise KeyError('Invalid type specified to DBField')

  def __repr__(self):
    return 'DBField({}, {}, {})'.format(self.name, self.dtype, self.value)

  def __str__(self):
    return '{}: {}'.format(self.name, self.value)


class DBRecord(object):

  def __init__(self, db_conn, table_name, id_field, id_val=None):
    if type(db_conn) == int:
      test = 1/0
    self._db = db_conn;
    self._table = table_name
    self._id_field = id_field
    self._fields = {}

    self._id_val = id_val

  def add_field(self, name, dtype='std', cls=None, attr_name=None):
    if attr_name == None:
      attr_name = name

    self._fields[name] = DBField(self._db, name, dtype, cls)
    setattr(self, attr_name, self._fields[name])

  def fetch(self):

    query = 'SELECT {} FROM {} WHERE {} = ?'.format(
      ', '.join([col for col in self._fields]),
      self._table,
      self._id_field);

    data = (self._id_val,)

    results = self._db.cursor().execute(query, data)
    data = results.fetchone()

    if data == None:
      raise KeyError('Failed to find {}={} in table {}'.format
        (self._id_field, self._id_val, self._table))
    else:
      num_fields = len(self._fields)

      for idx, col in enumerate(self._fields):
        self._fields[col].set_value(data[idx], modified=False)
        if self._fields[col].dtype == 'foreign_key':
          self._fields[col].value.fetch()
          

  def __str__(self):
    output = '{' + ', '.join([str(f) for k, f in self._fields.items()]) + '}'
    return output

class Race(DBRecord):

  def __init__(self, db_conn, db_id=None):
    super().__init__(db_conn, 'race', 'raceid', db_id)

    self.add_field('name')
    self.add_field('date_time', dtype='date')

class Boat(DBRecord):

  def __init__(self, db_conn, db_id=None):
    super().__init__(db_conn, 'boat', 'boatid', db_id)

    self.add_field('name')
    self.add_field('sail_number')
    self.add_field('skipperid', dtype='foreign_key', cls=Person, attr_name='skipper')

class Person(DBRecord):

  def __init__(self, db_conn, db_id=None):
    super().__init__(db_conn, 'person', 'personid', db_id)

    self.add_field('last_name')
    self.add_field('first_name')

  def __str__(self):
    return str(self.first_name.value) + ' ' + str(self.last_name.value)
