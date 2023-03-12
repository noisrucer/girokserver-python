
from textual import log

def build_category_tree(parent, cats):
    """
    tree (textual.widgets.Tree object)
    cats: dictionary containing hierarchical category structure
    """
    for cat_name in cats:
        if cats[cat_name] == {}:
            cur = parent.add_leaf(cat_name)
        else:
            cur = parent.add(cat_name, expand=True)
            build_category_tree(cur, cats[cat_name])
            

def get_full_path_from_node(node):
    if str(node.label) == "Categories":
        return ""
    node_name = str(node.label)
    parent_path = get_full_path_from_node(node.parent)
    return parent_path + node_name + "/"
    
    
    