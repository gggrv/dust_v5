# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
import os
# pip install
# same project
from sparkling.common.SomeDoer import SomeDoer
    
class Paths:
    
    __CODE_ROOT = os.path.dirname( __file__ )
    __APPLICATION_ROOT = os.path.dirname( __CODE_ROOT )
    __DATA_ROOT = os.path.join( __APPLICATION_ROOT, 'data' )
    
    # in the future
    # create object that will manage core paths
    # right now i don't need it
    __OwnDoer = None
    
    @staticmethod
    def get_code_root():
        # Returns the root folder of the main code.
        return Paths.__CODE_ROOT
    
    @staticmethod
    def get_application_root():
        # Returns the root folder of this application.
        return Paths.__APPLICATION_ROOT
    
    @staticmethod
    def get_data_root():
        # Returns the root folder of the user
        # customizeable data folder
        # that is managed by __MasterDoer.
        return Paths.__DATA_ROOT
    
    @staticmethod
    def _get_own_doer():
        
        # Should not be used outside of this static class.
        # For how is hidden rather then private for
        # debug purposes.
        
        # make sure it exists
        if( Paths.__OwnDoer is None ):
            
            Paths.__OwnDoer = SomeDoer(
                Paths.__DATA_ROOT
                )
            
        return Paths.__OwnDoer
    
        
    @staticmethod
    def set_file( filename ):
        
        OwnDoer = Paths._get_own_doer()
        src = OwnDoer.set_file( filename )
        
        return src
        
    @staticmethod
    def set_folder( dirname ):
        
        OwnDoer = Paths._get_own_doer()
        src = OwnDoer.set_folder( dirname )
            
        return src

#---------------------------------------------------------------------------+++
# end 2023.05.11
# simplified
