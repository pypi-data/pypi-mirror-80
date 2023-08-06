from selenium.webdriver.common.by import By


class Element:
    '''
    Simple struct to store instructions to find an element on a page.

    Attributes
    ----------
    method : str
        The name of the method used to locate the element. Common values include "id", "xpath", and "css_selector" - look at `<https://selenium-python.readthedocs.io/locating-elements.html>`_ for more info. This is passed directly into the ``selenium.webdriver.common.By`` constructor.
    selector : str
        Combined with `method`, defines a way to find a specific element on the DOM. This is the actual xpath, css selector, etc., used to find the element.
    needsInstructions : Boolean
        If true, this element requires instructions in the :class:`centaurminer.MiningEngine` class to extract - used for the Complex subclass.
    '''
    def __init__(self, method, selector):
        self.needsInstructions = False
        self.attribute = None
        if isinstance(method, str):
            self.method = getattr(By, method.upper())
        else:
            self.method = method
            print(type(self.method))
        self.selector = selector

    def get_attribute(self, attributeName):
        '''
        Indicate which attribute of the element should be extracted.

        Arguments
        ---------
        attributeName : str
            Name of the attribute to be extracted.

        Returns
        -------
        Element
            Used for chaining with the contructor.
        '''
        self.attribute = attributeName
        return self


class MetaData(Element):
    '''
    A special type of Element that's derived from the metadata

    Arguments
    ---------
    name : str
        The 'name' or 'property' value of the Metadata this object points to.
    '''

    def __init__(self, name):
        super().__init__("XPATH", "html/head/meta[@name='" + name + "' or @property='" + name + "']")
        self.attribute = "content"


class Complex(Element):
    '''
    This represents an element that needs further directions to extract.

    An error will be thrown when trying to gather data, if the :class:`centaurminer.MiningEngine` doing the mining does not have an instruction for a Complex element.
    '''
    def __init__(self):
        self.needsInstructions = True


class PageLocations:
    '''
    The base class for locating article elements on a site.

    Some fields are gathered in a default way, based on standard metadata:

        * title : MetaData("citation_title")
        * authors : MetaData("citation_author")
        * doi : MetaData("citation_doi")
        * abstract : MetaData("citation_abstract")
        * date_publication : MetaData("citation_date")

    These *can* be overwritten if required. Also, see :class:`centaurminer.MiningEngine` to see how authors specifically are handled.

    To include an :class:`Element <centaurminer.Element>` for another piece of information, just subclass this class and add a static variable that stores an :class:`Element <centaurminer.Element>`.
    '''
    # High priority
    title = MetaData("citation_title")
    authors = MetaData("citation_author")
    doi = MetaData("citation_doi")
    abstract = MetaData("citation_abstract")
    # full_body = None
    # licensing = None

    # Medium priority
    date_publication = MetaData("citation_date")
    # citations = None
    # references = None
    extra_link = MetaData("citation_pdf_url")

    # Low priority
    # organization_affiliated = None
    # category = None
    # keywords: None
    # source_impact_factor = None

    # _defaults = ['title', 'authors', 'doi', 'abstract', 'date_publication', 'extra_link']

    @classmethod
    def _elements(cls):
        '''Returns the elements which have locations defined'''
        return [v for v in dir(cls) if not v.startswith('_') and not callable(v)]
