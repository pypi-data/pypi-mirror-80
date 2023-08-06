import os, sys

### Controller object

class MdreeController:
    def __init__(self):
        self.rootnode = None
        self.pathstack = []
        self.magnitudepath = []
        self.file_path = "."

### Node logic

class TagValue:
    # Initializes tag metadata
    # @param path is the path of the tag target
    # @param req is the list of tags that are required for this tag to be resolvable
    # @param callback is the function that is called to resolve the tag. The callback has
    #                 to take an argument of dictionary, where keys are tags and values are the path
    def __init__(self, req, callback):
        self.req = req
        self.callback = callback

        self.resolved = False

    def resolve(self, requirement_dict, path):
        self.resolved = True

        return self.callback(requirement_dict, path)

    def is_resolved(self):
        return self.resolved

class MdreeNode:
    # Initializes Node object
    # @param tags is dict with tag as key and TagValue as the value
    # @param children is list of child Nodes
    def __init__(self, tags, children):
        self.tags = tags
        self.children = children
        self.controller = MdreeController()

        self.checked_tags = {}
        self.checked_tags.update(self.tags.keys())

    def _set_controller(self, controller):
        self.controller = controller

    # Does the node have instructions for the tag?
    def has_tag(self, tag):
        return tag in self.tags.keys()

    def get(self, tag):
        # If the tag has already been checked for this node, skip
        if tag in self.checked_tags:
            return None

        self.checked_tags.add(tag)

        # Set the controller for the children
        for child in self.children:
            child._set_controller(self.controller)

        self.controller.pathstack.append(self)
        self.controller.magnitudepath.append(self)

        ## Find the tag
        if not self.has_tag(tag):
            for child in self.children:
                target = child.get(tag)
                if target is not None:
                    return target

            return None

        ## Tag can be provided by this node
        # Get the metadata about the tag
        tagdata = self.tags[tag]

        # List of requirements
        reqs = set(tagdata.req)

        ## Handle the requirement for the tag
        requirements_resolved = False

        # Create the dict for the requirements
        requirement_dict = {}

        # Go through children
        for child in self.children.keys():
            removed = set()

            self.controller.file_path = os.path.join(self.controller.filePath, self.children[child])

            for req in reqs:
                #print(f"Child: {tag} requires {req}")
                cget = child.get(req)
                if cget is not None:
                    requirement_dict[req] = cget #.path
                    removed.add(req)

            self.controller.filePath = self.controller.filePath.rsplit(os.sep, 1)[0]

            # Remove handled requirements
            reqs = reqs.difference(removed)

            # If all the requirements are handled
            if len(reqs) == 0:
                requirements_resolved = True
                break

        # If children didn't have the requirements
        # Ask from the parent
        if not requirements_resolved:
            if len(self.controller.magnitudepath) == 1:
                return None

            thisnode = self.controller.magnitudepath[-1]
            del self.controller.magnitudepath[-1]

            parent = self.controller.magnitudepath[-1]

            for req in reqs:
                cget = parent.get(req)
                if cget is not None:
                    requirement_dict[req] = cget #.path

                else
                    raise Exception(f'Could not find tag: {req}')


            self.controller.magnitudepath += [thisnode]

        # Resolve the tag
        return tagdata.resolve(requirement_dict, self.controller.file_path)
