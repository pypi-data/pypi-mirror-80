import json

import cro_validate.classes.definition_classes as Definitions
from cro_validate.classes.configuration_classes import Config
from cro_validate.enum import DataType


class DefaultExamplesProvider:
	def get_examples(self, definition, **kw):
		return [1]
		# TODO: Triage/resolve these. Some are CRO specific...
		#if definition.data_type == DataType.Boolean:
		#	return [True]
		#if definition.data_format == DataFormat.Email:
		#	return ['test@crosoftware.net']
		#if definition.data_format == DataFormat.PhoneNumber:
		#	return ['+1 (360) 123-6543']
		#if definition.data_format == DataFormat.IntResourceId:
		#	return [1]
		#if definition.data_format == DataFormat.UuidResourceId:
		#	return ['ddf936ae-f5a3-4210-977c-0ac8583040f9']
		#if definition.data_format == DataFormat.Url:
		#	return ['https://test.url']
		#if definition.data_format == DataFormat.DateTime:
		#	return ['2049-10-31T11:32:38.390000']
		#if definition.data_format == DataFormat.Uuid:
		#	return ['9f34f340-54d2-4403-a53b-d8017a64734f']
		#return None

class _Empty:
	pass


def isempty(v):
	if isinstance(v, _Empty):
		return True
	return False


class PrimitiveValueGenerator:
	def __init__(self, name, definition, values):
		if len(values) < 1:
			values = definition.examples
		if values is None:
			raise Config.exception_factory.create_internal_error(name, 'Missing examples.')
		self.name = name
		self.values = values
		self.index = 0

	def first(self):
		return self.values[0]

	def next(self):
		if self.index < len(self.values):
			next_value = self.values[self.index]
			self.index = self.index + 1
			return next_value
		return _Empty()

	def __iter__(self):
		return self

	def __next__(self):
		result = self.next()
		if isempty(result):
			raise StopIteration()
		return result


# TODO: Add dependency vector in dependency sort order
#       for dependent generators (e.g. OneOf).
# TODO: Add more reliable perm indexing (seen).
class ObjectValueGenerator:
	def __init__(self, field_name, definition, values):
		# assert definition is object
		self.name = field_name
		self.generators = {}
		self.seen = set()
		self.processed = set()
		self.selected = _Empty()
		for k in definition.validator.list_field_names():
			field_definition = Definitions.Index.get(definition.validator.get_field_definition_name(k))
			given_values = []
			if k in values:
				given_values = values[k]
			elif not definition.validator.is_field_required(k):
				continue
			else:
				raise Config.exception_factory.create_internal_error(k, 'Required field missing examples.' + str(values) + ' ' + field_name)
			if field_definition.data_type == DataType.Object:
				self.generators[k] = ObjectValueGenerator(k, field_definition, given_values)
			elif field_definition.data_type == DataType.Array:
				self.generators[k] = ArrayGenerator(k, field_definition, given_values)
			else:
				self.generators[k] = PrimitiveValueGenerator(k, field_definition, given_values)
		self.first_value = self.next()

	def first(self):
		if not isinstance(self.first_value, _Empty):
			return self.first_value
		self.first_value = self.next()
		return self.first_value

	def _select_next(self):
		selected = _Empty()
		for k in self.generators:
			if k in self.processed:
				continue
			selected = k
			self.processed.add(k)
			break
		return selected

	def next(self):
		result = {}
		first = False
		if isempty(self.selected):
			first = True
			self.selected = self._select_next()
		if isempty(self.selected):
			return _Empty()
		for k in self.generators:
			if first is False and k == self.selected:
				result[k] = self.generators[self.selected].next()
				if isempty(result[k]):
					self.selected = _Empty()
					return self.next()
			else:
				result[k] = self.generators[k].first()
		return result

	def __iter__(self):
		return self

	def __next__(self):
		result = self.next()
		if isempty(result):
			raise StopIteration()
		s = json.dumps(result, sort_keys=True)
		if s in self.seen:
			return self.__next__()
		self.seen.add(s)
		return result


class ArrayGenerator:
	def _create_generator(self, field_name, definition, vector):
		generator = _Empty()
		if definition.data_type == DataType.Object:
			generator = ObjectValueGenerator(field_name, definition, vector)
		elif definition.data_type == DataType.Array:
			generator = ArrayGenerator(field_name, definition, vector)
		else:
			generator = PrimitiveValueGenerator(field_name, definition, vector)
		return generator

	def __init__(self, field_name, definition, values):
		self.name = field_name
		self.generators = []
		self.current_index = 0
		self.seen = set()
		item_definition = definition.data_format
		if isinstance(item_definition, str):
			item_definition = Definitions.Index.get(item_definition)
		for vector in values:
			generator = self._create_generator(field_name, item_definition, vector)
			self.generators.append(generator)
		self.first_value = self.first()

	def first(self):
		i = 0
		self.first_value = []
		for g in self.generators:
			v = g.first()
			if isempty(v):
				raise Config.exception_factory.create_internal_error(g.name, 'Missing values.')
			self.first_value.append(v)
			i = i + 1
		self.current_index = 0
		return self.first_value

	def _next(self):
		result = []
		variant = _Empty()
		i = 0
		for g in self.generators:
			if isempty(variant) and i >= self.current_index:
				v = g.next()
				if isempty(v):
					result.append(self.first_value[i])
				else:
					result.append(v)
					variant = v
					self.current_index = i
			else:
				result.append(self.first_value[i])
			i = i + 1
		if isempty(variant):
			self.first_value = _Empty()
			return self.first_value
		return result

	def next(self):
		result = self._next()
		if isempty(result):
			return result
		s = json.dumps(result, sort_keys=True)
		if s in self.seen:
			return self.next()
		self.seen.add(s)
		return result

	def __iter__(self):
		return self

	def __next__(self):
		result = self.next()
		if isempty(result):
			raise StopIteration()
		return result


# TODO: Currently N-Wise where N=1. Support N=x?
# https://en.wikipedia.org/wiki/All-pairs_testing
class ExampleGenerator:
	def __init__(self, definition, given_values={}, **kw):
		self.definition = definition
		if isinstance(self.definition, str):
			self.definition = Definitions.Index.get(definition)
		if self.definition.data_type == DataType.Object:
			self.generator = ObjectValueGenerator(self.definition.name, self.definition, given_values)
		elif self.definition.data_type == DataType.Array:
			self.generator = ArrayGenerator(self.definition.name, self.definition, given_values)
		else:
			self.generator = PrimitiveValueGenerator(self.definition.name, self.definition, given_values)

	def next(self):
		return self.__next__()

	def __iter__(self):
		return self

	def __next__(self):
		result = self.generator.__next__()
		return result


class DefaultExampleGeneratorFactory:
	def create(self, definition, **kw):
		g = ExampleGenerator(definition, **kw)
		return g