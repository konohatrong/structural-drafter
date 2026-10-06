
from ._dbSecSS import _SS_DBUSER,_SS_DB_SECTION
from ._offsetSS import Offset
from ._unSupp import _SS_UNSUPP,_SS_STD_DB

from ._compositeSS_Steel import _SS_COMP_STEEL_I_TYPE1,_SS_COMP_STEEL_TUB_TYPE1
from ._TapdbSecSS import _SS_TAPERED_DBUSER
from ._Tap_CompSteelSS import _SS_TAP_COMP_STEEL_TUB_TYPE1



from midas_gen import MidasAPI
from typing import Literal

_dbsection = Literal["L","C","H","T","B","P","2L","2C","SB","SR","OCT"]
_variation = Literal["LINEAR","POLY"]
_symplane = Literal["i","j"]
_Section = Literal["Section"]

class _helperSECTION:
    ID, NAME, SHAPE, TYPE, OFFSET, USESHEAR, USE7DOF = 0,0,0,0,0,0,0
    def update():
        pass
    def toJSON():
        pass


def _SectionADD(self):
    # Commom HERE ---------------------------------------------
    if self.ID==None: id = 0
    else: id = int(self.ID)
    
    
    if Section.ids == []: 
        count = 1
    else:
        count = max(Section.ids)+1

    if id==0 :
        self.ID = count
        Section.sect.append(self)
        Section.ids.append(int(self.ID))
    elif id in Section.ids:
        self.ID=int(id)
        print(f'⚠️  Section with ID {id} already exist! It will be replaced.')
        index=Section.ids.index(id)
        Section.sect[index]=self
    else:
        self.ID=id        
        Section.sect.append(self)
        Section.ids.append(int(self.ID))
    Section._dic[self.NAME] = int(self.ID)
    # Common END -------------------------------------------------------



def off_JS2Obj(js):

    try: OffsetPoint = js['OFFSET_PT']
    except: OffsetPoint='CC'
    try: CenterLocation = js['OFFSET_CENTER']
    except: CenterLocation=0
    try: HOffset = js['USERDEF_OFFSET_YI']
    except: HOffset=0
    try: HOffOpt = js['HORZ_OFFSET_OPT']
    except: HOffOpt=0
    try: VOffOpt = js['VERT_OFFSET_OPT']
    except: VOffOpt=0
    try: VOffset = js['USERDEF_OFFSET_ZI']
    except: VOffset=0
    try: UsrOffOpt = js['USER_OFFSET_REF']
    except: UsrOffOpt=0

    return Offset(OffsetPoint,CenterLocation,HOffset,HOffOpt,VOffset,VOffOpt,UsrOffOpt)



# -------------------  FUNCTION TO CREATE OBJECT used in ELEMENT SYNC  --------------------------
def _JS2OBJ(id,js):
    name = js['SECT_NAME']
    type = js['SECTTYPE']
    shape = js['SECT_BEFORE']['SHAPE']
    offset = off_JS2Obj(js['SECT_BEFORE'])
    uShear = js['SECT_BEFORE']['USE_SHEAR_DEFORM']
    u7DOF = js['SECT_BEFORE']['USE_WARPING_EFFECT']
    if type == 'DBUSER':
        if js['SECT_BEFORE']['DATATYPE'] ==2: obj = _SS_DBUSER._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        elif js['SECT_BEFORE']['DATATYPE'] ==1: obj = _SS_DB_SECTION._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        else: obj = _SS_STD_DB(id,name,type,shape,offset,uShear,u7DOF,js)

    elif type == 'PSC' :
        obj = _SS_UNSUPP(id,name,type,shape,offset,uShear,u7DOF,js)

    elif type == 'COMPOSITE':
        if shape in ['I']: obj = _SS_COMP_STEEL_I_TYPE1._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        elif shape in ['Tub']: obj = _SS_COMP_STEEL_TUB_TYPE1._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        else: obj = _SS_UNSUPP(id,name,type,shape,offset,uShear,u7DOF,js)

    elif type == 'TAPERED' :
        try:
            typeDB = js['SECT_BEFORE']['TYPE']
        except: typeDB = 0
        if typeDB == 2: 
            obj = _SS_TAPERED_DBUSER._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        elif shape == 'CP_T': obj = _SS_TAP_COMP_STEEL_TUB_TYPE1._objectify(id,name,type,shape,offset,uShear,u7DOF,js)
        else: obj = _SS_UNSUPP(id,name,type,shape,offset,uShear,u7DOF,js)

    else :
        obj = _SS_UNSUPP(id,name,type,shape,offset,uShear,u7DOF,js)


    _SectionADD(obj)





