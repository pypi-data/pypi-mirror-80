from PropBank.RoleSet cimport RoleSet


cdef class Predicate(object):

    def __init__(self, lemma: str):
        """
        A constructor of Predicate class which takes lemma as input and initializes lemma with this input.
        The constructor also initializes the roleSets array.

        PARAMETERS
        ----------
        lemma : str
            Lemma of the predicate
        """
        self.__lemma = lemma
        self.__roleSets = []

    cpdef str getLemma(self):
        """
        Accessor for lemma.

        RETURNS
        -------
        str
            lemma.
        """
        return self.__lemma

    cpdef addRoleSet(self, RoleSet roleSet):
        """
        The addRoleSet method takes a RoleSet as input and adds it to the roleSets list.

        PARAMETERS
        ----------
        roleSet : RoleSet
            RoleSet to be added
        """
        self.__roleSets.append(roleSet)

    cpdef int size(self):
        """
        The size method returns the size of the roleSets list.

        RETURNS
        -------
        int
            the size of the roleSets list.
        """
        return len(self.__roleSets)

    cpdef RoleSet getRoleSet(self, int index):
        """
        The getRoleSet method returns the roleSet at the given index.

        PARAMETERS
        ----------
        index : int
            Index of the roleSet

        RETURNS
        -------
        RoleSet
            RoleSet at the given index.
        """
        return self.__roleSets[index]

    cpdef RoleSet getRoleSetWithId(self, str roleId):
        """
        Another getRoleSet method which returns the roleSet with the given roleSet id.

        PARAMETERS
        ----------
        roleId : str
            Id of the searched roleSet

        RETURNS
        -------
        RoleSet
            RoleSet which has the given id.
        """
        for roleSet in self.__roleSets:
            if roleSet.getId() == roleId:
                return roleSet
        return None
