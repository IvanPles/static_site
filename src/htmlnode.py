
class HTMLNode:

    def __init__(self, **kwargs):
        self.tag = kwargs.get("tag", None)
        self.value = kwargs.get("value", None)
        self.children = kwargs.get("children", [])
        self.props = kwargs.get("props", {})

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return " ".join([f'{k}="{v}"' for k, v in self.props.items()])
    
    def __repr__(self):
        tag_val = f"tag={self.tag}, value={self.value}"
        child_repr = "children: " + "\n".join([ch.__repr__() for ch in self.children])
        props_repr = self.props_to_html()
        return "\n".join([tag_val, child_repr, props_repr])


class LeafNode(HTMLNode):

    def __init__(self, value, **kwargs):
        super().__init__(value=value, **kwargs)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return f"{self.value}"
        if self.props:
            first_tag = f"<{self.tag} {self.props_to_html()}>"
        else:
            first_tag = f"<{self.tag}>"
        last_tag = f"</{self.tag}>"
        res_html = first_tag + f"{self.value}" + last_tag
        return res_html

class ParentNode(HTMLNode):

    def __init__(self, tag, children, **kwargs):
        super().__init__(tag=tag, children=children, **kwargs)

    def to_html(self):
        if self.props:
            first_tag = f"<{self.tag} {self.props_to_html()}>"
        else:
            first_tag = f"<{self.tag}>"
        last_tag = f"</{self.tag}>" 
        res_html = first_tag
        for ch in self.children:
            res_html = res_html + ch.to_html()
        res_html = res_html + last_tag
        return res_html

