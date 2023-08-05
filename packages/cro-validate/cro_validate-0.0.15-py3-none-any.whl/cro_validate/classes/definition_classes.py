import importlib

from enum import Enum
from cro_validate.enum import DataType
from cro_validate.classes.configuration_classes import Config
import cro_validate.classes.parameter_classes as Parameters
import cro_validate.classes.schema_classes as Schemas
import cro_validate.classes.name_strategy_classes as NameStrategies
import cro_validate.classes.util_classes as Utils


class Meta:
	def initialize(self, definition, **kw):
		raise NotImplementedError()

	def to_json_dict(self):
		return {}


class DefaultMeta(Meta):
	def __init__(self, component_name_strategy=NameStrategies.DefaultComponentNameStrategy()):
		self.component_name_strategy = component_name_strategy
		self.schema_name = None
		self.component_name = None

	def initialize(self, definition, component_name_suffix='Model', display_name=None):
		if definition.is_object():
			self.schema_name = definition.data_format.model_name
			self.component_name = self.schema_name
		elif definition.is_array():
			self.component_name = definition.data_format
		else:
			self.component_name = self.component_name_strategy.create_name(definition, component_name_suffix, display_name)

		def to_json_dict(self):
			return {
				'component_name_strategy': self.component_name_strategy.to_json_dict()
			}


