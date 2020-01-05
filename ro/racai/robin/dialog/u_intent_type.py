from enum import Enum

"""
<p>User intent type: add new types here, as required.</p>
SAY_SOMETHING:
User wants some explanation from Pepper

TAKE_ME_SOMEWHERE:
User wants Pepper to take him/her somewhere

BRING_ME_THAT:
 User wants Pepper to bring him/her something
 
 SHOW_ME_HOW:
 User wants Pepper to show him/her how to do something
"""
UIntentType = Enum("UIntentType", ("SAY_SOMETHING",
                                   "TAKE_ME_SOMEWHERE",
                                   "BRING_ME_THAT",
                                   "SHOW_ME_HOW"))
