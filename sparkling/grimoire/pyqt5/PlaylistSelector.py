# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
# pip install
import pandas as pd
from PyQt5.QtCore import pyqtSignal, Qt
# same project
# columns
from sparkling.grimoire.PlaylistColumns import (
    ColumnsPlaylist,
    NODE, DB_DEFAULT,
    LABEL_SEPARATOR, MULTIVALUE_SEPARATOR
    )
# common
from sparkling.common.pyqt5.ActionDefinitionsColumns import ColumnsActionDefinitions
from sparkling.grimoire.pyqt5.NodeViewer import NodeViewer
        
PLAYLIST_COLUMNS_TO_SHOW = [
    ColumnsPlaylist.title,
    ColumnsPlaylist.db_name,
    ]

class PlaylistSelector( NodeViewer ):
    
    # I want to browse existing playists.
    # Contents of opened playlists are available in a
    # dedicated `PlaylistViewer`.

    PLAYLIST_OPEN = pyqtSignal( pd.DataFrame )
    PLAYLIST_EDITED = pyqtSignal( pd.DataFrame )
    
    _conn = None

    def __init__( self,
                  parent=None,
                  *args, **kwargs ):
        super( PlaylistSelector, self ).__init__(
            parent=parent,
            accept_drops=False,
            *args, **kwargs )
        
        self.__init_context_menu()
        
        # i only need this data for this widget to work
        self.set_settings( {ColumnsPlaylist.db_name:DB_DEFAULT} )
        
    def __init_context_menu( self ):
        
        # Called once upon init.
        
        # short name for convenience
        c = ColumnsActionDefinitions
        
        actions = [
            {
                c.identity: 'grimoire/playlist_selector/playlist/open',
                c.text: 'Open',
                c.method: self.open_selected_playlists,
                },
            {
                c.identity: 'grimoire/node_viewer/row/edit',
                c.text: 'Edit',
                c.method: self.launch_selection_editor,
                },
            {
                c.identity: 'grimoire/playlist_selector/playlist/new',
                c.text: 'New',
                c.method: self.new_playlist,
                },
            {
                c.identity: 'grimoire/playlist_selector/playlist/delete',
                c.text: 'Delete',
                c.method: self.del_from_view_db,
                },
            # {
            #     c.identity: 'grimoire/playlist_selector/playlist/export_db_to_csv',
            #     c.text: 'Export db to .csv',
            #     c.method: self.export_db_to_csv,
            #     },
            # {
            #     c.identity: 'grimoire/playlist_selector/playlist/export_playlist_to_csv',
            #     c.text: 'Export playlist to .csv',
            #     c.method: self.export_playlist_to_csv,
            #     },
            # {
            #     c.identity: 'grimoire/playlist_selector/playlist/import_csv_to_db',
            #     c.text: 'Import .csv to db',
            #     c.method: self.import_csv_to_playlist,
            #     },
            ]
        
        # i want to fully replace parent context menu
        # so that `PlaylistSelector`'s functionality is limited
        c.remove_actions( self )
        c.add_actions( self, actions )
        
    def mouseDoubleClickEvent( self, ev ):
    
        if ev.button()==Qt.LeftButton:
            self.open_selected_playlists()
        
    def download_playlists( self ):#, conn ):
        
        # I want to download info regarding `playlists`.
        # Without actually downloading contents of these `playlists`.
        
        # TODO
        # download only limited predefined columns, because
        # in `PlaylistSelector` i don't need
        # - identities
        # - auto query
        # - plugins
        # - etc
        
        # for now i download full playlists metadata
        # and store it in self
        
        c = ColumnsPlaylist
        
        df = c.get_playlists( self._conn )
        
        self.switch_df( df, columns_to_hide=PLAYLIST_COLUMNS_TO_SHOW, appropriate_reverse=True )
        
    def new_playlist( self ):#, conn ):
        
        # Alternative `create new row`.
        
        c = ColumnsPlaylist
        
        df = c.new_playlist( self._conn )
        
        # i use df instead of `dict` in order to get
        # 100% accurate node.identity value
        # in current self._MODEL.df.index
        # avoid using `add_rows`
        self.add_df( df )
        
    def open_selected_playlists( self ):
        
        # Opens specific playlists chosen from gui.
        
        rowilocs = self.selected_rowilocs()
        if len(rowilocs)==0: return
        
        df2open = self._MODEL.df.iloc[ rowilocs ]
        
        self.PLAYLIST_OPEN.emit( df2open )
    
    def launch_selection_editor( self ):
        
        # TODO
        # custom editor
        # with convenient comboboxes, etc
        
        super( PlaylistSelector, self ).launch_selection_editor()
        
    def _accept_selection_edits_event( self, changes, db_name ):
    
        new_df = super( PlaylistSelector, self )._accept_selection_edits_event( changes, db_name )
        
        self.reapply_columns_to_hide( columns_to_hide=PLAYLIST_COLUMNS_TO_SHOW, appropriate_reverse=True )
        
        # tell everyone that some playlists
        # changed somehow
        
        self.PLAYLIST_EDITED.emit( new_df )
        
#---------------------------------------------------------------------------+++
# end 2023.10.07
# simplified
