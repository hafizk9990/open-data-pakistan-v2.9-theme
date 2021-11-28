import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

class ExampleThemePlugin(plugins.SingletonPlugin):
    '''An example theme plugin.

    '''
    pass

    def update_config(self, config):
        # Adding this line overrides CKAN's default templates (.html jinja template files)
        # and allows us to define our own custom templates and pages
        
        # The word 'templates' is the path to the folder, 
        # relative to this file
        
        toolkit.add_template_directory(config, 'templates')