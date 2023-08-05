from collections import deque
import heapq
from math import inf

class NotRelatableError(TypeError):

    def __init__(self, inst):
        self.inst = inst

    def __str__(self):
        return f"-<{self.inst.__class__.__name__}> not a subclass of <FamilyMember>-"


class TimeParadoxError(AttributeError):

    def __init__(self, obj, relationship, subj):
        """
        Loop detected in parent-child relationship

        Trying to set parent as child or child as parent.
        Translate attribute as `{obj} is {relationship} of {subj}`
        :param obj:
        :param relationship:
        :param subj:
        """
        self._obj = obj
        self._subj = subj
        self._relationship = relationship

    def __str__(self):
        return f"-{self._obj.__str__()} is already a {self._relationship.upper()} of {self._subj.__str__()}-"


class MemberIterator:
    def __init__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __call__(self, member):
        self._iterable(member)
        return self

class LevelIterator(MemberIterator):

    def __init__(self, iterable, step=inf):
        self._iterable = iterable
        self._step = step

    def __iter__(self):
        que = deque([(1, m) for m in self._iterable])
        visited = set()
        while que:
            level, member = que.popleft()
            if member not in visited and level <= self._step:
                visited.add(member)
                yield member
                que += [(level+1, m) for m in self._iterable(member)]


class PreorderIterator(MemberIterator):

    def __init__(self, iterable, step=inf):
        self._iterable = iterable
        self._step = step

    def __iter__(self):
        heap = [(1, i, m) for i, m in enumerate(self._iterable)]
        next_count = len(heap)
        depth_record = {m: 1 for m in self._iterable}

        while heap:
            level, _, member = heapq.heappop(heap)
            if depth_record.get(self, 0) >= level + 1:
                continue

            for next_member in self._iterable(member):
                if depth_record.get(next_member, 0) < level + 1:
                    depth_record[next_member] = level + 1
                    heapq.heappush(heap, (level+1, next_count, next_member))
                    next_count += 1

        for member, level in sorted(depth_record.items(), key=lambda x: x[1]):
            if level <= self._step:
                yield member


class PostorderIterator(MemberIterator):

    def __init__(self, iterable, visited=None):
        self._iterable = iterable
        self._visited = visited
        self.a = 10

    def __iter__(self):
        if self._visited is None:
            self._visited = set()
        for member in self._iterable:
            if member not in self._visited:
                self._visited.add(member)
                for i in PostorderIterator(self._iterable(member), self._visited):
                    yield i
                yield member


class TypeFilterIterator(MemberIterator):

    def __init__(self, iterable, typ):
        self._iterable = iterable
        self._typ = typ

    def __iter__(self):
        for member in self._iterable:
            if isinstance(member, self._typ):
                yield member


class ParentIterator(MemberIterator):

    def __init__(self):
        self._member = None

    def __iter__(self):
        for parent in self._member.fm_all_parents():
            yield parent

    def __call__(self, member):
        self._member = member
        return self


class ChildrenIterator(MemberIterator):

    def __init__(self):
        self._member = None

    def __iter__(self):
        for child in self._member.fm_all_children():
            yield child

    def __call__(self, member):
        self._member = member
        return self

class FirstDegreeIterator(MemberIterator):
    """
    Iter member's parent and children only
    """

    def __init__(self):
        self._member = None

    def __iter__(self):
        for parent in self._member.fm_all_parents():
            yield parent
        for child in self._child.fm_all_children():
            yield child

    def __call__(self, member):
        self._member = member
        return self


