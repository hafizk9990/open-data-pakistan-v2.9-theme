import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

def Categories_Objects():
    return [
        {"url" : "/dataset?category=Agriculture%2C+Food+%26+Forests", "name" : "Agriculture, Food & Forests", "img": "agriculture"},
        {"url" : "/dataset?category=Cities+%26+Regions" , "name" : "Cities & Regions", "img": "cities"},
        {"url" : "/dataset?category=Connectivity" , "name" : "Connectivity", "img": "connectivity"},
        {"url" : "/dataset?category=Culture" , "name": "Culture", "img": "culture"},
        {"url" : "/dataset?category=Demography" , "name": "Demography", "img": "demography"},
        {"url" : "/dataset?category=Economy+%26+Finance" , "name" : "Economy & Finance", "img": "economy"},
        {"url" : "/dataset?category=Education" , "name" :"Education", "img": "education"},
        {"url" : "/dataset?category=Environment+%26+Energy" , "name" : "Environment & Energy", "img": "envoirnment"},
        {"url" : "/dataset?category=Government+%26+Public+Sector" , "name" : "Government & Public Sector", "img": "government"},
        {"url" : "/dataset?category=Health" , "name" : "Health", "img": "health"},
        {"url" : "/dataset?category=Housing+%26+Public+Services", "name" : "Housing & Public Services", "img": "housing"},
        {"url" : "/dataset?category=Manufacturing" , "name" : "Manufacturing", "img": "manufecturing"},
        {"url" : "/dataset?category=Public+Safety" , "name" : "Public Safety", "img": "publicsafety"},
        {"url" : "/dataset?category=Science+%26+Technology" , "name" : "Science & Technology", "img": "science"}
    ]

def Categories():
    return [
        "Agriculture, Food & Forests",
        "Cities & Regions",
        "Connectivity",
        "Culture",
        "Demography",
        "Economy & Finance",
        "Education",
        "Environment & Energy",
        "Government & Public Sector",
        "Health",
        "Housing & Public Services",
        "Manufacturing",
        "Public Safety",
        "Science & Technology"
    ]

def Facet_Count():
    try:
        counts = {}
        for cat in Categories():
            facet_name = 'category:"' + cat + '"'
            count = toolkit.get_action('package_search')(None, {'fq': facet_name})
            # count = 0
            counts[cat] = count['count']
        return counts
    except:
        return []

def Popular_Datasets():
    try:
        data =  toolkit.get_action('package_search')(None , {
            'sort': 'score desc, views_recent desc',
            'rows': 4
        })
        return data['results']
    except:
        return []

def Recently_Added_Datasets():
    try:
        data =  toolkit.get_action('package_search')(None , {
            'sort': 'score desc, metadata_created desc',
            'rows': 4
        })
        return data['results']
    except:
        return []

def Relevant_Datasets(cat):
    try:
        data =  toolkit.get_action('package_search')(None , {
            'sort': 'score desc, metadata_modified desc',
            'fq': 'category:"' + cat + '"',
            'rows' : 3
        })
        return data['results']
    except:
        return []
    
def Total_Views(package_id):
    try:
        data =  toolkit.get_action('package_show')(None , {
            'id': package_id,
            'include_tracking': True,
        })
        if data['tracking_summary']['total']:
            return data['tracking_summary']['total']
        else:
           return 10
    except:
        return 10

def Total_Organization_Views(organization_id):
    try:
        data =  toolkit.get_action('organization_show')(None , {
            'id': organization_id,
            'include_datasets': True,
        })
        if data['packages']:
            total_views = 0
            for pkg in data['packages']:
                total_views += Total_Views(pkg['id'])
            return total_views
        else:
           return 10
    except:
        return 10

def Footer_Counts():
    footer_counts = {}
    dataset_count = toolkit.get_action('package_list')(None, {})
    organization_count = toolkit.get_action('organization_list')(None, {})
    categories_count = Categories()
    footer_counts['dataset'] = len(dataset_count)
    footer_counts['organization'] = len(organization_count)
    footer_counts['categories'] = len(categories_count)
    
    return footer_counts

class ExampleThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')

    def get_helpers(self):
        return {
            'facet_count': Facet_Count,
            'footer_counts': Footer_Counts,
            "popular_datasets" : Popular_Datasets,
            'relevant_datasets' : Relevant_Datasets,
            'category_objects' : Categories_Objects,
            'recently_added_dataset' : Recently_Added_Datasets,
            'get_views' : Total_Views,
            'get_org_views' : Total_Organization_Views,
        }
