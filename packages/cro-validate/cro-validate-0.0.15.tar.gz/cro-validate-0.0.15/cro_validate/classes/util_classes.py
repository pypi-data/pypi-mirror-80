
class DataDefinitionDefaultValue:
	pass


class ClassName:
	def class_fqn(obj):
		return '.'.join([obj.__class__.__module__, obj.__class__.__name__])

	def class_fqn_parts(fqn):
		i = fqn.rfind('.')
		m = fqn[:i]
		c = fqn[i+1:]
		return (m, c)
