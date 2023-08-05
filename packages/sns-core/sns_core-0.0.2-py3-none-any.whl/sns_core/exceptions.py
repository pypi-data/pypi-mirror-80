class SNSparserException(Exception):
    """Exception raised when parsing an SNS interaction.

    Attributes:
        interaction -- the interaction that raised the error
        message -- explanation of the error
    """

    def __init__(self, interaction, message="Exception occurred while parsing the following interaction"):
        self.interaction = interaction
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.interaction}: {self.message}'

class SNSinteractionException(Exception):
    """Exception raised when requesting an SNS interaction.
    
    Attributes:
        interaction -- the interaction that raised the error
        message -- explanation of the error
    """

    def __init__(self, interaction, message="Exception occurred while requesting with the following interaction"):
        self.interaction = interaction
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.interaction}: {self.message}'

class SNSrecordIntegrityException(Exception):
    """Exception raised when the integrity of a record is instable.
    
    Attributes:
        record -- the record that raised the error
        message -- explanation of the error
    """

    def __init__(self, record, message="Exception occurred while checked the integrity of the following record"):
        self.record = record
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.record}: {self.message}'