class Section:
    """Manage cross-sections in a MIDAS GEN NX model.

    ``Section`` is a static database that holds all sections defined in the
    current Python session and provides factory methods for every supported
    section type. Sections are pushed to / pulled from MIDAS GEN NX via the
    REST API using :meth:`create`, :meth:`get`, :meth:`sync`, and
    :meth:`delete`.

    Class Attributes:
        sect (list[_helperSECTION]): All section objects in the current session.
        ids (list[int]): Database IDs of all registered sections.
        _dic (dict): Mapping of section name → section ID.

    Section type hierarchy::

        Section
        ├── DBUSER(...)          — Standard shape with user dimensions
        ├── DB(...)              — Shape sourced from a codal database
        ├── Composite
        │   ├── SteelI_Type1(…)  — Composite steel I-girder (Type 1)
        │   ├── SteelTub_Type1(…)— Composite steel tub girder (Type 1)
        └── Tapered
            ├── DBUSER(...)      — Tapered standard shape
            ├── SteelTub_Type1(…)— Tapered composite steel tub
            └── bySHAPE(...)     — Tapered section built from two end sections

    Example::

        s1 = Section.DBUSER("Girder", "H", [1000, 300, 200, 300, 20, 20, 15])
        s2 = Section.DB("HEA300", "H", "EN", "HEA300")
        Section.create()   # push all sections to MIDAS
    """
    sect: list[_helperSECTION] = []
    ids: list[int] = []
    _dic = {}

    @classmethod
    def json(cls):
        """Serialise all registered sections to the MIDAS API JSON format.

        Returns:
            dict: ``{"Assign": {id: section_json, ...}}`` ready for the
            ``/db/SECT`` endpoint.
        """
        json = {"Assign":{}}
        for sect in cls.sect:
            js = sect.toJSON()
            json["Assign"][str(sect.ID)] = js
        return json

    @staticmethod
    def create():
        """Push all registered sections to MIDAS GEN NX (PUT /db/SECT)."""
        MidasAPI("PUT","/db/SECT",Section.json())

    @staticmethod
    def get():
        """Retrieve all sections from MIDAS GEN NX (GET /db/SECT).

        Returns:
            dict: Raw API response containing the ``'SECT'`` dictionary.
        """
        return MidasAPI("GET","/db/SECT")

    @staticmethod
    def delete():
        """Delete all sections from MIDAS GEN NX and clear the local database."""
        MidasAPI("DELETE","/db/SECT")
        Section.clear()

    @staticmethod
    def clear():
        """Clear the local section database without affecting the MIDAS model."""
        Section.sect=[]
        Section.ids=[]

    @staticmethod
    def sync(bDBSectParams: bool = False, bSectionProperty: bool = False):
        """Pull sections from MIDAS GEN NX and rebuild the local database.

        Fetches all sections via the API and reconstructs the corresponding
        Python objects. Optionally retrieves additional section data.

        Args:
            bDBSectParams (bool): If ``True``, also fetch raw dimension
                parameters for ``DBUSER`` (database) sections from the
                ``SECTIONDB/USER`` result table and attach them as a
                ``PARAMS`` attribute on each matching section object.
            bSectionProperty (bool): If ``True``, also fetch computed section
                properties (area, shear areas, moments of inertia) from the
                ``SECTIONALL`` result table and attach them as ``AREA``,
                ``ASY``, ``ASZ``, ``IXX``, ``IYY``, ``IZZ`` attributes.
        """
        a = Section.get()
        if a != {'message': ''}:
            Section.sect = []
            Section.ids=[]
            for sect_id in a['SECT'].keys():
                _JS2OBJ(sect_id,a['SECT'][sect_id])
        
        if bDBSectParams:
            jsRes = {
                "Argument": {
                    "TABLE_NAME": "SS_Table",
                    "TABLE_TYPE": "SECTIONDB/USER"
                }
            }
        
            dicParams = {}
            resp = MidasAPI('POST','/post/TABLE',jsRes)
            for q in resp['SS_Table']['DATA']:
                dicParams[q[1]] = [float(q[11+j]) for j in range(10)]
        
            for sec in Section.sect:
                if sec.TYPE=='DBUSER':
                    if sec.DATATYPE==1:
                        sec.PARAMS = dicParams[str(sec.ID)]     # Add additional PARAMS property to DB Section
                        # Section.DBUSER(f"{sec.NAME}_DB2User",sec.SHAPE,dicParams[str(sec.ID)],sec.OFFSET,sec.USESHEAR,sec.USE7DOF,sec.ID)
        
        if bSectionProperty:
            jsRes = {
                "Argument": {
                    "TABLE_NAME": "SS_Table",
                    "TABLE_TYPE": "SECTIONALL"
                }
            }
            dicParams = {}
            resp = MidasAPI('POST','/post/TABLE',jsRes)
            for q in resp['SS_Table']['DATA']:
                dicParams[q[1]] = [float(q[5+j]) for j in range(6)]
            for sec in Section.sect:
                sec.AREA, sec.ASY ,sec.ASZ ,sec.IXX ,sec.IYY ,sec.IZZ , = dicParams[str(sec.ID)]



