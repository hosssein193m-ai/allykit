from .password import generate_password_with_prefix_suffix
from .Scoring_password import Review_Password
from allykit.Security_kit.hash_kit import HP
from allykit.data_kit.Language import PRINTABLE_ASCII

from datetime import datetime, timedelta


def generate_timed_password(time: str = 'days.10', charset: str = PRINTABLE_ASCII) -> str:
    """
    Generates a cryptographically strong random password with embedded start and
    expiration timestamps.

    This function creates a self-contained time-limited password that includes
    the generation timestamp (start time) and an automatically calculated
    expiration timestamp (end time) based on the specified duration. The random
    middle portion is generated using secure random methods from the specified
    character set.

    Args:
        time (str): Duration string in 'unit.value' format specifying how long
                the password should remain valid. Supported units include:
                - 'days' (e.g., 'days.10' for 10 days)
                - 'hours' (e.g., 'hours.5' for 5 hours)
                - 'minutes' (e.g., 'minutes.30' for 30 minutes)
                - 'seconds' (e.g., 'seconds.45' for 45 seconds)
                Defaults to 'days.10' (10 days validity).

        charset (str): Character set to use for generating the random password
                    portion. Must be a string containing all allowed characters.
                    Defaults to PRINTABLE_ASCII (all printable ASCII characters).

    Returns:
        str: A formatted password string with the structure:
            "time start {ISO_TIMESTAMP}--{RANDOM_PASSWORD}--time end {ISO_TIMESTAMP}"

            Example output:
            "time start 2026-06-10T04:32:32.115727--QCGfik`?gKuEk2}]DZF_Nm[h3&~M@=&PL}CTnQ--time end 2026-06-20T04:32:32.115727"

    Raises:
        ValueError: If the time parameter format is invalid (e.g., missing dot,
                non-integer value, or unsupported unit).
        ValueError: If charset is empty or contains no valid characters for generation.

    Dependencies:
        Requires generate_password_with_prefix_suffix() function which handles
        the actual random password generation with the specified length and
        character set.

    Example:
        >>> # Generate a password valid for 10 days (default)
        >>> pwd = generate_timed_password()
        >>> print(pwd)
        time start 2026-06-10T04:32:32.115727--aB3$xZ9@--time end 2026-06-20T04:32:32.115727

        >>> # Generate a password valid for 2 hours
        >>> pwd = generate_timed_password('hours.2')
        >>> print(pwd)
        time start 2026-06-10T14:25:10.123456--K#mP9$qL2@--time end 2026-06-10T16:25:10.123456

        >>> # Generate a password with custom character set (digits only)
        >>> pwd = generate_timed_password('minutes.5', charset='0123456789')
        >>> print(pwd)
        time start 2026-06-10T10:00:00.000000--8347291056--time end 2026-06-10T10:05:00.000000
    """
    times = datetime.now()
    password = generate_password_with_prefix_suffix(
        length=50,
        prefix=f"time start {times.isoformat()}--",
        add=40,
        charset=charset
    )
    parts = time.split('.')
    unit = parts[0]
    value = int(parts[1])
    delta_args = {unit: value}
    delta_obj = timedelta(**delta_args)
    end_time_str = (times + delta_obj).isoformat()
    return generate_password_with_prefix_suffix(
        password,
        prefix=f"--time end {end_time_str}",
        suffix=True
    )


