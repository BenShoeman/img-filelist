class DirectoryHTMLText:
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
        return DirectoryPlainText.__get_tree_text(root, 0)[:-1]
    
    def __get_tree_text(root, depth):
        tree_text = DirectoryPlainText.__get_depth_text(root, depth) + '`' + root.name + '`' + "\n"
        for child in root.children:
            if isinstance(child, File):
                tree_text += DirectoryPlainText.__get_depth_text(root, depth+1) + child.name + "\n"
            elif isinstance(child, Directory):
                tree_text += DirectoryPlainText.__get_tree_text(child, depth+1)
        return tree_text
    
    def __get_depth_text(root, depth):
        return "|   " * (0 if depth < 1 else depth-1) + ("" if depth == 0 else "|-- ")

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
    
    def add_child(self, child):
        if isinstance(child, Directory) or isinstance(child, File):
            self.__children.append(child)
    
    def add_directory(self, name):
        path = name.split('/')
        if len(path) == 1:
            self.find_or_create_directory(path[0])
        else:
            self.find_or_create_directory(path[0]).add_directory('/'.join(path[1:]))
    
    def add_file(self, name):
        path = name.split('/')
        if len(path) == 1:
            self.add_child(File(name))
        else:
            self.find_or_create_directory(path[0]).add_file('/'.join(path[1:]))
    
    def find_or_create_directory(self, name):
        for x in self.__children:
            if x.name == name and isinstance(x, Directory):
                return x
        child = Directory(name)
        self.add_child(child)
        return child
    
    # def get_tree_text(self):
    #     This is now a public attribute determined by treeprint. Should work when called
    
    def __repr__(self):
        return "Directory('" + self.name.replace("'", "\\'") + "', [" + ", ".join(x.__repr__() for x in self.__children) + "])"

class File:
    def __init__(self, name):
        self.__name = name
    
    @property
    def name(self):
        return self.__name
    
    def __repr__(self):
        return "File('" + self.name.replace("'", "\\'") + "')"