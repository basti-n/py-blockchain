class ErrorHandler:

    @staticmethod
    def logError(error: Exception, *, msgPrefix: str = 'Error occured for: ', msgPostfix: str = '') -> None:
        """ Logs the initial input for the passed error to the console  """
        try:
            input = error.args[0].split(':')[-1]
            print(msgPrefix + input + msgPostfix)
        except:
            print(f'An Error occured logging {error.args}')

