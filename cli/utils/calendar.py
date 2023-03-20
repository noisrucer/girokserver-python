from datetime import datetime
import calendar
from textual import log
import constants
from rich.text import Text
from rich.style import Style

def build_category_tree(parent, cats):
    """
    tree (textual.widgets.Tree object)
    cats: dictionary containing hierarchical category structure
    """
    for cat_name in cats:
        if cats[cat_name]['subcategories'] == {}:
            cur = parent.add_leaf(cat_name)
        else:
            cur = parent.add(cat_name, expand=True)
            build_category_tree(cur, cats[cat_name]['subcategories'])
            

def get_full_path_from_node(node):
    label = str(node._label)
    if label.endswith(" " + constants.LEFT_ARROW_EMOJI):
        label = label[:-2]
    else:
        pass
    if label == "All Categories":
        return ""
    elif label == "No Category":
        return "No Category"
    node_name = label
    parent_path = get_full_path_from_node(node.parent)
    return parent_path + node_name + "/"
    
    
def convert_day_to_cell_num(year: int, month: int, day: int):
    """
    
    """
    first_weekday, total_days = calendar.monthrange(year, month)
    return first_weekday + day - 1


def convert_cell_num_to_day(year: int, month: int, cell_num: int):
    first_weekday, total_days = calendar.monthrange(year, month)
    return cell_num - first_weekday + 1
    
    
def convert_cell_num_to_coord(cell_num: int):
    """
    cell_num: 0 ~ 34
    """
    
    return (cell_num // 7, cell_num % 7)


def convert_coord_to_cell_num(x: int, y: int):
    return x * 7 + y


def get_date_obj_from_str_separated_by_T(s: str):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")


def remove_left_arrow(cell):
    if not cell.children:
        return
    cell_label = cell.children[0]
    cell_label_text = str(cell_label.render())
    if cell_label_text.endswith(" " + constants.LEFT_ARROW_EMOJI):
        new_label_text = Text(cell_label_text[:2])
    else:
        new_label_text = Text(cell_label_text)
    cell_label.update(new_label_text)
    
    
def add_left_arrow(cell):
    if not cell.children:
        return
    cell_label = cell.children[0]
    cell_label_text = str(cell_label.render())
    if cell_label_text.endswith(" " + constants.LEFT_ARROW_EMOJI):
        new_label_text = cell_label_text
    else:
        new_label_text = Text.assemble(cell_label_text, " ", Text(constants.LEFT_ARROW_EMOJI, style=Style(color="red")))
    cell_label.update(new_label_text)
    

def remove_left_arrow_tree(node):
    style = node._label.style
    label_text = str(node._label)
    log("REMOVE", label_text, style)
    if label_text.endswith(" " + constants.LEFT_ARROW_EMOJI):
        label = Text(label_text[:-2], style=style)
        node.set_label(label)
    else:
        pass
    
def add_left_arrow_tree(node):
    style = node._label.style
    label = Text(str(node._label), style=style)
    if str(label).endswith(" " + constants.LEFT_ARROW_EMOJI):
        pass
    else:
        node.set_label(Text.assemble(label, " ", constants.LEFT_ARROW_EMOJI))
        
    
def remove_highlight(node):
    label = str(node._label)
    node.set_label(str(label))
    
    
def add_highlight(node):
    label = str(node._label)
    node.set_label(Text(label, style=Style(color="#9bdfbb")))