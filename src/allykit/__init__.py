# allykit/__init__.py
# allykit <<< ¶¶

"""
allykit - Ultimate Toolkit for Python Developers
===============================================
Dear friend, after installing this module, please run this command in your terminal so that you can use allykit correctly.
>>>  pip install selenium beautifulsoup4 requests tenacity deepdiff 
"""

# ==================== Automobile_kit ====================
from .Automobile_kit.Automobile.Cmd import cmd
from .Automobile_kit.Automobile.powerShell import PowerShell
from .Automobile_kit.New_automobile.python import Pip , Python
from .Automobile_kit.Automobile.hybrid import hash_password
from .Automobile_kit.New_automobile.file import File
from .Automobile_kit.New_automobile.git import Git
from allykit.Automobile_kit.ProcessManager import ( 
    ProcessManager,
    kill_process,
    kill_chrome, 
    kill_firefox, 
    kill_edge, 
    kill_all_browsers, 
    get_process_info,
    is_process_running,
    count_processes,
    suspend_process,
    resume_process,
    get_process_pids
)


# ==================== Tools_kit ====================
from .Tools_kit.file_tools import (
    remove_file,
    remove_files,
    is_dir,
    write_file,
    dump_file,
    load_file,
    read_file,
    get_permission,
    change_permission,
    get_stat_info,
    datetime_file,
    type_file,
    information_files,
    information_files_dict,
)

from .Tools_kit.string_tools import (
    choice_string,
    choice_string_yield,
    str_choice_string,
    list_choice_string,
)

# ==================== Security ====================
from .Security_kit import  (
    # Password
    choice_string , choice_string_yield , 
    str_choice_string ,list_choice_string , 
    generate_password , generate_strong_password,
    generate_password_with_prefix_suffix, 
    wrap_password_with_time, generate_timed_password, Time_Password, Review_Password,
    # file 
    hash_file, dict_files_in_directory , find_file , hash_file, save_dict_and_expected , dict_files_in_directory_bool,
    verify_snapshot , create_snapshot,
    # hash
    smart_hash_detector , detect_hash_algorithm, hash_file , hash_password, verify_password,
    hash_with_salt , generate_salt , find_matching_hashes , compare_hash , double_hash, 
    hash_url, calculate_file_hashes  
)


# ==================== Web ====================
from .web_kit import fix_url
from .web_kit.CChrome import chrome, get_headless_driver , browser_context, wait_for_element
from .web_kit.Communications import get_rate_limit_info, fetch_url, is_link_alive, validate_links, execute_request
from .web_kit.Elastic_bands import Monitoring, DiskCache
from .web_kit.Get_Code import soup_url, javascript, javascript_driver , javascript_pro
from .web_kit.WebAutomation import WebAutomation
from .web_kit.Working_with_code import SoupToDict, extract_structured_data , extract_all_links,extract_images,extract_text_from_tags,save_link,save_links
from .web_kit.Cookie import Cookie

# ==================== Language & Geography ====================
from .data_kit.Language import *

from .data_kit.country import *

from .data_kit.IRAN import *

# ==================== Version & Metadata ====================
__version__ = "1.3"
__author__ = None
__license__ = "MIT"
__status__ = "Alpha"