class Definition:
	'''Def
	'''

	def to_json_dict(self):
		default_value = self.default_value
		if self.has_default_value() is False:
			default_value = None
		default_value_type = Utils.ClassName.class_fqn(self.default_value)
		meta = None
		if self.meta is not None:
			meta = self.meta.to_json_dict()
		meta_type = Utils.ClassName.class_fqn(self.meta)
		dependency_resolver = None
		if self.dependency_resolver is not None:
			dependency_resolver = self.dependency_resolver.to_json_dict()
		dependency_resolver_type = Utils.ClassName.class_fqn(self.dependency_resolver)
		fmt = None
		if self.data_format is not None:
			if isinstance(self.data_format, Enum):
				fmt = self.data_format.name
			elif isinstance(self.data_format, Schemas.Schema):
				fmt = self.data_format.to_json_dict()
			elif isinstance(self.data_format, set):
				fmt = [f for f in self.data_format]
				fmt.sort()
			else:
				fmt = self.data_format
		fmt_type = Utils.ClassName.class_fqn(self.data_format)
		aliases = [a for a in self.aliases]
		aliases.sort()
		return {
				#'name': self.name,
				'aliases': aliases,
				'description': self.description,
				'data_type': self.data_type.name,
				'data_format': fmt,
				'data_format_type': fmt_type,
				'default_value': default_value,
				'default_value_type': default_value_type,
				'examples': self.examples,
				'nullable': self.nullable,
				'deprecated': self.deprecated,
				'is_internal': self.is_internal,
				'rules': [{'type':Utils.ClassName.class_fqn(r), 'config':r.to_json_dict()} for r in self.rules],
				'meta': meta,
				'meta_type': meta_type,
				'dependency_resolver': dependency_resolver,
				'dependency_resolver_type': dependency_resolver_type
			}

	def __init__(
				self,
				name,
				aliases,
				description,
				data_type,
				data_format,
				default_value,
				examples,
				nullable,
				deprecated,
				is_internal,
				rules,
				meta,
				dependency_resolver
			):
		self.name = name
		self.aliases = aliases
		self.description = description
		self.data_type = data_type
		self.data_format = data_format
		self.default_value = default_value
		self.examples = examples
		self.nullable = nullable
		self.deprecated = deprecated
		self.is_internal = is_internal
		self.dependencies = set()
		self.rules = rules
		self.meta = meta
		self.dependency_resolver = dependency_resolver
		# Name
		######
		self.name = Config.definition_name_strategy.create_name(self, self.name)
		if self.name is None:
			ConfigApi.exception_factory.create_input_error(
					'<unset>', 'Definition name cannot be None (description={0})'.format(self.description)
				)
		# Aliases
		#########
		if isinstance(aliases, str):
			self.aliases = {aliases}
		# Nullable
		##########
		if self.default_value is None:
			self.nullable = True
		# Default Value
		###############
		if isinstance(self.default_value, Utils.DataDefinitionDefaultValue):
			if self.nullable is True:
				self.default_value = None
		# Data Format
		#############
		if self.data_type is DataType.Object and isinstance(self.data_format, str):
			format_definition = Index.get(self.data_format)
			self.data_format = format_definition.data_format
		elif self.data_type is DataType.OneOf:
			self.data_format = dependency_resolver.list_dependent_definition_names(self.name)
		# Validator
		###########
		if self.is_object():
			self.validator = self._get_obj_validator()
		elif self.is_array():
			self.validator = self._validate_array	
		else:
			self.validator = self._assign_value
		# Dependencies
		##############
		self.dependencies = set(self.dependency_resolver.list_dependency_fields(self.name))
		# Examples
		##########
		if not self.examples:
			self.examples = Config.default_examples_provider.get_examples(self)
		if not self.is_object() and not self.is_array():
			if not self.examples:
				raise Config.exception_factory.create_input_error(self.name, 'Missing examples')
		# Meta
		######
		self.meta.initialize(self)

	def _get_obj_model_validator(self):
		display_name = self.data_format.model_name
		if self.data_format.display_name is not None:
			display_name = str(self.data_format.display_name)
		validator = Schemas.ModelValidator(
				name=display_name,
				allow_unknown_fields=self.data_format.allow_unknown_fields,
				case_sensitive=self.data_format.case_sensitive
			)
		required = set()
		optional = set()
		ignored = set()
		unvalidated = set()
		definition_names = {}
		input_names = {}
		output_names = {}
		dependencies = {}
		default_values = {}
		model = self.data_format.model
		if model is None:
			raise Config.exception_factory.create_internal_error(self.data_format.model_name, 'Missing model')
		fields = {}
		if isinstance(model, dict):
			fields = model
		else:
			for name in dir(model):
				if name.startswith('_'):
					continue
				fields[name] = getattr(model, name)
		for name in fields:
			field_definition = fields[name]
			if field_definition is None:
				field_definition = Schemas.Field()
			if field_definition.required:
				required.add(name)
			else:
				optional.add(name)
			if field_definition.ignored:
				ignored.add(name)
			if field_definition.unvalidated:
				unvalidated.add(name)
			if field_definition.definition_name:
				definition_names[name] = field_definition.definition_name
			if field_definition.output_name:
				output_names[name] = field_definition.output_name
			if field_definition.input_name:
				input_names[name] = field_definition.input_name
			if not isinstance(field_definition.default_value, Utils.DataDefinitionDefaultValue):
				default_values[name] = field_definition.default_value
			definition_name = name
			if field_definition.definition_name is not None:
				definition_name = field_definition.definition_name
			if field_definition.unvalidated is not True:
				dependencies[name] = Index.get(definition_name).dependencies
		validator.add_spec(
				required=required,
				optional=optional,
				ignored=ignored,
				unvalidated=unvalidated,
				definition_names=definition_names,
				input_names=input_names,
				output_names=output_names,
				dependencies=dependencies,
				default_values=default_values)
		return validator

	def _get_obj_validator(self):
		model_validator = self._get_obj_model_validator()
		validator = Schemas.Validator(
				self.name,
				model_validator
			)
		return validator

	def _validate_array(self, results, field_fqn, field_name, definition, values, dependent_values):
		if not isinstance(values, list):
			raise Config.exception_factory.create_input_error(field_fqn, 'Expected array, received: {0}'.format(type(values)))
		items = []
		i = 0
		for entry in values:
			item = Index.validate_input(None, field_fqn + '[' + str(i) + ']', field_name, self.data_format, entry, dependent_values)
			items.append(item[field_name])
			i = i + 1
		results[field_name] = items

	def _assign_value(self, results, field_fqn, field_name, definition, value, dependent_values):
		results[field_name] = value

	def validate(self, results, field_fqn, field_name, definition, value, dependent_values):
		'''
		The validate func
		'''
		try:
			if not self.validator:
				raise Config.exception_factory.create_internal_error(self.name, "Missing validator.")
			if field_name is None:
				field_name = self.name
			if field_fqn is None:
				field_fqn = field_name
				if self.data_type == DataType.Object:
					field_fqn = self.validator.model_validator.name
			normalized = Parameters.Index()
			dependent_definition_name = self.dependency_resolver.get_dependent_definition(
					field_fqn,
					dependent_values
				)
			if value is None:
				if self.nullable is True:
					results[field_name] = None
					return
				else:
					raise Config.exception_factory.create_input_error(field_name, 'Not nullable.')
			if dependent_definition_name is not None:
				Index.validate_input(
						results,
						field_fqn,
						field_name,
						dependent_definition_name,
						value,
						dependent_values
					)
			else:
				self.validator(normalized, field_fqn, field_name, self, value, dependent_values)
			for rule in self.rules:
				normalized[field_name] = rule.execute(field_fqn, normalized[field_name])
			results.update(normalized)
		except Exception as ex:
			if self.is_internal:
				raise Config.exception_factory.create_internal_error(ex.source, ex.message)
			else:
				raise ex

	def has_default_value(self):
		if isinstance(self.default_value, Utils.DataDefinitionDefaultValue):
			return False
		return True

	def get_default_value(self, name):
		if not self.has_default_value():
			raise Config.exception_factory.create_internal_error(self.name, 'No default value configured')
		return self.default_value

	def get_name(self):
		return self.name

	def get_description(self, delim=' '):
		result = self.description
		if self.rules is not None and len(self.rules) > 0:
			result = result + delim + delim.join([rule.get_description() for rule in self.rules])
		return result

	def get_aliases(self):
		return self.aliases

	def is_array(self):
		if self.data_type == DataType.Array:
			return True
		return False

	def is_object(self):
		if self.data_type == DataType.Object:
			return True
		return False

	def is_primitive(self):
		if self.is_object() or self.is_array():
			return False
		return True

	def is_internal(self):
		return self.is_internal

