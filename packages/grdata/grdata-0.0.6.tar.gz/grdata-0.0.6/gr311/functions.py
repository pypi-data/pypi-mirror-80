import pyodbc
import pandas as pd
import base64

def get_scripts(start, end, user, password):
    ### GET 311 DATA
    crmcnxn = pyodbc.connect(
        r'driver={SQL Server};'
        r'server=dbi204\crm2015;'
        r'database=CRM2015PROD_MSCRM;'
        r'UID=' + user + ';'
        r'PWD=' + password)
    crmsql = "Select Incident.Incidentid as [Interaction ID], dateadd(HH,-4,Incident.CreatedOn) as [Date and Time] , \"pt_articletracker1\".pt_ArticleIdName as [Script Used], \"Ccon\".Address1_Line1 + ', ' + \"Ccon\".Address1_City + ', ' + \"Ccon\".Address1_StateOrProvince + ', ' + \"Ccon\".Address1_PostalCode as Address, ward.new_Ward as \"Ward\", Neighborhood.new_Neighborhood as \"Neighborhood\" from Incident as Incident left outer join pt_articletracker as \"pt_articletracker1\" on (Incident.IncidentId  =  \"pt_articletracker1\".pt_Case and ((((\"pt_articletracker1\".pt_articletrackerId is not null))))) left outer join Contact as Ccon on (Incident.CustomerId  =  Ccon.ContactId) left outer join Contact as ward on (Incident.CustomerId  =  ward.ContactId) left outer join Contact as Neighborhood on (Incident.CustomerId  =  Neighborhood.ContactId) where Incident.CreatedOn >= '" + str(start) + "' AND Incident.CreatedOn <= '" + str(end) + "' order by Incident.createdon, Incident.IncidentId desc"

    data_311 = pd.read_sql(crmsql, crmcnxn)

    ### DATA TRANSFORMS
    ## INTERACTION ID
    # Build Unique ID from Interaction ID + Script Used Encoded
    data_311['Unique ID'] = data_311['Interaction ID']
    for column in data_311.columns:
        data_311['Unique ID'] = data_311['Unique ID'] + '-' + data_311[column].apply(
            lambda x: str(base64.b16encode(str(x).encode()).decode())[len(str(x)) - 10: len(str(x))])

    ## TYPE
    data_311['Type'] = None
    data_311.loc[data_311['Script Used'].str.contains('WALK UP', na=False), 'Type'] = 'WALK UP'
    data_311.loc[data_311['Script Used'].str.contains('EMAIL', na=False), 'Type'] = 'EMAIL'
    data_311.loc[~(data_311['Script Used'].str.contains('WALK UP', na=False)) & ~(data_311['Script Used'].str.contains('EMAIL', na=False)), 'Type'] = 'PHONE'

    ## DATE AND TIME
    data_311['Date and Time'] = pd.to_datetime(data_311['Date and Time'])

    ## SCRIPT USED
    data_311['Script Used'] = data_311['Script Used'].str.replace('–', '-')
    data_311['Script Used'] = data_311['Script Used'].str.replace('\s+', ' ')

    ## DEPARTMENT
    data_311['Department'] = data_311['Script Used'].str.split('-')
    data_311['Department'] = data_311['Department'].str[0]
    data_311['Department'] = data_311['Department'].str.upper()
    data_311['Department'] = data_311['Department'].str.strip()

    ## ADDRESS
    # Remove Poorly Formed Addresses
    data_311['Coordinates'] = data_311['Address']
    data_311.loc[~data_311['Address'].str.contains(r'\d{1,4}(\s*\w+){1,5}', na=False) | data_311['Address'].isna(), 'Coordinates'] = None
    data_311.loc[data_311['Coordinates'].str.contains('^n(/*)a', case=False, na=False), 'Coordinates'] = None

    # Reformat Cardinal Directions When Necessary
    data_311['Coordinates'] = data_311['Coordinates'].str.replace('\s+CT\s+', ' ')
    data_311['Coordinates'] = data_311['Coordinates'].str.replace('\s+[Aa]{1}[Pp]{1}[Tt]{1}\s*#\d+', '')
    data_311['Coordinates'] = data_311['Coordinates'].str.replace('\s+#\d+', '')
    data_311['Coordinates'] = data_311['Coordinates'].str.replace(',.*?,\s*[A-Za-z0-9]{2,8}.*', '')

    return data_311