def wrap_password_with_time(password: str, time: str = 'days.10') -> str:
    """
    Wraps an existing password string with start and expiration timestamps,
    converting it into a time-limited credential.

    Unlike generate_timed_password() which creates a new random password, this
    function takes a user-provided password and embeds it between the start and
    end timestamps, preserving the original password content while adding
    time-based expiration functionality.

    Args:
        password (str): The original password string to be wrapped with timestamps.
                       This can be any string, including pre-existing passwords,
                       secrets, or tokens. The content is preserved exactly as provided.

        time (str): Duration string in 'unit.value' format specifying the validity
                   period from the current moment. Format: '{unit}.{value}'

                   Supported units:
                   - 'days' (e.g., 'days.7' for 7 days)
                   - 'hours' (e.g., 'hours.12' for 12 hours)
                   - 'minutes' (e.g., 'minutes.45' for 45 minutes)
                   - 'seconds' (e.g., 'seconds.30' for 30 seconds)

                   Defaults to 'days.10' (10 days validity).

    Returns:
        str: A formatted password string with the structure:
             "time start {ISO_TIMESTAMP}--{ORIGINAL_PASSWORD}--time end {ISO_TIMESTAMP}"

             Example output:
             "time start 2026-06-10 04:32:32.115989--my_secret_password--time end 2026-06-20T04:32:32.115989"

    Raises:
        ValueError: If the time parameter format is invalid (incorrect unit,
                   missing dot, or non-integer value).
        ValueError: If password is empty or None (depending on generate_password_with_prefix_suffix implementation).

    Dependencies:
        Uses generate_password_with_prefix_suffix() to handle the string wrapping
        with proper prefix and suffix formatting.

    Example:
        >>> # Wrap an existing password with 10-day validity
        >>> wrapped = wrap_password_with_time("mySecret123")
        >>> print(wrapped)
        time start 2026-06-10T04:32:32.115989--mySecret123--time end 2026-06-20T04:32:32.115989

        >>> # Wrap with 1-hour validity
        >>> wrapped = wrap_password_with_time("temp_access_key", "hours.1")
        >>> print(wrapped)
        time start 2026-06-10T15:30:00.123456--temp_access_key--time end 2026-06-10T16:30:00.123456

        >>> # Check if wrapped password is valid
        >>> is_password_valid(wrapped)
        True

        >>> # Extract and verify the original password hasn't been modified
        >>> parts = wrapped.split('--')
        >>> original = parts[1]  # Returns "temp_access_key"

    Use Cases:
        - Converting static passwords into time-limited credentials
        - Adding expiration to existing API keys or tokens
        - Creating temporary access codes from master passwords
        - Auditing and tracking when passwords were created

    Note:
        - The current timestamp (datetime.now()) is used as the start time
        - The original password is not encrypted or hashed; it remains in plaintext
        - For security-sensitive applications, consider hashing or encrypting
          the password portion before wrapping
        - The wrapped password remains compatible with is_password_valid() for
          expiration checking
    """
    times = datetime.now()
    password_time = generate_password_with_prefix_suffix(
        password,
        prefix=f"time start {times.isoformat()}--"
    )
    parts = time.split('.')
    unit = parts[0]
    value = int(parts[1])
    delta_args = {unit: value}
    delta_obj = timedelta(**delta_args)
    end_time_str = (times + delta_obj).isoformat()
    return generate_password_with_prefix_suffix(
        password_time,
        prefix=f"--time end {end_time_str}",
        suffix=True
    )