class DependentDefinitionResolver:
	def list_dependent_definition_names(self, fqn):
		raise NotImplementedError()

	def get_dependent_definition(self, fqn, dependent_values):
		raise NotImplementedError()

	def list_dependency_fields(self, fqn):
		raise NotImplementedError()


class DefaultResolver(DependentDefinitionResolver):
	def list_dependent_definition_names(self, fqn):
		return []

	def to_json_dict(self):
		return {}

	def get_dependent_definition(self, fqn, dependent_values):
		return None

	def list_dependency_fields(self, fqn):
		return []

	def to_json_dict(self):
		return {}


class _OneOfResolverPlayback:
	def __init__(self, fqn, dependency_state, dependent_definition_name):
		self.fqn = fqn
		self.dependency_state = dependency_state
		self.dependent_definition_name = dependent_definition_name

	def to_json_dict(self):
		return {
				'fqn': self.fqn,
				'dependency_state': self.dependency_state,
				'dependent_definition_name': self.dependent_definition_name
			}


class OneOfResolver(DependentDefinitionResolver):
	def __init__(self, playback=[]):
		self._dependencies = set()
		self._dependency_idx = {}
		self._dependency_order = []
		self._permutations = []
		self._serialize_playback = []
		for entry in playback:
			self.index_dependent_definition(
					entry['fqn'],
					entry['dependency_state'],
					entry['dependent_definition_name']
				)

	def to_json_dict(self):
		return {
				'playback': [entry.to_json_dict() for entry in self._serialize_playback]
			}

	def _update_dependency_idx_order(self, fqn, keys):
		diff = self._dependencies.difference(keys)
		if len(diff) > 0:
			raise Config.exception_factory.create_internal_error(fqn, 'Permutation keys must match dependencies.')
		self._dependencies.update([k for k in keys])
		for k in keys:
			if k in self._dependency_order:
				continue
			self._dependency_order.append(k)
		self._dependency_order.sort()

	def _index_permutation(self, fqn, permutation, value):
		self._permutations.append(permutation)
		idx = self._dependency_idx
		for k in self._dependency_order[:-1]:
			state = permutation[k]
			if state not in idx:
				idx[state] = {}
			idx = idx[state]
		state = permutation[self._dependency_order[-1]]
		if state in idx:
			raise Config.exception_factory.create_internal_error(fqn, 'Cannot re-index a permutation.')
		idx[state] = value

	def _get_permutation_value(self, fqn, permutation):
		idx = self._dependency_idx
		last_index = len(self._dependency_order) - 1
		for i in range(len(self._dependency_order)):
			k = self._dependency_order[i]
			if k not in permutation:
				raise Config.exception_factory.create_internal_error(
						fqn,
						'k not in permutation ({0})'.fromat(permutation)
					)
			state = permutation[k]
			if state not in idx:
				raise Config.exception_factory.create_internal_error(
						fqn,
						'Unknown permutation value (k={0} p={2}).'.format(k, state, permutation)
					)
			if i == last_index:
				return idx[state]
			idx = idx[state]
		return None

	def list_dependent_definition_names(self, fqn):
		result = set()
		for p in self._permutations:
			name = self._get_permutation_value(fqn, p)
			result.add(name)
		return result

	def index_dependent_definition(self, fqn, dependency_state, dependent_definition_name):
		self._update_dependency_idx_order(fqn, dependency_state.keys())
		self._index_permutation(fqn, dependency_state, dependent_definition_name)
		self._serialize_playback.append(_OneOfResolverPlayback(fqn, dependency_state, dependent_definition_name))

	def get_dependent_definition(self, fqn, dependent_values):
		name = self._get_permutation_value(fqn, dependent_values)
		return name

	def list_dependency_fields(self, fqn):
		return self._dependencies


