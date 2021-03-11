# PURP: - TO PROVIDE A CENTRAL FILE FOR STRINGS REPEATEDLY USED THROUGHOUT THE PROJECT. 

# MARK: - Logger File Basic Config constants
LOG_FORMAT = '%(levelname)s: %(asctime)s: %(message)s'
LOG_DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'

# MARK: - Logger constants strings
COMP_ERROR = "Computational Errors"

# MARK: drive_dump.py constants
# NOTE: - Why? Cause Fuck Network Drives that's why.

# drive types
DRIVE_UNKNOWN     = 0  # The drive type cannot be determined.
DRIVE_NO_ROOT_DIR = 1  # The root path is invalid; for example, there is no volume mounted at the specified path.
DRIVE_REMOVABLE   = 2  # The drive has removable media; for example, a floppy drive, thumb drive, or flash card reader.
DRIVE_FIXED       = 3  # The drive has fixed media; for example, a hard disk drive or flash drive.
DRIVE_REMOTE      = 4  # The drive is a remote (network) drive.
DRIVE_CDROM       = 5  # The drive is a CD-ROM drive.
DRIVE_RAMDISK     = 6  # The drive is a RAM disk.

# map drive types to strings
DRIVE_TYPE_MAP = { DRIVE_UNKNOWN     : 'DRIVE_UNKNOWN',
                   DRIVE_NO_ROOT_DIR : 'DRIVE_NO_ROOT_DIR',
                   DRIVE_REMOVABLE   : 'DRIVE_REMOVABLE',
                   DRIVE_FIXED       : 'DRIVE_FIXED',
                   DRIVE_REMOTE      : 'DRIVE_REMOTE',
                   DRIVE_CDROM       : 'DRIVE_CDROM',
                   DRIVE_RAMDISK     : 'DRIVE_RAMDISK'}

MAC_OS = 'Darwin'
LINUX = 'Linux'
WINDOWS = 'Windows'

MACOS_DETECTED = 'MacOS System detected'
LINUX_DETECTED = 'Linux System detected'
WINDOWS_DETECTED = 'Windows System detected'

MACOS_CRITICAL = 'Can not read the MacOS structure'
LINUX_CRITICAL = 'Can not read the Linux structure'
WINDOWS_CRITICAL = 'Can not read the Windows structure'
INDIE_CRITICAL = 'Can not read the OS structure'

# arg constants
D = '-d'
DRV = '--drv'
L = '-l'
FLD = '--fld'
F = '-f'
FIL = '--fil'
T = '-t'
TYP = '--typ'