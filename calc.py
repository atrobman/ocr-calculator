import math

class Func:

	def __init__(self, n):
		self.name = n
		self.args = 1

	def __str__(self):
		return self.name
	
	def __repr__(self):
		return self.name

class Calc:
	
	def __init__(self, s):
		
		# ) <close parentheses> is handled separately
		self.prec = {
			0: 0, # ( Open Parentheses
			1: 2, # + Plus
			2: 2, # - Minus
			3: 3, # * Multiply
			4: 3, # / Divide
			5: 3, # % Modulus
			6: 5, # ^ Exponentaite
			7: 6, # ! Factorial
			8: 4, # - Unary negation
			9: 0, # ( Function parentheses
			10: 1 # , Argument separation
		}
		
		self.binaries  = " +-*/%^   ,"
		self.prefixes  = "(       -( "
		self.postfixes = "       !   "

		self.sym = []
		self.num = []
		self.func = []
		self.decimals = -1
		self.numBuff = -1
		self.stackFlag = False
		self.strBuff = None
		self.expression = "(" + s + ")"

	def __is_op(self, c):
		return c in self.binaries or c in self.prefixes or c in self.postfixes

	def string_eval(self):

		for i, char in enumerate(self.expression):
			self.__read_char(char, i)

		if not len(self.sym) == 0:
			raise ArithmeticError("Could not parse expression")

		return self.num.pop()
	
	def __read_char(self, c, x):

		if c == ' ':
			pass

		elif c == '.':
			if self.numBuff == -1:
				self.numBuff = 0

			self.decimals = 0
		
		elif c.isalpha():
			
			if self.strBuff is None:
				self.strBuff = c
			else:
				self.strBuff += c
		
		elif c.isdigit():
			self.__put_numBuff(c)
		
		else:

			if self.numBuff >= 0:
				if self.decimals >= 0:
					self.numBuff /= 10 ** self.decimals
				
				self.num.append(self.numBuff)
				self.decimals = -1
				self.numBuff = -1
				self.stackFlag = True
			
			if c == '(':
				if self.strBuff is not None:
					self.func.append(Func(self.strBuff))
					self.strBuff = None
					self.sym.append(9)
				
				else:
					if self.stackFlag:
						self.__put_symbol("*")
					self.sym.append(0)
			
			elif self.__is_op(c) or c == ')':

				if self.strBuff is not None:
					self.__apply_const(self.strBuff)
				
				if c == ')' and x is not len(self.expression) - 1:
					count_open = 0

					for i in self.sym:
						if i == 0 or i == 9:
							count_open += 1
					
					if count_open == 1:
						raise ArithmeticError()

				self.__put_symbol(c)
		
		# print(f"{c} {self.sym} {self.num} {self.func}")
	
	def __eval(self, index):

		while index == -1 or (len(self.sym) != 0 and self.prec[self.sym[-1]] >= self.prec[index]):
			
			stop_eval = False
			op1, op2 = None, None

			top = self.sym.pop()

			if   top == 0:
				stop_eval = True

			elif top == 1:
				op2 = self.num.pop()
				op1 = self.num.pop()
				self.num.append(op1 + op2)

			elif top == 2:
				op2 = self.num.pop()
				op1 = self.num.pop()
				self.num.append(op1 - op2)

			elif top == 3:
				op2 = self.num.pop()
				op1 = self.num.pop()
				self.num.append(op1 * op2)

			elif top == 4:
				op2 = self.num.pop()
				op1 = self.num.pop()

				if op2 == 0:
					raise ZeroDivisionError()

				self.num.append(op1 / op2)

			elif top == 5:
				op2 = self.num.pop()
				op1 = self.num.pop()

				if op2 == 0:
					raise ZeroDivisionError()

				self.num.append(op1 % op2)

			elif top == 6:
				op2 = self.num.pop()
				op1 = self.num.pop()
				self.num.append(op1 ** op2)

			elif top == 7:
				op1 = self.num.pop()
				self.num.append(self.__fact(op1))
			
			elif top == 8:
				op1 = self.num.pop()
				self.num.append(-1 * op1)

			elif top == 9:
				self.__apply_func(self.func.pop())
				stop_eval = True
			
			elif top == 10:
				pass

			else:
				raise ArithmeticError(f"Invalid sym index ({top})")

			if stop_eval:
				break
	
	def __apply_const(self, const):

		if const == "pi": # Pi
			self.num.append(math.pi)
		
		elif const == "e": # E
			self.num.append(math.e)

		elif const == "tau": # Tau
			self.num.append(math.tau)

		elif const == "phi": # Golden Ratio
			self.num.append( (1 + math.sqrt(5)) / 2 )

		elif const == "c": # Speed of Light (in m/s)
			self.num.append(299792458)

		elif const == "G": # Gravitational Constant
			self.num.append(6.674E-11)

		else:
			raise ArithmeticError(f"Invalid constant ({const})")
		
		self.strBuff = None
		self.stackFlag = True

	def __put_symbol(self, c):

		symIndex = -1

		if self.stackFlag:
			if c in self.binaries:
				symIndex = self.binaries.index(c)
				self.stackFlag = False
			elif c in self.postfixes:
				symIndex = self.postfixes.index(c)
				stackFlag = True
		
		elif c in self.prefixes:
			symIndex = self.prefixes.index(c)
			self.stackFlag = False

		self.__eval(symIndex)

		if c != ')':
			self.sym.append(symIndex)
		
		if c == ',':
			f = self.func.pop()
			f.args += 1
			self.func.append(f)
	
	def __put_numBuff(self, c):

		if self.numBuff == -1:
			if self.stackFlag:
				self.__put_symbol('*')
			self.numBuff = 0
		
		if self.decimals >= 0:
			self.decimals += 1
		
		self.numBuff *= 10
		self.numBuff += int(c)
	
	def __apply_func(self, f):

		if f.name == "double":
			"""Multiply the input number by 2"""
			self.num.append(self.num.pop() * 2)
		
		elif f.name == "sin":
			"""Sine function (radians)"""
			self.num.append(math.sin(self.num.pop()))

		elif f.name == "sind":
			"""Sine function (degrees)"""
			self.num.append(math.sin(math.radians(self.num.pop())))

		elif f.name == "cos":
			"""Cosine function (radians)"""
			self.num.append(math.cos(self.num.pop()))

		elif f.name == "cosd":
			"""Cosine function (degrees)"""
			self.num.append(math.cos(math.radians(self.num.pop())))

		elif f.name == "tan":
			"""Tangent function (radians)"""
			self.num.append(math.tan(self.num.pop()))
		
		elif f.name == "tand":
			"""Tangent function (degrees)"""
			self.num.append(math.tan(math.radians(self.num.pop())))
		
		elif f.name == "dtr":
			"""Degrees to radians"""
			self.num.append(math.radians(self.num.pop()))
		
		elif f.name == "rtd":
			"""Radians to degrees"""
			self.num.append(math.degrees(self.num.pop()))

		elif f.name == "csc":
			"""Cosecant function (radians)"""
			self.num.append(1 / math.sin(self.num.pop()))

		elif f.name == "cscd":
			"""Cosecant function (degrees)"""
			self.num.append(1 / math.sin(math.radians(self.num.pop())))
		
		elif f.name == "sec":
			"""Secant function (radians)"""
			self.num.append(1 / math.cos(self.num.pop()))

		elif f.name == "secd":
			"""Secant function (degrees)"""
			self.num.append(1 / math.cos(math.radians(self.num.pop())))

		elif f.name == "cot":
			"""Cotangent function (radians)"""
			self.num.append(1 / math.tan(self.num.pop()))

		elif f.name == "cotd":
			"""Cotangent function (degrees)"""
			self.num.append(1 / math.tan(math.radians(self.num.pop())))

		elif f.name == "max":
			"""Returns the max of n numbers where n >= 2"""
			m = self.num.pop()

			for i in range(1, f.args):
				m = max(m, self.num.pop())
			
			self.num.append(m)
		
		elif f.name == "min":
			"""Returns the min of n numbers where n >= 2"""
			m = self.num.pop()

			for i in range(1, f.args):
				m = min(m, self.num.pop())

			self.num.append(m)

		elif f.name == "atan":
			"""Arc tangent function (radians)"""
			self.num.append(math.atan(self.num.pop()))
		
		elif f.name == "atand":
			"""Arc tangent function (degrees)"""
			self.num.append(math.degrees(math.atan(self.num.pop())))
		
		elif f.name == "asin":
			"""Arc sine function (radians)"""
			self.num.append(math.asin(self.num.pop()))

		elif f.name == "asind":
			"""Arc sine function (degrees)"""
			self.num.append(math.degrees(math.asin(self.num.pop())))

		elif f.name == "acos":
			"""Arc cosine function (radians)"""
			self.num.append(math.acos(self.num.pop()))

		elif f.name == "acosd":
			"""Arc cosine function (degrees)"""
			self.num.append(math.degrees(math.acos(self.num.pop())))

		elif f.name == "zeta":
			"""Approximation of the Riemann Zeta function (not analytically continued)"""
			num1 = self.num.pop()
			num2 = 0

			for i in range(1, 100000):
				num2 += 1 / (i ** num1)

			self.num.append(num2)

		elif f.name == "abs":
			"""Absolute value function"""
			self.num.append(math.abs(self.num.pop()))
		
	def __fact(self, n):

		if n == 1:
			return 1
		
		elif n < 1:
			raise ArithmeticError()

		return self.__fact(n-1) * n