class DefinitionJsonDeserializer:
	def _get_dict_value(self, idx, k, default_value=Utils.DataDefinitionDefaultValue()):
		if k in idx:
			return idx[k]
		return default_value

	def _set(self, src, tgt, k, default_value=Utils.DataDefinitionDefaultValue()):
			v = self._get_dict_value(src, k, default_value)
			if isinstance(v, Utils.DataDefinitionDefaultValue):
				return
			tgt[k] = v

	def _deserialize_schema_field(self, root, name, obj):
		kw = {}
		if obj['default_value_type'] != 'cro_validate.classes.util_classes.DataDefinitionDefaultValue':
			kw['default_value'] = self._instantiate(obj['default_value_type'], obj['default_value'])
		else:
			kw['default_value'] = Utils.DataDefinitionDefaultValue()
		kw['definition_name'] = obj['definition_name']
		if kw['definition_name'] is None:
			kw['definition_name'] = name
		if not Index.exists(kw['definition_name']):
			dependent_definition_profile = self.deserialize(root, kw['definition_name'])
			Index.register_definition(**dependent_definition_profile)
		self._set(obj, kw, 'dependencies')
		self._set(obj, kw, 'ignored')
		self._set(obj, kw, 'input_name')
		self._set(obj, kw, 'output_name')
		self._set(obj, kw, 'required')
		self._set(obj, kw, 'unvalidated')
		if isinstance(kw['dependencies'], list):
			kw['dependencies'] = set(kw['dependencies'])
		field = Schemas.Field(**kw)
		return field
		
	def _deserialize_schema(self, root, obj):
		kw = {}
		self._set(obj, kw, 'allow_unknown_fields')
		self._set(obj, kw, 'case_sensitive')
		self._set(obj, kw, 'display_name')
		self._set(obj, kw, 'model_name')
		self._set(obj, kw, 'model')
		model = {}
		for name in obj['model']:
			field = self._deserialize_schema_field(root, name, obj['model'][name])
			model[name] = field
		kw['model'] = model
		schema = Schemas.Schema(**kw)
		return schema

	def _instantiate(self, fqn, *args, **kw):
		module_name, class_name = Utils.ClassName.class_fqn_parts(fqn)
		if module_name == 'builtins' and class_name == 'NoneType':
			return None
		module = importlib.import_module(module_name)
		_class = getattr(module, class_name)
		if isinstance(_class, type(Enum)):
			result = _class[args[0]]
		else:
			result = _class(*args, **kw)
		return result

	def _deserialize_rule(self, root, obj):
		rule = self._instantiate(obj['type'], **obj['config'])
		return rule

	def deserialize(self, root, name):
		kw = {}
		namespace = {k:k for k in root}
		for k in root:
			for k1 in root[k]['aliases']:
				namespace[k1] = k
		obj = root[namespace[name]]
		# Data Format
		#############
		kw['data_type'] = DataType[obj['data_type']]
		if obj['data_format_type'] == 'cro_validate.classes.schema_classes.Schema':
			kw['data_format'] = self._deserialize_schema(root, obj['data_format'])
		else:
			kw['data_format'] = self._instantiate(obj['data_format_type'], obj['data_format'])
		# Default Value
		###############
		if obj['default_value_type'] == 'builtins.NoneType':
			kw['default_value'] = None
		elif obj['default_value_type'] != 'cro_validate.classes.util_classes.DataDefinitionDefaultValue':
			kw['default_value'] = self._instantiate(obj['default_value_type'], obj['default_value'])
		else:
			kw['default_value'] = Utils.DataDefinitionDefaultValue()
		# Meta
		######
		kw['meta'] = self._instantiate(obj['meta_type'], **obj['meta'])
		# Resolver
		##########
		kw['dependency_resolver'] = self._instantiate(obj['dependency_resolver_type'], **obj['dependency_resolver'])
		# Rules
		#######
		rules = []
		for rule in obj['rules']:
			rule_obj = self._deserialize_rule(obj, rule)
			rules.append(rule_obj)
		kw['rules'] = rules
		# Aliases
		#########
		kw['aliases'] = set(obj['aliases'])
		# Simple
		########
		kw['name'] = name
		self._set(obj, kw, 'description', '')
		self._set(obj, kw, 'examples', [])
		self._set(obj, kw, 'nullable', False)
		self._set(obj, kw, 'deprecated', False)
		self._set(obj, kw, 'is_internal', False)
		return kw


