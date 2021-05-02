class ErrorHandler:

    @staticmethod
    def logValueError(error: ValueError, *, msgPrefix: str = 'Error occured for: ', msgPostfix: str = '') -> None:
        """ Logs the initial input for the passed error to the console  """
        try:
            input = error.args[0].split(':')[-1]
            print(msgPrefix + input + msgPostfix)
        except:
            print(f'An Error occured logging {error.args}')
