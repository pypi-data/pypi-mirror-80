
class Stack():
	def __init__(self):
		self.stack_list = []

	def push(self, element):
		self.stack_list.append(element)

	def pop(self):
		try:
			return self.stack_list.pop(-1)
		except IndexError as e:
			raise EmptyStackException("Stack is empty, can't pop")
		
	def clear(self):
		del self.stack_list[:]

	def display(self):
		print(self.stack_list)

	def search(self, element):
		index_of_element = -1
		for i in range(self.get_stack_size()):
			if(self.stack_list[i] == element):
				index_of_element = i
		return index_of_element

	def is_empty(self):
		return not self.stack_list

	def clone(self):
		return self.stack_list.copy()

	def peek(self):
		try:	
			return self.stack_list[-1]
		except IndexError as e:
			raise EmptyStackException("May stack is empty")
		
		

	def get_stack_size(self):
		return len(self.stack_list)


class EmptyStackException(Exception):

	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		if self.message:
			message =  'Exception: {0} '.format(self.message)
		else:
			message =  'Check stack, May be empty'
		return message