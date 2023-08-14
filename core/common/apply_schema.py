from lxml import etree
import csv

from .update_values import update_values
from .add_values import add_values
from .remove_empty_dicts import remove_empty_dicts
from .remove_empty_fields import remove_empty_fields
from .modify_element import modify_element
from .dict_to_xml import dict_to_xml
from .xml_validator import validate_xml
from .check_row import check_row

def apply_schema(schema_path, csv_path):
    
    # Load XSD schema
    etree.XMLSchema(file=schema_path)

    # Create root XML element
    stundents = etree.Element('Students')
    
    #Define schema variables
    xsd_file = schema_path
    xsd_tree = etree.parse(xsd_file)
    xsd_root = xsd_tree.getroot()
    
    #define dict variables to hold the data generated in iterators
    group_elements = {}
    initial_schema_values = {}
    
    #Exception lists for the delete methods
    field_exceptions = ["BuildingNumber", "Faculty",]
    dict_exceptions = []
    
    #define the path. these where the iterators searching for keys
    root_path = "//xs:complexType | //xs:simpleType"
    element_xpath = ".//xs:sequence/xs:element | .//xs:attribute | .//xs:all/xs:element"

    #get the required fields from the schema
    for complex_type in xsd_root.xpath(root_path, namespaces={"xs": 
        "http://www.w3.org/2001/XMLSchema"}):
        group_name = complex_type.get("name")
        schema_dict = {}
        if group_name != None:
            [schema_dict.update({element.get("name"): ""}) for element in complex_type.xpath(element_xpath, namespaces={"xs": "http://www.w3.org/2001/XMLSchema"})]
            temp_dict = {group_name: schema_dict}
            initial_schema_values.update(temp_dict)
    
    # Traverse the XSD schema to identify complex types with sequences
    for complex_type in xsd_root.xpath("//xs:element[@name='Student']/xs:complexType/xs:sequence/xs:element", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}):
        group_name = complex_type.get("name")
        schema_type = complex_type.get("type")
        group_elements[group_name] = ""
        if str(schema_type).endswith("Type"):
            if not initial_schema_values[schema_type]:
                initial_schema_values[schema_type] = ""
            group_elements[group_name] = initial_schema_values[schema_type]
    
    constructed_dict_from_schema = update_values(group_elements, initial_schema_values)
    
    # Delete inconsistent data from the constructed schema dictionary
    del constructed_dict_from_schema['Study']['Consultant']
    del constructed_dict_from_schema['Study']['Payments']
    del constructed_dict_from_schema['Study']['Mobility']
    del constructed_dict_from_schema["SpecialNeeds"]
    
    #final_dict_list will contains every generated Student data
    final_dict_list = []
    
    #open the csv file, iterate over it, and add the values to the constructed dictionary, 
    #if the cloumn name is in the dictionary.
    #Remove any empty entity, except the ones that are in the exception lists
    with open(csv_path, "r", encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            template_dd = constructed_dict_from_schema
            return_dd = add_values(template_dd, row)
            return_dd = remove_empty_fields(return_dd, field_exceptions)
            return_dd = remove_empty_dicts(return_dd, dict_exceptions)
            final_dict_list.append(add_values(return_dd, row))

        #create a new Student entity for each row in the csv
        #Check the row and alter the values to be valid for the schema
        #Append birth_number for each student's parameter
        #convert the dict to xml   
    with open(csv_path, "r", encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for index, row in enumerate(csv_reader):
            checked_row_for_zeros = check_row(row)
            altered_row = {key: modify_element(value) for key, value in checked_row_for_zeros.items()}
            student = etree.SubElement(stundents, 'Student')
            student.set('birth_number', altered_row['birth_number'])
            dict_to_xml(student, final_dict_list[index])
            
    #Create a string from the generated xml tree, decode them, and write them to the output file         
    xml_string = etree.tostring(stundents, 
                                encoding='utf-8', 
                                pretty_print=True, 
                                xml_declaration=True,)
    xml_string = xml_string.decode('utf-8')
    with open('outputs/output.xml', 'w', encoding='utf-8') as xml_file:
            xml_file.write(str(xml_string))
    
    #validate the generated file based on the given schema
    validate_xml("outputs/output.xml", schema_path )
    



        