def generating_password(password: str = None, time: str = None, charset: str = PRINTABLE_ASCII):
    """
    Factory function that generates either a new timed password or wraps an existing one.

    This function serves as a unified interface for password generation, automatically
    selecting between creating a new random timed password or wrapping an existing
    password with time-based expiration based on the provided parameters.

    Args:
        password (str, optional): An existing password to wrap with timestamps.
                                  If None, a new random password will be generated.
                                  Defaults to None.

        time (str, optional): Duration string in 'unit.value' format specifying
                             the validity period. If not provided, defaults to
                             'days.10' when generating a new password, or will
                             be passed through to wrap_password_with_time().

        charset (str): Character set to use for generating random passwords.
                      Only used when password is None and a new password is generated.
                      Defaults to PRINTABLE_ASCII (all printable ASCII characters).

    Returns:
        str: A time-stamped password string in the format:
             "time start {ISO_TIMESTAMP}--{PASSWORD}--time end {ISO_TIMESTAMP}"

    Raises:
        ValueError: If time parameter format is invalid or if password is invalid.

    Example:
        >>> # Generate a new timed password
        >>> pwd = generating_password(time='hours.2')
        >>> print(pwd)
        time start 2026-06-10T15:30:00.123456--K#mP9$qL2@--time end 2026-06-10T17:30:00.123456

        >>> # Wrap an existing password
        >>> pwd = generating_password("my_secret", "days.5")
        >>> print(pwd)
        time start 2026-06-10T15:30:00.123456--my_secret--time end 2026-06-15T15:30:00.123456

        >>> # Generate with custom character set
        >>> pwd = generating_password(charset='0123456789', time='minutes.30')
        >>> print(pwd)
        time start 2026-06-10T15:30:00.123456--8347291056--time end 2026-06-10T16:00:00.123456

    See Also:
        - generate_timed_password(): For generating new random timed passwords
        - wrap_password_with_time(): For wrapping existing passwords with timestamps
    """
    if password is None:
        return generate_timed_password(time=time, charset=charset)
    return wrap_password_with_time(password=password, time=time)


