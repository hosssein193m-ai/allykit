"""
AllyKit Password 
"""

# Imports from core modules
from .Time_based_password import wrap_password_with_time, generate_timed_password, Time_Password, generating_password
from .password import (choice_string , choice_string_yield , 
                       str_choice_string ,list_choice_string , 
                       generate_password , generate_strong_password,
                       generate_password_with_prefix_suffix)
from .Scoring_password import Review_Password

# ---------- Password Generation Functions ----------
WPWT = wrap_password_with_time          # Wrap password with time
GTP = generate_timed_password           # Generate timed password
GP = generate_password_with_prefix_suffix  # Generate with prefix/suffix
GSP = generate_strong_password          # Generate strong password
G = generate_password                   # Generate simple password
GPT = generating_password               

# ---------- Character Generation Functions ----------
CS = choice_string                      # Random character
CSY = choice_string_yield               # Yield sequence of characters
SCS = str_choice_string                 # Random string
LCS = list_choice_string                # Character list

# ---------- Core Classes ----------
ReviewPassword = Review_Password        # Evaluate password strength
TimePassword = Time_Password            # Manage timed password