class FamilyMember:
    """
    Inheritor. Adds family tree functionality to class.
    Not like 'tree', this supports polygamy structure - multiple parent.
    Mono, polygamy functionality is supported by differentiating `set` `append` in method naming convention.
    """
    _ATTR_PREFIX = '_fm'
    PARENT = 0
    CHILD = 1

    PARENT_ITOR = ParentIterator
    CHILDREN_ITOR = ChildrenIterator
    TYPEFILTER_ITOR = TypeFilterIterator
    PREORDER_ITOR = PreorderIterator
    POSTORDER_ITOR = PostorderIterator
    LEVEL_ITOR = LevelIterator
    FIRSTDEGREE_ITOR = FirstDegreeIterator

    def __init__(self):
        self._relation_lst = ([], [])
        self._relation_set = (set(), set())

    def _typ_check(self, obj):
        if not isinstance(obj, FamilyMember):
            raise TypeError("not a member")

    def _paradox_check(self, relationship, subj):
        """
        Check Timeparadox.

        Whether trying to set parent as child of child as parent.
        Think of loop.
        Translate attributes as statement `{self} is {desired_rel} of {subj}`
        :param self: object
        :param relationship:
        :param subj:
        :return:
        """
        pass
        if relationship == self.PARENT:
            for offs in subj.fm_iter_member(subj.PREORDER_ITOR(subj.CHILDREN_ITOR())):
                if offs == self:
                    raise TimeParadoxError(subj, relationship, self)

        elif relationship == self.CHILD:
            for anc in subj.fm_iter_member(subj.PREORDER_ITOR(subj.PARENT_ITOR())):
                if anc == self:
                    raise TimeParadoxError(subj, relationship, self)
        else:
            raise TypeError

    def fm_append(self, obj, kind):
        """
        Appender
        :param obj:
        :param kind:
        :return:
        """
        self._typ_check(obj)
        self._paradox_check(not kind, obj)

        if obj not in self._relation_set[kind]:
            lst, st = self._relation_lst[kind], self._relation_set[kind]
            lst.append(obj)
            st.add(obj)

    def fm_remove(self, obj, kind):
        """
        Remover
        :param obj:
        :param kind:
        :return:
        """
        self._typ_check(obj)
        if obj in self._relation_set[kind]:
            lst, st = self._relation_lst[kind], self._relation_set[kind]
            lst.remove(obj)
            st.remove(obj)

    # bidirectional manipulator
    @classmethod
    def fm_append_member(cls, parent, child):
        """
        Record new bidirectional relationship as parent-child
        :param parent: member to be a parent
        :param child: member to be a child
        :return:
        """
        parent.fm_append(child, cls.CHILD)
        child.fm_append(parent, cls.PARENT)

    def fm_replace_member(self, old, new):
        """
        Replace member
        :param old:
        :param new:
        :return:
        """
        pass

    # def fm_remove_relationship(self, member1, member2):
    #     """
    #     Remove relationship between two members if there is one
    #     :param member1:
    #     :param member2:
    #     :return:
    #     """
    #     if member2 in member1.fm_all_parents():
    #         member1.fm_remove(member2, self.PARENT)
    #         member2.fm_remove(member1, self.CHILD)
    #     elif member1 in member2.fm_all_parents():
    #         member1.fm_remove(member2, self.CHILD)
    #         member2.fm_remove(member1, self.PARENT)

    def fm_clear_parent(self):
        for parent in self.fm_all_parents():
            parent.fm_remove(self, self.CHILD)
            self.fm_remove(parent, self.PARENT)

    def fm_clear_children(self):
        for child in self.fm_all_children():
            child.fm_remove_parent(self)


    # checker
    def fm_has_parent(self):
        return bool(self._relation_lst[self.PARENT])

    def fm_has_child(self):
        return bool(self._relation_lst[self.CHILD])

    # getter
    def fm_get_child(self, idx):
        """
        Return child of given idx
        :param idx: index of desired children
        :return: child
        """
        return self._relation_lst[self.CHILD][idx]

    def fm_get_parent(self, idx):
        """
        Return parent of given idx
        :param idx: index of desired parent
        :return:
        """
        return self._relation_lst[self.PARENT][idx]
    #
    # def fm_get_ancestor(self, gen, idx):
    #     ancestors = [self]
    #     for i in range(gen):
    #         new_ancestors = []
    #         visited = set()
    #         for ancestor in ancestors:
    #             for e in ancestor.fm_all_parents():
    #                 if e not in visited:
    #                     visited.add(e)
    #                     new_ancestors.append(e)
    #         ancestors = new_ancestors
    #     return ancestors[idx]

    def fm_get_roots(self, visited=set()):
        """
        Return roots of family tree

        For monopoly parent family tree, single value list will be returned.
        Else does simple BFS search and returns all roots - member that has no parent
        :param visited: do not assign, in-function variable to prevent duplication
        :return: [single_root] or [roots, ...]
        """
        roots = []
        if not self._relation_set[self.PARENT]:
            return [self]
        else:
            for p in self.fm_all_parents():
                if p not in visited:
                    visited.add(p)
                    roots += p.fm_get_roots(visited=visited)
        return roots

    def fm_all_parents(self):
        """
        Return list copy of parents
        :return:
        """
        return self._relation_lst[self.PARENT].copy()

    def fm_all_children(self):
        """
        Return list copy of children
        :return:
        """
        return self._relation_lst[self.CHILD].copy()

    def fm_iter_member(self, iterator):
        return iterator(self)