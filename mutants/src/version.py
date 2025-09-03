"""
Version and build information module.
"""
import os
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result

class BuildInfo:
    """Container for build and version information."""
    
    def xǁBuildInfoǁ__init____mutmut_orig(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_1(self):
        self.version = None
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_2(self):
        self.version = os.getenv(None, 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_3(self):
        self.version = os.getenv('APP_VERSION', None)
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_4(self):
        self.version = os.getenv('unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_5(self):
        self.version = os.getenv('APP_VERSION', )
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_6(self):
        self.version = os.getenv('XXAPP_VERSIONXX', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_7(self):
        self.version = os.getenv('app_version', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_8(self):
        self.version = os.getenv('APP_VERSION', 'XXunknownXX')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_9(self):
        self.version = os.getenv('APP_VERSION', 'UNKNOWN')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_10(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = None
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_11(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv(None, 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_12(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', None)
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_13(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_14(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', )
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_15(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('XXBUILD_DATEXX', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_16(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('build_date', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_17(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'XXunknownXX')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_18(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'UNKNOWN')
        self.git_commit = os.getenv('GIT_COMMIT', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_19(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = None
    
    def xǁBuildInfoǁ__init____mutmut_20(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv(None, 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_21(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', None)
    
    def xǁBuildInfoǁ__init____mutmut_22(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('unknown')
    
    def xǁBuildInfoǁ__init____mutmut_23(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', )
    
    def xǁBuildInfoǁ__init____mutmut_24(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('XXGIT_COMMITXX', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_25(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('git_commit', 'unknown')
    
    def xǁBuildInfoǁ__init____mutmut_26(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'XXunknownXX')
    
    def xǁBuildInfoǁ__init____mutmut_27(self):
        self.version = os.getenv('APP_VERSION', 'unknown')
        self.build_date = os.getenv('BUILD_DATE', 'unknown')
        self.git_commit = os.getenv('GIT_COMMIT', 'UNKNOWN')
    
    xǁBuildInfoǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBuildInfoǁ__init____mutmut_1': xǁBuildInfoǁ__init____mutmut_1, 
        'xǁBuildInfoǁ__init____mutmut_2': xǁBuildInfoǁ__init____mutmut_2, 
        'xǁBuildInfoǁ__init____mutmut_3': xǁBuildInfoǁ__init____mutmut_3, 
        'xǁBuildInfoǁ__init____mutmut_4': xǁBuildInfoǁ__init____mutmut_4, 
        'xǁBuildInfoǁ__init____mutmut_5': xǁBuildInfoǁ__init____mutmut_5, 
        'xǁBuildInfoǁ__init____mutmut_6': xǁBuildInfoǁ__init____mutmut_6, 
        'xǁBuildInfoǁ__init____mutmut_7': xǁBuildInfoǁ__init____mutmut_7, 
        'xǁBuildInfoǁ__init____mutmut_8': xǁBuildInfoǁ__init____mutmut_8, 
        'xǁBuildInfoǁ__init____mutmut_9': xǁBuildInfoǁ__init____mutmut_9, 
        'xǁBuildInfoǁ__init____mutmut_10': xǁBuildInfoǁ__init____mutmut_10, 
        'xǁBuildInfoǁ__init____mutmut_11': xǁBuildInfoǁ__init____mutmut_11, 
        'xǁBuildInfoǁ__init____mutmut_12': xǁBuildInfoǁ__init____mutmut_12, 
        'xǁBuildInfoǁ__init____mutmut_13': xǁBuildInfoǁ__init____mutmut_13, 
        'xǁBuildInfoǁ__init____mutmut_14': xǁBuildInfoǁ__init____mutmut_14, 
        'xǁBuildInfoǁ__init____mutmut_15': xǁBuildInfoǁ__init____mutmut_15, 
        'xǁBuildInfoǁ__init____mutmut_16': xǁBuildInfoǁ__init____mutmut_16, 
        'xǁBuildInfoǁ__init____mutmut_17': xǁBuildInfoǁ__init____mutmut_17, 
        'xǁBuildInfoǁ__init____mutmut_18': xǁBuildInfoǁ__init____mutmut_18, 
        'xǁBuildInfoǁ__init____mutmut_19': xǁBuildInfoǁ__init____mutmut_19, 
        'xǁBuildInfoǁ__init____mutmut_20': xǁBuildInfoǁ__init____mutmut_20, 
        'xǁBuildInfoǁ__init____mutmut_21': xǁBuildInfoǁ__init____mutmut_21, 
        'xǁBuildInfoǁ__init____mutmut_22': xǁBuildInfoǁ__init____mutmut_22, 
        'xǁBuildInfoǁ__init____mutmut_23': xǁBuildInfoǁ__init____mutmut_23, 
        'xǁBuildInfoǁ__init____mutmut_24': xǁBuildInfoǁ__init____mutmut_24, 
        'xǁBuildInfoǁ__init____mutmut_25': xǁBuildInfoǁ__init____mutmut_25, 
        'xǁBuildInfoǁ__init____mutmut_26': xǁBuildInfoǁ__init____mutmut_26, 
        'xǁBuildInfoǁ__init____mutmut_27': xǁBuildInfoǁ__init____mutmut_27
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBuildInfoǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBuildInfoǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁBuildInfoǁ__init____mutmut_orig)
    xǁBuildInfoǁ__init____mutmut_orig.__name__ = 'xǁBuildInfoǁ__init__'
    
    def __str__(self):
        return f"Version: {self.version}, Build: {self.build_date}, Commit: {self.git_commit}"
    
    def xǁBuildInfoǁto_dict__mutmut_orig(self):
        return {
            'version': self.version,
            'build_date': self.build_date,
            'git_commit': self.git_commit
        }
    
    def xǁBuildInfoǁto_dict__mutmut_1(self):
        return {
            'XXversionXX': self.version,
            'build_date': self.build_date,
            'git_commit': self.git_commit
        }
    
    def xǁBuildInfoǁto_dict__mutmut_2(self):
        return {
            'VERSION': self.version,
            'build_date': self.build_date,
            'git_commit': self.git_commit
        }
    
    def xǁBuildInfoǁto_dict__mutmut_3(self):
        return {
            'version': self.version,
            'XXbuild_dateXX': self.build_date,
            'git_commit': self.git_commit
        }
    
    def xǁBuildInfoǁto_dict__mutmut_4(self):
        return {
            'version': self.version,
            'BUILD_DATE': self.build_date,
            'git_commit': self.git_commit
        }
    
    def xǁBuildInfoǁto_dict__mutmut_5(self):
        return {
            'version': self.version,
            'build_date': self.build_date,
            'XXgit_commitXX': self.git_commit
        }
    
    def xǁBuildInfoǁto_dict__mutmut_6(self):
        return {
            'version': self.version,
            'build_date': self.build_date,
            'GIT_COMMIT': self.git_commit
        }
    
    xǁBuildInfoǁto_dict__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBuildInfoǁto_dict__mutmut_1': xǁBuildInfoǁto_dict__mutmut_1, 
        'xǁBuildInfoǁto_dict__mutmut_2': xǁBuildInfoǁto_dict__mutmut_2, 
        'xǁBuildInfoǁto_dict__mutmut_3': xǁBuildInfoǁto_dict__mutmut_3, 
        'xǁBuildInfoǁto_dict__mutmut_4': xǁBuildInfoǁto_dict__mutmut_4, 
        'xǁBuildInfoǁto_dict__mutmut_5': xǁBuildInfoǁto_dict__mutmut_5, 
        'xǁBuildInfoǁto_dict__mutmut_6': xǁBuildInfoǁto_dict__mutmut_6
    }
    
    def to_dict(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBuildInfoǁto_dict__mutmut_orig"), object.__getattribute__(self, "xǁBuildInfoǁto_dict__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_dict.__signature__ = _mutmut_signature(xǁBuildInfoǁto_dict__mutmut_orig)
    xǁBuildInfoǁto_dict__mutmut_orig.__name__ = 'xǁBuildInfoǁto_dict'

# Global instance
build_info = BuildInfo()

def x_get_version_info__mutmut_orig():
    """Get formatted version information string."""
    return str(build_info)

def x_get_version_info__mutmut_1():
    """Get formatted version information string."""
    return str(None)

x_get_version_info__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_version_info__mutmut_1': x_get_version_info__mutmut_1
}

def get_version_info(*args, **kwargs):
    result = _mutmut_trampoline(x_get_version_info__mutmut_orig, x_get_version_info__mutmut_mutants, args, kwargs)
    return result 

get_version_info.__signature__ = _mutmut_signature(x_get_version_info__mutmut_orig)
x_get_version_info__mutmut_orig.__name__ = 'x_get_version_info'

def get_version_dict():
    """Get version information as dictionary."""
    return build_info.to_dict()
