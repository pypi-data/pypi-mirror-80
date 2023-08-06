import logging
import bugsnag

class ErrorLogger:

    def __init__(self, api_key, release_stage):

        self.api_key = api_key
        self.release_stage = release_stage
            
        bugsnag.configure(
            api_key=self.api_key,
            release_stage=self.release_stage
        )
        
        self.logger = logging.getLogger('bugsnag')
        
        handler = bugsnag.handlers.BugsnagHandler()
        handler.setLevel(logging.ERROR)

        self.logger.addHandler(handler)

    def notify(self, e):
        bugsnag.notify(e)
        self.logger.error(e)
    
class ConfigError(Exception):

    def __init__(self, message):
        super().__init__(message)