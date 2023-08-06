import inspect;

class Integrity:
    positive_infinity = float('inf') 
    negative_infinity = float('-inf') 

    @staticmethod
    def check(condition, *msg):
        '''If condition is not true, then raises an exception, with default or optional message

        Args:
            condition (bool): The condition which must be true
            msg (any): Optional. See docstring for Integrity.deferredStringBuilder

        Raises:
            TypeError: if condition is not a bool (including if it is None)
            ValueError: if condition is false
        '''
        if(condition is None):
            raise TypeError(Integrity.__getTypeErrorDefaultString("bool", condition));

        if(not isinstance(condition, bool)):
            raise TypeError(Integrity.__getTypeErrorDefaultString("bool", condition));

        if(not condition):
            text = Integrity.__getMessage("Integrity check failed", msg)
            raise ValueError(text)

    @staticmethod
    def checkNotNone(test, *msg):
        '''If test is exactly None then raises an exception with default or optional message

        Args:
            test (bool): The condition which must be true
            msg (any): Optional. See docstring for Integrity.deferredStringBuilder

        Raises:
            ValueError: if and only if test is exctly None
        '''
        if(test is None):
            text = Integrity.__getMessage("None encountered", msg)
            raise ValueError(text)

    @staticmethod
    def checkIsBool(test, *msg):
        '''If test is not exactly of type bool then raises an exception with default or optional message

        Args:
            test (bool): The item which must be of type bool (note None would not be of type bool)
            msg (any): Optional. See docstring for Integrity.deferredStringBuilder

        Raises:
            TypeError: if test is not exactly of type bool
        '''
        if(not isinstance(test, bool)):
            text = Integrity.__getMessage(Integrity.__getTypeErrorDefaultString("bool", test), msg)
            raise TypeError(text)

    @staticmethod
    def checkIsBoolOrNone(test, *msg):
        '''If test is not exactly of type bool and not exactly None then raises an exception with default or optional message

        Args:
            test (bool): The item which must be of type bool or is set to None
            msg (any): Optional. See docstring for Integrity.deferredStringBuilder

        Raises:
            TypeError: if test is not exactly of type bool or set to None
        '''
        if(test is not None):
            Integrity.checkIsBool(test, *msg)

    @staticmethod
    def checkIsString(test, *msg):
        '''Check that first parameter is not None and is of type stringe

        Args:
            test (str): The item which must be of type string 
            msg (any): Optional. See docstring for Integrity.deferredStringBuilder

        Raises:
            TypeError: if test is not exactly of type string
        '''
        if(not isinstance(test, str)):
            text = Integrity.__getMessage(Integrity.__getTypeErrorDefaultString("string", test), msg)
            raise TypeError(text)

    @staticmethod
    def checkIsStringOrNone(test, *msg):
        '''Check that first parameter is either None or of type string

        Args:
            test (str): The item which must be of type string or set to None 
            msg (any): Optional. See docstring for Integrity.deferredStringBuilder

        Raises:
            TypeError: if test is not None and not exactly of type string
        '''
        if(test is not None):
            Integrity.checkIsString(test, *msg)

    @staticmethod
    def checkStringNotNoneOrEmpty(test, *msg):
        '''Check that first parameter is a string and is not None and not empty

        Args:
            test (str): The item which must be of type string and not None and not of length 0 (so a single space would pass) 
            msg (any): Optional. See docstring for Integrity.deferredStringBuilder

        Raises:
            TypeError: if test is not exactly of type string or set to None
            VaueError: if test is a string with length 0
        '''
        if(not isinstance(test, str)):
            text = Integrity.__getMessage(Integrity.__getTypeErrorDefaultString("string", test), msg)
            raise TypeError(text)
        if(test == ""):
            text = Integrity.__getMessage("Empty string", msg)
            raise ValueError(text)

    @staticmethod
    def checkIsValidNumber(test, *msg):
        '''Check that first parameter is a number (type float or int) and is not None, NaN or +-Infinity. Note bool is derived from int and will pass

        Args:
            test (int or float): The item which must be of type int or float and not None and not NaN and not infinity 
            msg (any): Optional. See docstring for Integrity.deferredStringBuilder

        Raises:
            TypeError: if test is not exactly of type string or set to None
            VaueError: if test is a string with length 0
        '''

        if(not isinstance(test, int) and not isinstance(test, float)):
            text = Integrity.__getMessage(Integrity.__getTypeErrorDefaultString("float or int", test), msg)
            raise TypeError(text)

        if(isinstance(test, bool)):
            text = Integrity.__getMessage(Integrity.__getTypeErrorDefaultString("float or int", test), msg)
            raise TypeError(text)

        if(test != test):
            text = Integrity.__getMessage("NaN", msg)
            raise ValueError(text)

        if(test == Integrity.positive_infinity):
            text = Integrity.__getMessage("Infinity", msg)
            raise ValueError(text)
        if(test == Integrity.negative_infinity):
            text = Integrity.__getMessage("-Infinity", msg)
            raise ValueError(text)

    @staticmethod
    def checkIsValidNumberOrNone(test, *msg):
        if(test is not None):
            Integrity.checkIsValidNumber(test, *msg)

    @staticmethod
    def checkIsFunction(test, *msg):
        if(not inspect.isroutine(test)):
            text = Integrity.__getMessage(Integrity.__getTypeErrorDefaultString("function", test), msg)
            raise TypeError(text)

    @staticmethod
    def checkIsFunctionOrNone(test, *msg):
        if(not test is None):
            Integrity.checkIsFunction(test, *msg)

    @staticmethod
    def __getTypeErrorDefaultString(expectedTypeString, item):
        prettyValue = str(item)
        if(item is None):
            return "Expected " + expectedTypeString + " but was None"

        if (hasattr(item, "__class__")):
            prettyType = item.__class__.__name__
        else:
            prettyType = type(item)

        return "Expected " + expectedTypeString + " but was " + prettyType + ", value was '" + prettyValue + "'"

    @staticmethod
    def deferredStringBuilder(*messageParts):
        '''Builds from an abritary mix of items, using {} substitution or adding after a comma

        Args:
            messageParts (any): variable arguments which get concatenated as strings (comma separated) or substituted into first {}

        Examples:
            "abc" -> "abc"
            "abc {} def", 1 -> "abc 1 def"
            1, "one", True -> "1, one, True"
            123, "and now {} ", 345 -> "123, and now 345"
            "{} {} {}", 1, 2, 3, 4 -> "1 2 3, 4"
        '''
        return Integrity.__getMessage('', messageParts)

    @staticmethod
    def __getMessage(default, msg):

        if(msg is None):
            return default

        if(len(msg) == 0):
            return default

        s = "";
        for item in msg:
            asString = str(item)

            pos = s.find("{}")
            if(pos != -1):
                s = s.replace("{}",  asString, 1)
            else:
                if(s == ""):
                    s += asString
                else:
                    if(isinstance(item, str)):
                        s += ", '" + item + "'"
                    else:
                        s += ", " + asString

        return s