def get_incidents(start, end, user, password):
    crmcnxn = pyodbc.connect(
        r'driver={SQL Server};'
        r'server=dbi204\crm2015;'
        r'database=CRM2015PROD_MSCRM;'
        r'UID=' + user + ';'
        r'PWD=' + password)

    crmsql = """
    SELECT TOP 1000
        DATEADD(HH, -4, Incident.CreatedOn) AS [CreatedOn_EDT], 
        Incident.Incidentid,
        Incident.OwnerIdName, 
        "pt_articletracker1".pt_ArticleIdName AS [Article Name], 
        Ccon.Address1_Line1 AS Address, 
        "Ccon".Address1_Line1 + ', ' + "Ccon".Address1_City + ', ' + "Ccon".Address1_StateOrProvince + ', ' + "Ccon".Address1_PostalCode AS Location, 
        ward.new_Ward AS "Ward", 
        Neighborhood.new_Neighborhood AS "Neighborhood", 
        LEFT((replace("pt_articletracker1".pt_ArticleIdName, '–', '-')) + '-', CHARINDEX('-', (replace("pt_articletracker1".pt_ArticleIdName, '–', '-')) + '-') - 1) OldMethod,
            isnull((select Title from SubjectBase where subjectid = (select Sub.ParentSubject from SubjectBase sub where sub.SubjectId = KB.SubjectId)), (select Sub.Title from SubjectBase sub where sub.SubjectId = KB.SubjectId)) NewMethod
    FROM
        Incident AS Incident
        JOIN Contact AS Contact ON(Incident.CustomerId = Contact.ContactId
             AND (((((Contact.ContactId != 'BB36F26D-0EB8-E211-8987-005056A20014'
                      OR Contact.ContactId IS NULL)
                      AND Contact.new_Neighborhood IS NOT NULL)))))
        LEFT OUTER JOIN pt_articletracker AS "pt_articletracker1" ON(Incident.IncidentId = "pt_articletracker1".pt_Case
                                                                     AND (((("pt_articletracker1".pt_articletrackerId IS NOT NULL)))))
        LEFT OUTER JOIN Contact AS Ccon ON(Incident.CustomerId = Ccon.ContactId)
        LEFT OUTER JOIN Contact AS ward ON(Incident.CustomerId = ward.ContactId)
        LEFT OUTER JOIN Contact AS Neighborhood ON(Incident.CustomerId = Neighborhood.ContactId)
        Inner join KbArticleBase KB on "pt_articletracker1".pt_ArticleId = KB.KbArticleId
    WHERE
        Incident.CreatedOn >= '2014-01-01 00:00:00'
    ORDER BY
        Incident.createdon, 
        Incident.IncidentId ASC;
    """

    departments = pd.read_sql(crmsql, crmcnxn)


