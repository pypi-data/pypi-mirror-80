#Uni testing
from Stack import Stack

def test_stack_push_integer():
	stack = Stack()
	input_value = 5
	stack.push(input_value)
	assert stack.peek() == input_value

def test_stack_push_string():
	stack = Stack()
	input_value = "Element"
	stack.push(input_value)
	assert stack.peek() == input_value

def test_stack_push_float():
	stack = Stack()
	input_value = 3.2
	stack.push(input_value)
	assert stack.peek() == input_value

def test_stack_push_boolean():
	stack = Stack()
	input_value = True
	stack.push(input_value)
	assert stack.peek() == input_value
