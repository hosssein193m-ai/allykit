from allykit.data_kit.Language import (DECIMAL_DIGITS, ASCII_UPPERCASE,
                ASCII_LOWERCASE, PUNCTUATION_ASCII)


class Review_Password:
    """
    A class for reviewing and evaluating password strength based on various security criteria.
    
    This class analyzes a password against multiple character set requirements, length constraints,
    space restrictions, and character repetition limits. It provides multiple output formats
    for the evaluation results and calculates an entropy-based score.
    """
    
    def __init__(self, password: str, add: int = 3):
        """
        Initialize the password reviewer with a password and repetition threshold.
        
        Args:
            password (str): The password string to be reviewed
            add (int, optional): Maximum allowed character repetition count. Defaults to 3.
        """
        self.password = password
        self.add = add  
        self.data = None
        self._refresh_data()

    def _refresh_data(self):
        """
        Refresh the internal evaluation data for the current password.
        
        This method updates the data list with the latest evaluation results for all
        password criteria checks. It is called automatically during initialization
        and should be called after any password changes.
        """
        self.data = [
            self.contains_any_char(PUNCTUATION_ASCII),
            self.contains_any_char(ASCII_LOWERCASE),
            self.contains_any_char(ASCII_UPPERCASE),
            self.contains_any_char(DECIMAL_DIGITS),
            self.len_password(),
            self.check_no_space(),
            self.Repeating_Characters() 
        ]

    def contains_any_char(self, charset: str) -> bool:
        """
        Check if the password contains at least one character from the given character set.
        
        Args:
            charset (str): A string containing the character set to check against
            
        Returns:
            bool: True if at least one character from charset is found in password, False otherwise
        """
        for char in self.password:
            if char in charset:
                return True
        return False

    def len_password(self) -> bool:
        """
        Check if the password meets the minimum length requirement.
        
        Returns:
            bool: True if password length is 8 or more characters, False otherwise
        """
        if len(self.password) < 8:
            return False
        return True

    def check_no_space(self) -> bool:
        """
        Check if the password contains any space characters.
        
        Returns:
            bool: True if no spaces are present in the password, False if spaces exist
        """
        if " " in self.password:
            return False
        return True

    def Repeating_Characters(self) -> bool:
        """
        Check if any character in the password exceeds the maximum repetition threshold.
        
        Returns:
            bool: True if no character appears more than 'add' times, False otherwise
        """
        for char in self.password:
            if self.password.count(char) > self.add:
                return False
        return True

    def password_check(self, types: str = "bool") -> bool | dict | list | str:
        """
        Retrieve password evaluation results in various output formats.
        
        Args:
            types (str, optional): Desired output format - "bool", "dict", "list", or "str".
                                  Defaults to "bool".
        
        Returns:
            bool | dict | list | str: Evaluation results in the specified format:
                - "bool": Overall password status (True if all criteria pass)
                - "dict": Dictionary with individual criteria results
                - "list": List starting with overall status followed by individual results
                - "str": Formatted string with all evaluation results
        
        Raises:
            TypeError: If an unsupported output type is specified
        """
        data = self.data
        status = all(data)
        if types == "bool":
            return status
        if types == "dict":
            return {"status": status,
                    "DECIMAL_DIGITS": data[3],
                    "upper": data[2],
                    "lower": data[1],
                    "PUNCTUATION_ASCII": data[0],
                    "len_password": data[4],
                    "no_space": data[5],
                    "Repeating_Characters": data[6]}
        if types == "list":
            return [status] + data 
        if types == "str":
            return f"status:{status}, DECIMAL_DIGITS:{data[3]}, upper : {data[2]}, lower:{data[1]}, PUNCTUATION_ASCII:{data[0]}, len_password:{data[4]}, no_space:{data[5]}, Repeating_Characters:{data[6]}"
        raise TypeError(f"not input type:{types},type -> (str or list or dict or bool)")
    
    def Entropy_Score_Password(self) -> int:
        """
        Calculate an entropy-based security score for the password.
        
        The score is calculated based on the following criteria:
        - Punctuation presence: +3 points
        - Lowercase letters: +1 point
        - Uppercase letters: +1 point
        - Digits: +1 point
        - Minimum length (8+ chars): +2 points
        - No character repetition exceeding threshold: +2 points
        
        Returns:
            int: A numerical score representing password strength (higher = stronger).
                 Returns 0 if the password contains spaces.
        """
        data = self.data
        Score = 0
        if not data[5]:
            return Score
        if data[0]:
            Score += 3
        if data[1]:
            Score += 1
        if data[2]:
            Score += 1
        if data[3]:
            Score += 1
        if data[4]:
            Score += 2
        if data[6]:
            Score += 2
        return Score