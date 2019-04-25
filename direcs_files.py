# DirectoryHTMLText and DirectoryPlainText simply define the behavior of getting
# the text of a directory tree of class Directory. Directory objects use the
# get_tree_text method from these functions, and custom directory text output
# can be defined using a similar class with a get_tree_text method defined.
# ---
# If you want to define custom behavior and are confused where to start, create
# a new class based on the DirectoryPlainText and modify the methods from there.

class DirectoryHTMLText:
    # This class follows the same structure as DirectoryPlainText, just using
    # HTML tags instead to clearly indicate what's a directory vs what's a file
    def get_tree_text(root):
        return "<pre>" + DirectoryHTMLText.__get_tree_text(root, 0)[:-6] + "</pre>"
    
    def __get_tree_text(root, depth):
        tree_text = DirectoryHTMLText.__get_depth_text(root, depth) + "<strong>" + root.name + "</strong>" + "<br/>\n"
        for child in root.children:
            if isinstance(child, File):
                tree_text += DirectoryHTMLText.__get_depth_text(root, depth+1) + child.name + "<br/>\n"
            elif isinstance(child, Directory):
                tree_text += DirectoryHTMLText.__get_tree_text(child, depth+1)
        return tree_text
    
    def __get_depth_text(root, depth):
        return "|   " * (0 if depth < 1 else depth-1) + ("" if depth == 0 else "|-- ")

class DirectoryPlainText:
    def get_tree_text(root):
        # Get the tree text but remove the last newline character
        return DirectoryPlainText.__get_tree_text(root, 0)[:-1]
    
    # Helper method to get the tree text that runs recursively
    def __get_tree_text(root, depth):
        # `Backticks` are used to indicate what's a directory. That can be
        # changed on this line by replacing the backticks with another character
        tree_text = DirectoryPlainText.__get_depth_text(root, depth) + '`' + root.name + '`' + "\n"
        for child in root.children:
            # If the child is just a file, add it to the tree text and move on
            if isinstance(child, File):
                tree_text += DirectoryPlainText.__get_depth_text(root, depth+1) + child.name + "\n"
            # If the child is a directory, recursively get the tree text of it
            elif isinstance(child, Directory):
                tree_text += DirectoryPlainText.__get_tree_text(child, depth+1)
        return tree_text
    
    # This simply prints the "depth lines" to indicate how deep the directory or
    # file is in the current structure. This increases by 1 every time a
    # directory is found in the __get_tree_text method, and these lines are
    # included for every file in a directory
    def __get_depth_text(root, depth):
        return "|   " * (0 if depth < 1 else depth-1) + ("" if depth == 0 else "|-- ")

# This class represents a directory, and its get_tree_text method is defined
# using the class passed into treeprint. This class could be modified in the
# future to have info like created/modified dates, permissions, etc.
class Directory:
    def __init__(self, name, children=None, treeprint=DirectoryPlainText):
        self.__name = name
        if children is None:
            self.__children = []
        else:
            self.__children = children
        self.get_tree_text = lambda: treeprint.get_tree_text(self)
    
    @property
    def name(self):
        return self.__name
    
    @property
    def children(self):
        return tuple(self.__children)
    
    # Adds a child (either a File or Directory object). Mostly a helper for
    # find_or_create_directory but could be directly used if needed.
    def add_child(self, child):
        if isinstance(child, Directory) or isinstance(child, File):
            self.__children.append(child)
    
    # Creates a directory using a file path, like "folder1/.../folder2". All
    # necessary directories in that path will be created if they don't exist.
    def add_directory(self, name):
        path = name.split('/')
        if len(path) == 1:
            self.find_or_create_directory(path[0])
        else:
            self.find_or_create_directory(path[0]).add_directory('/'.join(path[1:]))
    
    # Creates a file using a file path, like "folder1/folder2/.../file.ext". All
    # necessary directories in that path will be created if they don't exist.
    def add_file(self, name):
        path = name.split('/')
        if len(path) == 1:
            self.add_child(File(name))
        else:
            self.find_or_create_directory(path[0]).add_file('/'.join(path[1:]))
    
    # Helper function for add_directory and add_file that finds the necessary
    # directory or, if it doesn't exist, creates it. In all cases it will return
    # the necessary directory
    def find_or_create_directory(self, name):
        for x in self.__children:
            if x.name == name and isinstance(x, Directory):
                return x
        child = Directory(name, treeprint=treeprint)
        self.add_child(child)
        return child
    
    # This function is defined through the treeprint attribute.
    # def get_tree_text(self)
    
    # Console representation of object visible when print(object) is called
    def __repr__(self):
        return "Directory('" + self.name.replace("'", "\\'") + "', [" + ", ".join(x.__repr__() for x in self.__children) + "])"

# This class represents a file. This class could be modified in the future to
# have info like created/modified dates, permissions, etc.
class File:
    def __init__(self, name):
        self.__name = name
    
    @property
    def name(self):
        return self.__name
    
    # Console representation of object visible when print(object) is called
    def __repr__(self):
        return "File('" + self.name.replace("'", "\\'") + "')"