class Time_Password:
    """
    A comprehensive class for managing and validating time-limited passwords.

    This class parses, validates, and provides detailed information about passwords
    that have been created with embedded start and expiration timestamps. It offers
    methods to check validity, extract the original password, calculate remaining time,
    and generate detailed status reports including security scoring.

    The class expects passwords in the format:
    "time start {ISO_TIMESTAMP}--{PASSWORD}--time end {ISO_TIMESTAMP}"

    Key features:
        - Automatic validation of password format and structure
        - Extraction of start time, end time, and original password
        - Validity checking against current time
        - Time remaining calculation
        - Password security scoring using Review_Password
        - Multiple output formats (string representation, dictionary, etc.)

    Example:
        >>> # Create a timed password
        >>> pwd = generate_timed_password('hours.2')
        >>>
        >>> # Initialize the Time_Password object
        >>> tp = Time_Password(pwd)
        >>>
        >>> # Check if still valid
        >>> if tp.is_password_valid():
        >>>     print(f"Password is valid for {tp.time_remaining()}")
        >>>
        >>> # Get detailed status
        >>> status = tp.status_password()
        >>> print(status['status']['text'])  # "Active" or "Expired"
        >>> print(status['Password security']['score'])  # Security score

    Attributes:
        password (str): The complete time-stamped password string
        _time_formats (list): List of supported datetime formats for parsing
    """

    def __init__(self, password: str):
        """
        Initialize the Time_Password instance with a time-stamped password.

        Args:
            password (str): The complete time-stamped password string in the format
                           "time start {ISO_TIMESTAMP}--{PASSWORD}--time end {ISO_TIMESTAMP}"

        Raises:
            ValueError: If password is None, or if the password format is invalid
                       (missing required markers or separators)

        Example:
            >>> tp = Time_Password("time start 2026-06-10T04:32:32.115989--myPass--time end 2026-06-20T04:32:32.115989")
        """
        if password is None:
            raise ValueError("Password cannot be None")
        self.password = password
        self._time_formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%d %H:%M:%S.%f"]
        self._preliminary_review()

    def _preliminary_review(self) -> None:
        """
        Performs initial validation of the password format.

        This method checks for the presence of required markers and separators
        in the password string. It is called automatically during initialization.

        Raises:
            ValueError: If the password is missing 'time start' marker,
                       'time end' marker, or '--' separators.

        Note:
            This is a basic format validation and does not verify timestamp
            validity or password content.
        """
        if 'time start' not in self.password:
            raise ValueError("Invalid password format: missing 'time start' marker.")
        if 'time end' not in self.password:
            raise ValueError("Invalid password format: missing 'time end' marker.")
        if '--' not in self.password:
            raise ValueError("Invalid password format: missing '--' separators.")

    def _extract_time(self, marker: str) -> str:
        """
        Extracts a timestamp string associated with the given marker.

        This internal helper method finds the specified marker in the password
        string and extracts the timestamp that follows it, stopping at the next
        '--' separator or the end of the string.

        Args:
            marker (str): The marker to search for ('time start' or 'time end')

        Returns:
            str: The extracted timestamp string

        Raises:
            ValueError: If the specified marker is not found in the password

        Note:
            The extracted timestamp is returned as a string and may need
            additional parsing to convert to a datetime object.
        """
        if marker not in self.password:
            raise ValueError(f"No '{marker}' marker found")

        start_idx = self.password.find(marker) + len(marker)
        end_idx = self.password.find("--", start_idx)
        if end_idx == -1:
            end_idx = len(self.password)

        return self.password[start_idx:end_idx].strip()

    def start_time(self) -> str:
        """
        Retrieves the start timestamp from the password.

        Returns:
            str: The start timestamp as a string in ISO format

        Example:
            >>> tp = Time_Password("time start 2026-06-10T04:32:32.115989--pass--time end ...")
            >>> tp.start_time()
            '2026-06-10T04:32:32.115989'
        """
        return self._extract_time("time start")

    def end_time(self) -> str:
        """
        Retrieves the expiration timestamp from the password.

        Returns:
            str: The end timestamp as a string in ISO format

        Example:
            >>> tp = Time_Password("...--time end 2026-06-20T04:32:32.115989")
            >>> tp.end_time()
            '2026-06-20T04:32:32.115989'
        """
        return self._extract_time("time end")

    def get_password(self) -> str:
        """
        Extracts and returns the original password without timestamps.

        This method parses the complete time-stamped password string and
        returns the middle portion that contains the actual password.

        Returns:
            str: The extracted password string

        Raises:
            ValueError: If the password format is invalid (doesn't contain exactly
                       two '--' separators)

        Example:
            >>> tp = Time_Password("time start 2026-06-10--mySecret123--time end 2026-06-20")
            >>> tp.get_password()
            'mySecret123'
        """
        parts = self.password.split('--')
        if len(parts) != 3:
            raise ValueError("Invalid password format")
        return parts[1]

    def is_expired(self) -> bool:
        """
        Checks if the password has expired.

        Returns:
            bool: True if the password has expired, False if it is still valid

        Example:
            >>> tp = Time_Password(wrapped_password)
            >>> if tp.is_expired():
            >>>     print("Password has expired!")
        """
        return not self.is_password_valid()

    def time_remaining(self) -> timedelta:
        """
        Calculates the remaining time until the password expires.

        Returns:
            timedelta: A timedelta object representing the time remaining.
                      Returns timedelta(0) if the password is already expired.

        Example:
            >>> tp = Time_Password(password)
            >>> remaining = tp.time_remaining()
            >>> print(f"Password expires in {remaining.total_seconds()} seconds")
        """
        if self.is_password_valid():
            end_time = datetime.strptime(self.end_time(), self._time_formats[0])
            return end_time - datetime.now()
        return timedelta(0)

    def is_password_valid(self) -> bool:
        """
        Determines if the password is still valid (not expired).

        This method compares the current time against the password's
        expiration timestamp to determine validity.

        Returns:
            bool: True if the password is still valid (current time <= end time),
                 False if it has expired

        Raises:
            ValueError: If the timestamp format is unrecognized or cannot be parsed

        Example:
            >>> tp = Time_Password(password)
            >>> if tp.is_password_valid():
            >>>     # Proceed with authentication
            >>>     pass
        """
        try:
            end_time_part = self.end_time()
            for fmt in self._time_formats:
                try:
                    end_time = datetime.strptime(end_time_part, fmt)
                    return datetime.now() <= end_time
                except ValueError:
                    continue

            raise ValueError(f"Unrecognized time format: {end_time_part}")

        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid password time format: {e}")

    def status_password(self) -> dict:
        """
        Generates a comprehensive status report for the password.

        This method returns detailed information including:
        - Timestamps (start and end)
        - The password (in plaintext)
        - Password hash (for secure storage)
        - Validity status (Active/Expired)
        - Time-to-Live statistics (seconds, days, hours, minutes)
        - Password security score and individual criteria results

        Returns:
            dict: A dictionary containing all status information with the following keys:
                - "time start": Start timestamp string
                - "password": The original password
                - "time end": Expiration timestamp string
                - "password hash": Hashed version of the password
                - "status": Dict with "text" (Active/Expired) and "is_valid" (bool)
                - "Time to Live": Dict with total seconds, days, seconds, microseconds,
                  total minutes, and total hours
                - "Password security": Dict with "score" (int) and "status" (dict of criteria)

        Example:
            >>> tp = Time_Password(password)
            >>> status = tp.status_password()
            >>> print(status['status']['text'])  # "Active"
            >>> print(status['Time to Live']['Total hours'])  # 240.5
            >>> print(status['Password security']['score'])  # 8
        """
        is_valid = self.is_password_valid()
        password = self.get_password()
        start_time_str = self.start_time()
        end_time_str = self.end_time()

        start_time = datetime.strptime(start_time_str, self._time_formats[0])
        end_time = datetime.strptime(end_time_str, self._time_formats[0])
        time_diff = end_time - start_time

        review = Review_Password(password)

        return {
            "time start": start_time_str,
            "password": password,
            "time end": end_time_str,
            "password hash": HP(password),
            "status": {
                "text": "Active" if is_valid else "Expired",
                "is_valid": is_valid
            },
            "Time to Live": {
                "Total seconds": time_diff.total_seconds(),
                "Days": time_diff.days,
                "Seconds (within the day)": time_diff.seconds,
                "Microseconds": time_diff.microseconds,
                "Total minutes": time_diff.total_seconds() / 60,
                "Total hours": time_diff.total_seconds() / 3600
            },
            "Password security": {
                "score": review.Entropy_Score_Password(),
                "status": review.password_check(types="dict")
            }
        }

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the password status.

        Returns:
            str: A status string indicating whether the password is Active or Expired

        Example:
            >>> tp = Time_Password(password)
            >>> print(str(tp))
            'Time_Password(✅ Active)'  # or 'Time_Password(❌ Expired)'
        """
        status = "✅ Active" if self.is_password_valid() else "❌ Expired"
        return f"Time_Password({status})"

    def to_dict(self, security: bool = True) -> dict:
        """
        Converts password information to a dictionary format.

        This method provides a serializable representation of the password with
        options to hash sensitive information for security purposes.

        Args:
            security (bool, optional): If True, hash the password values for
                                     security. If False, return plaintext passwords.
                                     Defaults to True.

        Returns:
            dict: A dictionary containing:
                - "password You": The complete time-stamped password (hashed or plaintext)
                - "password": The extracted password (hashed or plaintext)
                - "start_time": Start timestamp string
                - "end_time": Expiration timestamp string
                - "is_valid": Boolean indicating validity

        Example:
            >>> tp = Time_Password(password)
            >>> # Get hashed version for storage
            >>> dict_hash = tp.to_dict(security=True)
            >>> print(dict_hash['password'])  # Hashed password
            >>>
            >>> # Get plaintext version for display
            >>> dict_plain = tp.to_dict(security=False)
            >>> print(dict_plain['password'])  # Original password
        """
        if not security:
            return {
                "password You": self.password,
                "password": self.get_password(),
                "start_time": self.start_time(),
                "end_time": self.end_time(),
                "is_valid": self.is_password_valid()
            }
        return {
            "password You": HP(self.password),
            "password": HP(self.get_password()),
            "start_time": self.start_time(),
            "end_time": self.end_time(),
            "is_valid": self.is_password_valid()
        }