class Index:
	_idx = {}

	def get(definition_or_name):
		if isinstance(definition_or_name, Definition):
			return definition_or_name
		definition_name = str(definition_or_name)
		resolved = Config.definition_name_resolver.resolve(Index._idx, definition_name)
		if resolved is None:
			raise Config.exception_factory.create_input_error(definition_name, 'Definition name resolution failed (Unknown definition name).')
		return Index._idx[resolved]

	def exists(name):
		resolved = Config.definition_name_resolver.resolve(Index._idx, name)
		if resolved is None:
			return False
		return True

	def as_dict():
		return Index._idx

	def to_json_dict():
		aliases = set()
		keys = [k for k in Index.as_dict()]
		keys.sort()
		for k in keys:
			definition = Index.get(k)
			aliases.update(definition.aliases)
		result = {k:Index.get(k).to_json_dict() for k in keys if k not in aliases}
		return result

	def from_json_dict(root):
		deserializer = DefinitionJsonDeserializer()
		for k in root:
			if Index.exists(k):
				continue
			profile = deserializer.deserialize(root, k)
			Index.register_definition(**profile)

	def register_definition(
				name,
				aliases,
				description,
				data_type,
				data_format,
				default_value,
				examples,
				nullable,
				deprecated,
				is_internal,
				rules,
				meta,
				dependency_resolver
			):
		definition = Definition(
				name=name,
				aliases=aliases,
				description=description,
				data_type=data_type,
				data_format=data_format,
				default_value=default_value,
				examples=examples,
				nullable=nullable,
				deprecated=deprecated,
				is_internal=is_internal,
				rules=rules,
				meta=meta,
				dependency_resolver=dependency_resolver
			)
		definition_name = definition.get_name()
		names = set()
		names.add(definition_name)
		if isinstance(aliases, str):
			names.add(aliases)
		else:
			names.update(aliases)
		for entry in names:
			if definition_name in Index._idx:
				raise Config.exception_factory.create_internal_error(definition_name, 'Input definiton already exists.')
		for entry in names:
			Index._idx[entry] = definition
		return definition

	def validate_inputs(validated, **kw):
		results = Parameters.Index.ensure(validated)
		for name in kw:
			Index.validate_input(results, name, name, name, kw[name])
		return results

	def validate_input(validated, field_fqn, field_name, definition_or_name, value, dependent_values={}):
		definition = Index.get(definition_or_name)
		results = Parameters.Index.ensure(validated)
		definition.validate(results, field_fqn, field_name, definition, value, dependent_values)
		return results

	def ensure_alias(name, alias):
		definition = Index.get(name)
		if alias not in Index._idx:
			Index._idx[alias] = definition

	def list_definitions():
		result = [k for k in Index._idx]
		result.sort()
		return result

	def list_dependent_definitions(definition_name):
		results = set()
		definition = Index.get(definition_name)
		if definition.data_type == DataType.Object:
			result = definition.validator.list_definition_names()
		elif definition.data_type == DataType.Array:
			results = Index.list_dependent_definitions(definition.data_format)
		return results

	def list_fields(name):
		definition = Index.get(name)
		if definition.data_type == DataType.Object:
			return definition.validator.list_field_names()
		return [name]

	def clear():
		Index._idx = {}