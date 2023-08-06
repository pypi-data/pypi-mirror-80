from PropBank.ArgumentType cimport ArgumentType
from PropBank.ArgumentTypeEnum cimport ArgumentTypeEnum
from PropBank.FramesetArgument cimport FramesetArgument
import xml.etree.ElementTree


cdef class Frameset(object):

    def __init__(self, fileName: str = None):
        """
        Another constructor of Frameset class which takes filename as input and reads the frameset

        PARAMETERS
        ----------
        fileName : str
            File name of the file to read frameset
        """
        if fileName is not None:
            root = xml.etree.ElementTree.parse(fileName).getroot()
            self.__id = root.attrib["id"]
            self.__framesetArguments = []
            for child in root:
                self.__framesetArguments.append(FramesetArgument(child.attrib["name"], child.text,
                                                                 child.attrib["function"]))
        else:
            self.__id = ""
            self.__framesetArguments = []

    cpdef bint containsArgument(self, ArgumentTypeEnum argumentType):
        """
        containsArgument method which checks if there is an Argument of the given argumentType.

        PARAMETERS
        ----------
        argumentType : ArgumentType
            ArgumentType of the searched Argument

        RETURNS
        -------
        bool
            true if the Argument with the given argumentType exists, false otherwise.
        """
        for framesetArgument in self.__framesetArguments:
            if ArgumentType.getArguments(framesetArgument.getArgumentType()) == argumentType:
                return True
        return False

    cpdef addArgument(self, str argumentType, str definition, str function = None):
        """
        The addArgument method takes a type and a definition of a FramesetArgument as input, then it creates a new
        FramesetArgument from these inputs and adds it to the framesetArguments list.

        PARAMETERS
        ----------
        argumentType : str
            Type of the new FramesetArgument
        definition : str
            Definition of the new FramesetArgument
        function: str
            Function of the new FramesetArgument
        """
        cdef FramesetArgument framesetArgument
        check = False
        for framesetArgument in self.__framesetArguments:
            if framesetArgument.getArgumentType() == argumentType:
                framesetArgument.setDefinition(definition)
                check = True
                break
        if not check:
            arg = FramesetArgument(argumentType, definition, function)
            self.__framesetArguments.append(arg)

    cpdef deleteArgument(self, str argumentType, str definition):
        """
        The deleteArgument method takes a type and a definition of a FramesetArgument as input, then it searches for the
        FramesetArgument with these type and definition, and if it finds removes it from the framesetArguments list.

        PARAMETERS
        ----------
        argumentType : str
            Type of the to be deleted FramesetArgument
        definition : str
            Definition of the to be deleted FramesetArgument
        """
        cdef FramesetArgument framesetArgument
        for framesetArgument in self.__framesetArguments:
            if framesetArgument.getArgumentType() == argumentType and framesetArgument.getDefinition() == definition:
                self.__framesetArguments.remove(framesetArgument)
                break

    cpdef list getFramesetArguments(self):
        """
        Accessor for framesetArguments.

        RETURNS
        -------
        list
            framesetArguments.
        """
        return self.__framesetArguments

    cpdef str getId(self):
        """
        Accessor for id.

        RETURNS
        -------
        str
            id.
        """
        return self.__id

    cpdef setId(self, str _id):
        """
        Mutator for id.

        PARAMETERS
        ----------
        _id : str
            id to set.
        """
        self.__id = _id

    cpdef save(self, str fileName):
        """
        Saves current frameset with the given filename.

        PARAMETERS
        ----------
        fileName : str
            Name of the output file.
        """
        outputFile = open(fileName, mode="w", encoding="utf-8")
        outputFile.write("<FRAMESET id=\"" + self.__id + "\">\n")
        for framesetArgument in self.__framesetArguments:
            outputFile.write("\t<ARG name=\"" + framesetArgument.getArgumentType() + "\" function=\"" +
                             framesetArgument.getFunction() + "\">" + framesetArgument.getDefinition() + "</ARG>\n")
        outputFile.write("</FRAMESET>\n")
        outputFile.close()