#---------------------------------     S E C T I O N S    ---------------------------------------------

    #---------------------     D B   U S E R    --------------------
    @staticmethod
    def DBUSER(Name:str='',Shape:_dbsection='',parameters:list=[],Offset=Offset(),useShear:bool=True,use7Dof:bool=False,id:int=None):
        """Create a standard section with user-defined dimensions.

        The section shape is one of the built-in database shapes, but the
        dimensions are provided directly rather than looked up from a codal
        database. Both I- and J-end parameters are identical (prismatic).

        Args:
            Name (str): Section name.
            Shape (_dbsection): Shape code — one of ``'L'``, ``'C'``, ``'H'``,
                ``'T'``, ``'B'``, ``'P'``, ``'2L'``, ``'2C'``, ``'SB'``,
                ``'SR'``, ``'OCT'``.
            parameters (list[float]): Section dimensions. Order depends on the
                chosen shape (see MIDAS GEN NX section definition).
            Offset (Offset): Cross-section offset. Defaults to centroid (CC).
            useShear (bool): Include shear deformation. Default ``True``.
            use7Dof (bool): Include warping (7th DOF) effect. Default ``False``.
            id (int | None): Section database ID. Auto-assigned when ``None``.

        Returns:
            _SS_DBUSER: The created section object.

        Example::

            Section.DBUSER("MainGirder", "H", [1000, 300, 200, 300, 20, 20, 15, 0])
        """
        args = locals()
        sect_Obj = _SS_DBUSER(**args)
        _SectionADD(sect_Obj)
        return sect_Obj
    
    @staticmethod
    def DB(Name:str='',Shape:_dbsection='',DB_Name:str='',Sect_Name:str='',Offset=Offset(),useShear:bool=True,use7Dof:bool=False,id:int=None):
        """Create a section sourced from a codal steel/section database.

        Dimensions are looked up by MIDAS from the specified database entry
        rather than entered manually.

        Args:
            Name (str): Section name used within the model.
            Shape (_dbsection): Shape code (e.g. ``'H'``, ``'L'``, ``'C'``).
            DB_Name (str): Name of the codal database (e.g. ``'EN'``, ``'AISC'``).
            Sect_Name (str): Name of the section within the database
                (e.g. ``'HEA300'``, ``'W14X22'``).
            Offset (Offset): Cross-section offset. Defaults to centroid (CC).
            useShear (bool): Include shear deformation. Default ``True``.
            use7Dof (bool): Include warping (7th DOF) effect. Default ``False``.
            id (int | None): Section database ID. Auto-assigned when ``None``.

        Returns:
            _SS_DB_SECTION: The created section object.

        Example::

            Section.DB("Column", "H", "EN", "HEA300")
        """
        args = locals()
        sect_Obj = _SS_DB_SECTION(**args)
        _SectionADD(sect_Obj)
        return sect_Obj
    
    class Composite:
        """Factory methods for composite sections (steel or PSC girder + concrete slab)."""

        @staticmethod
        def SteelI_Type1(Name='', Bc=0, tc=0, Hh=0, Hw=0, B1=0, tf1=0, tw=0, B2=0, tf2=0,
                EsEc=0, DsDc=0, Ps=0, Pc=0, TsTc=0,
                MultiModulus=False, CreepEratio=0, ShrinkEratio=0,
                Offset: Offset = Offset.CC(), useShear: bool = True, use7Dof: bool = False, id: int = None):
            """Create a composite steel I-girder section, Type 1 (symmetric I + slab).

            Args:
                Name (str): Section name.
                Bc (float): Effective slab width.
                tc (float): Slab thickness.
                Hh (float): Haunch height.
                Hw (float): Steel web height.
                B1 (float): Top flange width.
                tf1 (float): Top flange thickness.
                tw (float): Web thickness.
                B2 (float): Bottom flange width.
                tf2 (float): Bottom flange thickness.
                EsEc (float): Modular ratio steel / concrete (E_s / E_c).
                DsDc (float): Unit weight ratio steel / concrete.
                Ps (float): Steel Poisson's ratio.
                Pc (float): Concrete Poisson's ratio.
                TsTc (float): Thermal expansion ratio.
                MultiModulus (bool): Use multi-modulus method.
                CreepEratio (float): Creep modular ratio.
                ShrinkEratio (float): Shrinkage modular ratio.
                Offset (Offset): Cross-section offset. Defaults to centroid (CC).
                useShear (bool): Include shear deformation. Default ``True``.
                use7Dof (bool): Include warping effect. Default ``False``.
                id (int | None): Section ID. Auto-assigned when ``None``.

            Returns:
                _SS_COMP_STEEL_I_TYPE1: The created section object.
            """
            args = locals()
            sect_Obj = _SS_COMP_STEEL_I_TYPE1(**args)
            _SectionADD(sect_Obj)
            return sect_Obj

        @staticmethod
        def SteelTub_Type1(Name='',
                Bc=0, tc=0, Hh=0,
                Hw=0, B1=0, Bf1=0, tf1=0, Bf3=0,
                tw=0, B2=0, Bf2=0, tf2=0, tfp=0,
                EsEc=0, DsDc=0, Ps=0, Pc=0, TsTc=0,
                MultiModulus=False, CreepEratio=0, ShrinkEratio=0,
                Offset: Offset = Offset.CC(), useShear: bool = True, use7Dof: bool = False, id: int = None):
            """Create a composite steel tub (U-girder) section, Type 1.

            Args:
                Name (str): Section name.
                Bc (float): Effective slab width.
                tc (float): Slab thickness.
                Hh (float): Haunch height.
                Hw (float): Web height.
                B1 (float): Top flange width (left).
                Bf1 (float): Top flange overhang (left).
                tf1 (float): Top flange thickness.
                Bf3 (float): Top flange inner width.
                tw (float): Web thickness.
                B2 (float): Bottom flange width.
                Bf2 (float): Bottom flange overhang.
                tf2 (float): Bottom flange thickness.
                tfp (float): Top plate thickness.
                EsEc (float): Modular ratio steel / concrete.
                DsDc (float): Unit weight ratio steel / concrete.
                Ps (float): Steel Poisson's ratio.
                Pc (float): Concrete Poisson's ratio.
                TsTc (float): Thermal expansion ratio.
                MultiModulus (bool): Use multi-modulus method.
                CreepEratio (float): Creep modular ratio.
                ShrinkEratio (float): Shrinkage modular ratio.
                Offset (Offset): Cross-section offset. Defaults to centroid (CC).
                useShear (bool): Include shear deformation. Default ``True``.
                use7Dof (bool): Include warping effect. Default ``False``.
                id (int | None): Section ID. Auto-assigned when ``None``.

            Returns:
                _SS_COMP_STEEL_TUB_TYPE1: The created section object.
            """
            args = locals()
            sect_Obj = _SS_COMP_STEEL_TUB_TYPE1(**args)
            _SectionADD(sect_Obj)
            return sect_Obj

    
    class Tapered:
        """Factory methods for tapered sections whose shape varies from I-end to J-end."""

        @staticmethod
        def DBUSER(Name: str = '', Shape: _dbsection = '', params_I: list = [], params_J: list = [],
                   Offset=Offset(), useShear: bool = True, use7Dof: bool = False, id: int = None):
            """Create a tapered standard section with user-defined I/J-end dimensions.

            Args:
                Name (str): Section name.
                Shape (_dbsection): Shape code — one of ``'L'``, ``'C'``, ``'H'``,
                    ``'T'``, ``'B'``, ``'P'``, ``'SB'``, etc.
                params_I (list[float]): Dimensions at the I-end (start of element).
                params_J (list[float]): Dimensions at the J-end (end of element).
                Offset (Offset): Cross-section offset. Defaults to centroid (CC).
                useShear (bool): Include shear deformation. Default ``True``.
                use7Dof (bool): Include warping effect. Default ``False``.
                id (int | None): Section ID. Auto-assigned when ``None``.

            Returns:
                _SS_TAPERED_DBUSER: The created section object.
            """
            args = locals()
            sect_Obj = _SS_TAPERED_DBUSER(**args)
            _SectionADD(sect_Obj)
            return sect_Obj

        @staticmethod
        def SteelTub_Type1(Name='',
                Bc=0, tc=0, Hh=0,
                params_I=[0,0,0,0,0,0,0,0,0,0],
                params_J=[0,0,0,0,0,0,0,0,0,0],
                EsEc=0, DsDc=0, Ps=0, Pc=0, TsTc=0,
                MultiModulus=False, CreepEratio=0, ShrinkEratio=0,
                Offset: Offset = Offset.CC(), useShear: bool = True, use7Dof: bool = False, id: int = None):
            """Create a tapered composite steel tub (U-girder) section, Type 1.

            The steel tub geometry varies from I-end to J-end via 10-element
            parameter lists (``params_I`` / ``params_J``); the concrete slab
            dimensions are constant along the element.

            Args:
                Name (str): Section name.
                Bc (float): Effective slab width (constant along element).
                tc (float): Slab thickness.
                Hh (float): Haunch height.
                params_I (list[float]): 10 steel tub dimension values at I-end
                    ``[Hw, B1, Bf1, tf1, Bf3, tw, B2, Bf2, tf2, tfp]``.
                params_J (list[float]): 10 steel tub dimension values at J-end
                    (same order as ``params_I``).
                EsEc (float): Modular ratio steel / concrete.
                DsDc (float): Unit weight ratio steel / concrete.
                Ps (float): Steel Poisson's ratio.
                Pc (float): Concrete Poisson's ratio.
                TsTc (float): Thermal expansion ratio.
                MultiModulus (bool): Use multi-modulus method.
                CreepEratio (float): Creep modular ratio.
                ShrinkEratio (float): Shrinkage modular ratio.
                Offset (Offset): Cross-section offset. Defaults to centroid (CC).
                useShear (bool): Include shear deformation. Default ``True``.
                use7Dof (bool): Include warping effect. Default ``False``.
                id (int | None): Section ID. Auto-assigned when ``None``.

            Returns:
                _SS_TAP_COMP_STEEL_TUB_TYPE1: The created section object.
            """
            args = locals()
            sect_Obj = _SS_TAP_COMP_STEEL_TUB_TYPE1(**args)
            _SectionADD(sect_Obj)
            return sect_Obj

        @staticmethod
        def bySHAPE(Name: str, Sect_I: _Section, Sect_J: _Section,
                    Offset=Offset(), useShear: bool = True, use7Dof: bool = False, id: int = None):
            """Create a tapered section by combining two existing prismatic end sections.

            Inspects the types of ``Sect_I`` and ``Sect_J`` and constructs the
            appropriate tapered section object automatically. Both sections must
            be the same type and, for ``DBUSER`` sections, the same shape code.

            Supported end-section types:
                - ``_SS_DBUSER`` → ``_SS_TAPERED_DBUSER``
                - ``_SS_PSC_12CELL`` → ``_SS_TAP_PSC_12CELL``
                - ``_SS_PSC_Value`` → ``_SS_TAP_PSC_Value``

            Args:
                Name (str): Name for the new tapered section.
                Sect_I: Prismatic section object at the I-end.
                Sect_J: Prismatic section object at the J-end (must match type
                    and shape of ``Sect_I``).
                Offset (Offset): Cross-section offset. Defaults to centroid (CC).
                useShear (bool): Include shear deformation. Default ``True``.
                use7Dof (bool): Include warping effect. Default ``False``.
                id (int | None): Section ID. Auto-assigned when ``None``.

            Returns:
                Tapered section object, or ``False`` if the end sections are
                incompatible.

            Example::

                s_i = Section.DBUSER("EndI", "H", [900, 300, 200, 300, 20, 20, 12, 0])
                s_j = Section.DBUSER("EndJ", "H", [600, 300, 200, 300, 16, 16, 10, 0])
                Section.Tapered.bySHAPE("TapGirder", s_i, s_j)
            """
            if not isinstance(Sect_I, type(Sect_J)):
                print(f"  ⚠️   Section of I and J end does not match for '{Name}' section")
                return False

            if isinstance(Sect_I,_SS_DBUSER):
                if Sect_I.SHAPE == Sect_J.SHAPE:
                    sect_Obj = _SS_TAPERED_DBUSER(Name,Sect_I.SHAPE,Sect_I.PARAMS,Sect_J.PARAMS,Offset,useShear,use7Dof,id)
                else:
                    print(f"  ⚠️   Section of I and J end does not match for '{Name}' section")
                    return False

            _SectionADD(sect_Obj)
            return sect_Obj

        

