from typing import List
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
class ChannelPoster:
    def xǁChannelPosterǁ__init____mutmut_orig(self, bot_instance, channel_id: int):
        self.bot = bot_instance
        self.channel_id = channel_id
    def xǁChannelPosterǁ__init____mutmut_1(self, bot_instance, channel_id: int):
        self.bot = None
        self.channel_id = channel_id
    def xǁChannelPosterǁ__init____mutmut_2(self, bot_instance, channel_id: int):
        self.bot = bot_instance
        self.channel_id = None
    
    xǁChannelPosterǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁChannelPosterǁ__init____mutmut_1': xǁChannelPosterǁ__init____mutmut_1, 
        'xǁChannelPosterǁ__init____mutmut_2': xǁChannelPosterǁ__init____mutmut_2
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁChannelPosterǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁChannelPosterǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁChannelPosterǁ__init____mutmut_orig)
    xǁChannelPosterǁ__init____mutmut_orig.__name__ = 'xǁChannelPosterǁ__init__'

    async def post_article(self, telegraph_urls: List[str]):
        """
        Post one or multiple Telegraph URLs to the channel
        """
        pass
            