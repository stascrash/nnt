class FilterExpression(object):
	def __init__(self, lambda_filter="lambda value: ", filter_operator="==", lambda_expression="lambda **results: "):
		"""Expression Filter constructor.
			:arg lambda_filter="lambda value: ",
			:arg lambda_expression="lambda **results: ",
			:arg filter_operator="==", supported values ==, <=, >=
		You may also provide your own filter and expression declarations.

		"""
		self.conditions = dict()
		self.eval_result = dict()
		self.process_filter = str()
		self.lambda_filter_declaration = lambda_filter
		self.lambda_filter_operator = filter_operator
		self.lambda_expression_declaration = lambda_expression

	def set_filter_conditions(self, **kwargs):
		"""Populates the conditions dictionary with generated boolean-lambdas.

		Each lambda function returns a True/False.
		a sample lambda string may have the following format:
		"lambda value: value == "{string query}"
		The input kwarg argument must have the following syntax:
		named-argument: a Key value that represents the condition of argument,
		value-argument: is a string expression that supports the following syntax:
		"$bob" - the search value must be prefixed with '$' symbol.
		"or / and / not" - are valid boolean keywords.
		The "$" Symbol is stripped during lambda-generation.

		A simple input **kwarg may have the following look: name="$bob"
			-> generated: "lambda value: value == "bob"

		A complex input **kwarg may have the following look: name="$chad or $paul and not $zack"
			-> generated: "lambda value: value == "chad" or value == "paul" and not value == "zack"

		The eval method, returns a callable object(function), that is constructed by generated filter string.
		The generated callable object is invoked during evaluation stage, in 'eval' function.
		"""
		for key, val in kwargs.items():
			if not str(val).startswith("$"):
				val = "${}".format(val)
			self.conditions[key] = compile(self._generate_filter(val), '<string>', 'eval')

	def _generate_filter(self, expression):
		"""Parse user expression and generate lambda expression string"""
		parts = expression.split(" ")
		assembly = [self.lambda_filter_declaration]
		for part in parts:
			if part.startswith("$"):
				expected_value = part.split("$")[-1]
				if expected_value.isdigit():
					assembly.append("value {operator} {expected}".format(operator=self.lambda_filter_operator,
					                                                     expected=expected_value))
				else:
					assembly.append(
						"value {operator} \"{expected}\"".format(operator=self.lambda_filter_operator,
						                                         expected=expected_value))
			else:
				assembly.append(part)
		return " ".join(assembly)

	def validate_keys(self, data):
		"""Validates the keys in input object. It raises a KeyError exception
		if required condition-key specified in expression's **kwargs exists
		within the searchable data-set(dict-like object).
		Supplied search key must exist for the object for which expression is being
		generated. Externally, user may handle cases of exception raising.
		"""
		for k in self.conditions.keys():
			if k not in data:
				raise KeyError("No \"{}\" key in data".format(k))

	def set_filter_expression(self, expression):
		"""Add basic logic to evaluate expressions"""
		self.process_filter = compile("{}".format(self._generate_expression(expression)), '<string>', 'eval')

	def _generate_expression(self, raw_eval_str):
		"""Parse user basic logic and generate valid lambda expression string"""
		parts = raw_eval_str.split(" ")
		assembly = [self.lambda_expression_declaration]
		for part in parts:
			if part.startswith("$"):
				complete_part = "results[\"{}\"]".format(part.split("$")[-1])
				assembly.append(complete_part)
			else:
				assembly.append(part)
		return " ".join(assembly)

	def get_filter_expression(self):
		"""Returns the filter expression as a string, this allows user to append to existing expression
		without declaring a new filter again.."""
		return self.process_filter.split(self.lambda_expression_declaration)[-1]

	def eval(self, data):
		self.validate_keys(data)
		results = dict()
		for key, func in self.conditions.items():
			results[key] = eval(func)(data.get(key))
		return eval(self.process_filter)(**results)


class Filter(object):
	# Class variable of live Expression instance
	expression = FilterExpression()

	@staticmethod
	def skip_month(data, operator="==", **kwargs):
		"""Returns true/false if given month of a year should be skipped for
		individual record.

		:arg data: Record object(or dict-like object,
		:arg y: int Year
		:arg m: int Month
		:arg operator: str (supported ==, <=, >=
		operator argument defines the logic of how lambda is evaluated
		"""
		y = kwargs.get('y')
		m = kwargs.get('m')

		Filter.expression.lambda_filter_operator = operator
		Filter.expression.set_filter_conditions(r_year="${}".format(y),
		                                        r_month="${}".format(m))
		Filter.expression.set_filter_expression("$r_year and $r_month")

		return Filter.expression.eval(data)

	@staticmethod
	def company_and_date(data, company, date, operator="=="):
		Filter.expression.lambda_filter_operator = operator
		Filter.expression.set_filter_conditions(company=company,
		                                 start_year=date.year,
		                                 start_month=date.month,
		                                 start_day=date.day)
		Filter.expression.set_filter_expression("$company and $start_year and $start_month and $start_day")
		return Filter.expression.eval(data)