def rename_depts(departments):

    dept_dict = {'AFRICAN AMERICAN ART & MUSIC FESTIVAL': 'EXECUTIVE OFFICE',
                 'ATTORNEY': 'CITY ATTORNEY',
                 'CANCEL REFUSE SERVICE': 'PUBLIC SERVICES',
                 'CLERK': 'CITY CLERK',
                 'CLERKS': 'CITY CLERK',
                 'COMMUNITY DEVELOPEMENT': 'COMMUNITY DEVELOPMENT',
                 'COMMUNITY ENGAGEMENT': 'ENGINEERING',
                 'CUSTOMER SREVICE': 'CUSTOMER SERVICE & INNOVATION',
                 'CUSTOMER SERVICES': 'CUSTOMER SERVICE & INNOVATION',
                 'DELETE DUPLICATE SCRIPT 2/16/16 ENGINEERING': 'ENGINEERING',
                 'DIVERSITY AND INCLUSION': 'DIVERSITY & INCLUSION',
                 'DOWNTOWN GRAND RAPIDS INC': 'DOWNTOWN GRAND RAPIDS, INC.',
                 'DOWNTOWN GRAND RAPIDS INC.': 'DOWNTOWN GRAND RAPIDS, INC.',
                 'DOWNTOWN GRAND RAPIDS, INC': 'DOWNTOWN GRAND RAPIDS, INC.',
                 'ECONOMIC DEVLOPMENT': 'ECONOMIC DEVELOPMENT',
                 'ELECTION DAY': 'CITY CLERK',
                 'ENGINEERS': 'ENGINEERING',
                 'ESD': 'ENVIRONMENTAL SERVICES',
                 'ESD AQ': 'ENVIRONMENTAL SERVICES',
                 'ESD IPP': 'ENVIRONMENTAL SERVICES',
                 'ESD LAB': 'ENVIRONMENTAL SERVICES',
                 'FACILITIES MANAGEMENT': 'FACILITIES AND FLEET MANAGEMENT',
                 'FACILITIES MANGAGEMENT': 'FACILITIES AND FLEET MANAGEMENT',
                 'FIRE': 'FIRE DEPARTMENT',
                 'FLEET MANAGEMENT': 'FACILITIES AND FLEET MANAGEMENT',
                 'HR BENEFITS': 'HUMAN RESOURCES',
                 'HR LABOR REALTIONS': 'HUMAN RESOURCES',
                 'HR LABOR RELATIONS': 'HUMAN RESOURCES',
                 'HR LABOR RELATIONS EMPLOYEE PARKING TICKET VOID REQUEST': 'HUMAN RESOURCES',
                 'LIQUOR LICENSE': 'CITY CLERK',
                 'MICRO LOCAL BUSINESS': 'DIVERSITY & INCLUSION',
                 'MOBILE GR AND PARKING SERVICES': 'MOBILE GR & PARKING SERVICES',
                 'OFFICE OF ENERGY AND SUSTAINABILITY': 'SUSTAINABILITY',
                 'OUR COMMUNITY\'S CHILDREN (NOTE: THIS MAY BE PART OF A CITY DEPARTMENT)': 'OUR COMMUNITY\'S CHILDREN',
                 'PARKS': 'PARKS & RECREATION',
                 'PARKS AND RECREATION': 'PARKS & RECREATION',
                 'PARKS & RECERATION': 'PARKS & RECREATION',
                 'PARKS & RECEATION': 'PARKS & RECREATION',
                 'PARKS SIGN DESIGN COMPETITION': 'PARKS & RECREATION',
                 'PARKING SERIVCES': 'MOBILE GR & PARKING SERVICES',
                 'PARKING SERVICES': 'MOBILE GR & PARKING SERVICES',
                 'PLANNING DEPARTMENT': 'PLANNING',
                 'POLICE': 'POLICE DEPARTMENT',
                 'POLICE NON': 'POLICE DEPARTMENT',
                 'PUBLIC SERVICE': 'PUBLIC SERVICES',
                 'PUBLIC SERVICES STREETS AND SANITATION': 'PUBLIC SERVICES',
                 'REFUSE CART PAYMENT': 'PUBLIC SERVICES',
                 'REFUSE SCHEDULE': 'PUBLIC SERVICES',
                 'RETIREMENT SYSTEM': 'HUMAN RESOURCES',
                 'RETIREMENT SYSTEMS': 'HUMAN RESOURCES',
                 'RISK MANAGEMENT': 'HUMAN RESOURCES',
                 'SMALL BUSINESS AND TECHNOLOGY DEVELOPMENT CENTER': 'OTHER OUTSIDE AGENCIES',
                 'STREET LIGHTING': 'ELC',
                 'STREETS & SANITATION': 'PUBLIC SERVICES',
                 'SUSTAINABILITY': 'EXECUTIVE OFFICE',
                 'TRAFFIC SAFETY': 'MOBILE GR & PARKING SERVICES',
                 'TRAFFIC TICKETS OR FINES': 'CITY TREASURER',
                 'TREASURER': 'CITY TREASURER',
                 'TREASURERS': 'CITY TREASURER',
                 'WATER': 'WATER SYSTEM',
                 'WHAT IS A LUDS PERMIT?': 'DEVELOPMENT CENTER'
                 }

    ## DEPARTMENTS
    # Dictionary to Replace Redundant department Names
    departments = departments.replace(dept_dict)

    return departments


