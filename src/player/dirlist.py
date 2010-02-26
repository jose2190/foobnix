'''
Created on Feb 26, 2010

@author: ivan
'''
import gtk
import os
import LOG

class DirectoryList:
    def __init__(self, root_directory, directoryListWidget):
        self.root_directory = root_directory        
        
        column = gtk.TreeViewColumn("Title", gtk.CellRendererText(), text=0)
        column.set_resizable(True)
        directoryListWidget.append_column(column)
        self.direcotryTreeModel = gtk.TreeStore(str, str)                
        directoryListWidget.set_model(self.direcotryTreeModel)

        self.addAll()
    
    def addAll(self):
        level = None;
        self.go_recursive(self.root_directory, level)    
              
    def go_recursive(self, path, level):
            
        dir = os.path.abspath(path)
        list = os.listdir(dir)
                
        for file in list:
            
            full_path = path + "/" + file        
            sub = self.direcotryTreeModel.append(level, [file, full_path])              
            
            if os.path.isdir(full_path):
                LOG.debug("directory", file)                    
                self.go_recursive(full_path, sub) 
            else:
                LOG.debug("file", file)                             