#---------------------------------     T A P E R E D   G R O U P    ---------------------------------------------
    class TaperedGroup:
        """database and API wrapper for MIDAS GEN NX Tapered Section Groups (TSGR).

        A Tapered Group assigns a variation law (linear or polynomial) to the
        cross-section change along a set of elements that share a tapered
        section. MIDAS requires this grouping to interpolate section properties
        correctly during analysis.

        Class Attributes:
            data (list): All ``TaperedGroup`` instances in the current session.

        Example::

            Section.TaperedGroup("LinGrp", [1, 2, 3], "LINEAR", "LINEAR")
            Section.TaperedGroup("PolyGrp", [4, 5], "POLY", "LINEAR", z_exp=2.5)
            Section.TaperedGroup.create()
        """

        data = []
        
        def __init__(self, name, elem_list:list, z_var:_variation="LINEAR", y_var:_variation="LINEAR", z_exp:float=2.0, z_from:_symplane="i", z_dist:float=0, 
                     y_exp:float=2.0, y_from:_symplane="i", y_dist:float=0, id:int=None):
            """
            Args:
                name (str): Tapered Group Name (Required).
                elem_list (list): List of element numbers (Required).
                z_var (str): Section shape variation for Z-axis: "LINEAR" or "POLY" (Required).
                y_var (str): Section shape variation for Y-axis: "LINEAR" or "POLY" (Required).
                z_exp (float, optional): Z-axis exponent. Required if z_var is "POLY".
                z_from (str, optional): Z-axis symmetric plane ("i" or "j"). Defaults to "i" for "POLY".
                z_dist (float, optional): Z-axis symmetric plane distance. Defaults to 0 for "POLY".
                y_exp (float, optional): Y-axis exponent. Required if y_var is "POLY".
                y_from (str, optional): Y-axis symmetric plane ("i" or "j"). Defaults to "i" for "POLY".
                y_dist (float, optional): Y-axis symmetric plane distance. Defaults to 0 for "POLY".
                id (str, optional): ID for the tapered group. Auto-generated if not provided.
            
            Example:
                Section.TapperGroup("Linear", [1, 2, 3], "LINEAR", "LINEAR")
                Section.TapperGroup("ZPoly", [4, 5], "POLY", "LINEAR", z_exp=2.5)
            """
            self.NAME = name
            self.ELEM_LIST = elem_list
            self.Z_VAR = z_var
            self.Y_VAR = y_var
            self.Z_FROM = z_from
            self.Y_FROM = y_from
            self.Z_DIST = z_dist
            self.Y_DIST = y_dist
            
            # Z-axis parameters (only for POLY)
            if z_var == "POLY":
                if z_exp is None:
                    raise ValueError("z_exp is required when z_var is 'POLY'")
                self.Z_EXP = z_exp
            else:
                self.Z_EXP = None
                self.Z_DIST = None
            
            # Y-axis parameters (only for POLY)
            if y_var == "POLY":
                if y_exp is None:
                    raise ValueError("y_exp is required when y_var is 'POLY'")
                self.Y_EXP = y_exp
            else:
                self.Y_EXP = None
                self.Y_DIST = None
            
            if id == None:
                id = len(Section.TaperedGroup.data) + 1
            self.ID = id
            
            Section.TaperedGroup.data.append(self)
        
        @classmethod
        def json(cls):
            """Serialise all tapered groups to the MIDAS API JSON format.

            Returns:
                dict: ``{"Assign": {id: group_data, ...}}`` ready for the
                ``/db/tsgr`` endpoint. Polynomial-only fields (``ZEXP``,
                ``ZDIST``, ``YEXP``, ``YDIST``) are omitted for linear groups.
            """
            json_data = {"Assign": {}}
            for i in cls.data:
                # Base data that's always included
                tapper_data = {
                    "NAME": i.NAME,
                    "ELEMLIST": i.ELEM_LIST,
                    "ZVAR": i.Z_VAR,
                    "YVAR": i.Y_VAR,
                    "ZFROM" : i.Z_FROM,
                    "YFROM" : i.Y_FROM
                }
                
                # Add Z-axis polynomial parameters only if Z_VAR is "POLY"
                if i.Z_VAR == "POLY":
                    tapper_data["ZEXP"] = i.Z_EXP
                    tapper_data["ZDIST"] = i.Z_DIST
                
                # Add Y-axis polynomial parameters only if Y_VAR is "POLY"
                if i.Y_VAR == "POLY":
                    tapper_data["YEXP"] = i.Y_EXP
                    tapper_data["YDIST"] = i.Y_DIST
                
                json_data["Assign"][str(i.ID)] = tapper_data
            
            return json_data
        
        @classmethod
        def create(cls):
            """Push all tapered groups to MIDAS GEN NX (PUT /db/tsgr)."""
            MidasAPI("PUT", "/db/tsgr", cls.json())

        @classmethod
        def autoGenerate(cls):
            """Auto-create one tapered group per tapered section based on element assignments.

            Iterates over all sections in ``Section.sect`` that have
            ``TYPE == 'TAPERED'``, finds every element referencing each
            tapered section from ``Element.elements``, and creates a
            ``TaperedGroup`` named ``TG_SecID{id}`` for each. The local
            database is cleared before generation.

            Note:
                Uses linear variation (default) for all generated groups. Call
                individual ``TaperedGroup`` constructors manually to set
                polynomial variation.
            """
            from midas_gen import Element
            _tapSectElems = {}
            _tapSectIDs = []
            cls.clear()
            #GET TAPERED SECTION IDS
            for sec in Section.sect:
                if sec.TYPE == 'TAPERED':
                    _tapSectElems[sec.ID] = []
                    _tapSectIDs.append(sec.ID)
            
            #GET ELEMS WITH TAPERED SECTIONS
            for elm in Element.elements:
                if elm.SECT in _tapSectIDs:
                    _tapSectElems[elm.SECT].append(elm.ID)

            #GENERATE TAPERED GROUP
            for sectID in _tapSectIDs:
                Section.TaperedGroup(f"TG_SecID{sectID}",_tapSectElems[sectID])

        
        @classmethod
        def get(cls):
            """Retrieve all tapered groups from MIDAS GEN NX (GET /db/tsgr).

            Returns:
                dict: Raw API response containing the ``'TSGR'`` dictionary.
            """
            return MidasAPI("GET", "/db/tsgr")

        @classmethod
        def delete(cls):
            """Delete all tapered groups from MIDAS GEN NX and clear the local database."""
            cls.clear()
            return MidasAPI("DELETE", "/db/tsgr")

        @classmethod
        def clear(cls):
            """Clear the local tapered group database without affecting the MIDAS model."""
            cls.data = []

        @classmethod
        def sync(cls):
            """Pull tapered groups from MIDAS GEN NX and rebuild the local database.

            Fetches all tapered groups via the API and reconstructs the
            corresponding ``TaperedGroup`` objects. The local database is
            cleared before repopulating.
            """
            cls.data = []
            response = cls.get()
            
            if response and response != {'message': ''}:
                tsgr_data = response.get('TSGR', {})
                # Iterate through the dictionary of tapered groups from the API response
                for tsgr_id, item_data in tsgr_data.items():
                    # Extract base parameters
                    name = item_data.get('NAME')
                    elem_list = item_data.get('ELEMLIST')
                    z_var = item_data.get('ZVAR')
                    y_var = item_data.get('YVAR')
                    
                    # Extract optional parameters based on variation type
                    z_exp = item_data.get('ZEXP') if z_var == "POLY" else None
                    z_from = item_data.get('ZFROM') if z_var == "POLY" else None
                    z_dist = item_data.get('ZDIST') if z_var == "POLY" else None
                    
                    y_exp = item_data.get('YEXP') if y_var == "POLY" else None
                    y_from = item_data.get('YFROM') if y_var == "POLY" else None
                    y_dist = item_data.get('YDIST') if y_var == "POLY" else None
                    
                    Section.TaperedGroup(
                        name=name,
                        elem_list=elem_list,
                        z_var=z_var,
                        y_var=y_var,
                        z_exp=z_exp,
                        z_from=z_from,
                        z_dist=z_dist,
                        y_exp=y_exp,
                        y_from=y_from,
                        y_dist=y_dist,
                        id=tsgr_id
                    )