def label_depts(dataframe):

    dataframe = dataframe.rename(columns={'department': 'Department',
                                          'script_used': 'Script Used'})

    dept_list = ['ASSESSOR',
                 'CITY ATTORNEY',
                 'CITY CLERK',
                 'CITY TREASURER',
                 'CODE COMPLIANCE',
                 'COMMUNITY DEVELOPMENT',
                 'COMPTROLLER',
                 'DEVELOPMENT CENTER',
                 'ECONOMIC DEVELOPMENT',
                 'ELC',
                 'ENGINEERING',
                 'ENVIRONMENTAL SERVICES',
                 'EXECUTIVE OFFICE',
                 'FACILITIES AND FLEET MANAGEMENT',
                 'FIRE DEPARTMENT',
                 'FISCAL SERVICES',
                 'FORESTRY',
                 'HUMAN RESOURCES',
                 'INCOME TAX',
                 'INFORMATION TECHNOLOGY',
                 'MOBILE GR & PARKING SERVICES',
                 'PARKS & RECREATION',
                 'PLANNING',
                 'POLICE DEPARTMENT',
                 'PUBLIC SERVICES',
                 'PURCHASING',
                 'RETIREMENT SYSTEM',
                 'RISK MANAGEMENT',
                 'STREET LIGHTING',
                 'STREETS & SANITATION',
                 'TRAFFIC SAFETY',
                 'WATER SYSTEM']

    forestry_scripts = ['PARKS & RECREATION - Branch/Brush Removal',
                        'PARKS & RECREATION - Tree Trimming',
                        'PARKS & RECREATION - Tree Removal Requests',
                        'PARKS & RECREATION - Cityworks Request Update & Service Request Timeframes',
                        'PARKS & RECREATION - Fallen Tree, Tree Down',
                        'PARKS & RECREATION - Tree Planting or Opt Out',
                        'PARKS & RECREATION - Tree Inspection',
                        'PARKS & RECREATION - Tree Stump Removal/Grinding',
                        'PARKS & RECREATION - Insects in Trees',
                        'PARKS & RECREATION - Branch/Brush Removal - MOBILE',
                        'PARKS & RECREATION - Tree Trimming - MOBILE',
                        'PARKS & RECREATION - YES Gypsy Moth Treatment 060419',
                        'PARKS & RECREATION - Gypsy Moths',
                        'PARKS & RECREATION - Tree Trimming in Alleys or Utility Easement',
                        'PARKS & RECREATION - Tree Removal Requests - MOBILE 08/18/17',
                        'PARKS & RECREATION - Tree, Branch, and Brush Removal due to July 6, 2014 storm damage 10/03/14',
                        'PARKS & RECREATION - Fallen Tree, Tree Down - MOBILE 08/18/17',
                        'PARKS & RECREATION - Trimming or Removal of City Trees by Residents',
                        'PARKS & RECREATION - Tree Stakes',
                        'PARKS & RECREATION - Tree Removal Requests - EMAIL',
                        'PARKS & RECREATION - Tree Root Cutting',
                        'PARKS & RECREATION - Branch/Brush Removal - EMAIL',
                        'PARKS & RECREATION - Markings on City Tree',
                        'PARKS & RECREATION - Stump Removal Request - MOBILE 08/18/17',
                        'PARKS & RECREATION - Tree Grates and Power Outlets',
                        'PARKS & RECREATION - Tree Removal Notice Postcard',
                        'PARKS & RECREATION - Tree Inspection - MOBILE 08/18/17',
                        'PARKS & RECREATION - Tree Trimming - EMAIL',
                        'PARKS & RECREATION - Tree Planting or Opt-Out - MOBILE 08/18/17',
                        'PARKS & RECREATION - Tree Inspection - EMAIL',
                        'PARKS & RECREATION - Tree Planting or Opt-Out - EMAIL',
                        'PARKS & RECREATION - Stump Removal Request - EMAIL',
                        'PARKS & RECREATION - Fallen Tree, Tree Down - EMAIL',
                        'PARKS & RECREATION - Insects in Trees - MOBILE',
                        'PARKS & RECREATION - Tree Trimming - WALK UP',
                        'PARKS & RECREATION - Tree stakes placed in right of way',
                        'PARKS & RECREATION - Tree Trimming on Edgewood, Woodcliff, Vassar, and Hampshire',
                        'Parks and Recreation - Oak Wilt Spread Prevention and Information (Press Release)',
                        'PARKS & RECREATION - Branch/Brush Removal - WALK UP',
                        'PARKS & RECREATION - NO Gypsy Moth Treatment 060419',
                        'PARKS & RECREATION - Tree Grates and Power Outlets - EMAIL',
                        'PARKS & RECREATION - Tree Planting or Opt-Out - WALK UP',
                        'PARKS & RECREATION - Tree Removal Request - WALK UP',
                        'PARKS & RECREATION - Tree Trimming in Alleys or Utility Easement - MOBILE 08/18/17']

    elc_scripts = ['TRAFFIC SAFETY - Street Lighting Issue 010719',
                   'TRAFFIC SAFETY- Pole Accidents, Damaged/Downed Poles or Lines 102218',
                   'TRAFFIC SAFETY- Pole Accidents, Damaged / Downed Poles or Lines - MOBILE 08/18/17',
                   'TRAFFIC SAFETY - Street Lighting',
                   'TRAFFIC SAFETY - Lights on Downtown Bridges 010719',
                   'TRAFFIC SAFETY - Wires Down/Downed Power Lines - MOBILE 08/18/17',
                   'TRAFFIC SAFETY - Street Lighting Issue - MOBILE',
                   'TRAFFIC SAFETY - Emergency, Street Lighting (at night)',
                   'TRAFFIC SAFETY- Pole Accidents, Damaged / Downed Poles or Lines - EMAIL 102218',
                   'TRAFFIC SAFETY - Amount of Voltage Line 102218',
                   'TRAFFIC SAFETY - Alley - Lights - 12/08/2016',
                   'TRAFFIC SAFETY - Street Lighting Issue - WALK UP 010719']

    # Label Outside Agencies
    dataframe.loc[~dataframe['Department'].str.contains('|'.join(dept_list), na=False)] = 'OTHER OUTSIDE AGENCIES'

    # Replace nan with Blanks
    dataframe.loc[dataframe['Department'].isna(), 'Department'] = None

    # Override Department Labels for Select Scripts
    dataframe.loc[dataframe['Script Used'].str.contains('forestry', case=False, na=False), 'Department'] = 'FORESTRY'
    dataframe.loc[dataframe['Script Used'].isin(forestry_scripts), 'Department'] = 'FORESTRY'

    dataframe.loc[dataframe['Script Used'].str.contains(r'\s*elc\s+', case=False, na=False), 'Department'] = 'ELC'
    dataframe.loc[dataframe['Script Used'].isin(elc_scripts), 'Department'] = 'ELC'

    return dataframe['Department']
