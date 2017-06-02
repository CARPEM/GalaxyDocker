<%namespace file="ie.mako" name="ie"/>
<%
import os
import shutil
import time

# Sets ID and sets up a lot of other variables
ie_request.load_deploy_config()
ie_request.attr.docker_port = 3838
# Create tempdir in galaxy
#temp_dir = ie_request.temp_dir
#PASSWORD = ie_request.notebook_pw
#USERNAME = "galaxy"
#print "because top"

# Did the user give us an RData file?
#if hda.datatype.__class__.__name__ == "RData":
#    shutil.copy( hda.file_name, os.path.join(temp_dir, '.RData') )
#will put the right file here  
#data type definition
#/galaxy-central/lib/galaxy/datatypes  
#Appfolder = ie_request.volume('/galaxy-central/tools/shiny_docker/shinytest', '/srv/shiny-server/', how='ro')
CNVdata = ie_request.volume(hda.file_name, '/srv/shiny-server/data/inputdata.txt', how='ro')
#cnvMatrix = ie_request.volume(hda.file_name, '/srv/shiny-server/data/marc/R_2016_04_06_11_39_1bcmatrix.xls', how='ro')
#cnvSummary = ie_request.volume(test.file_name, '/srv/shiny-server/data/marc/R_2016_04_06_11_39_13bc_summary.xls', how='ro')
#print "because yolo from request"
ie_request.launch(volumes=[CNVdata],env_override={
    'PUB_HOSTNAME': ie_request.attr.HOST,
})

## General IE specific
# Access URLs for the notebook from within galaxy.
# TODO: Make this work without pointing directly to IE. Currently does not work
# through proxy.
#notebook_access_url = ie_request.url_template('${PROXY_URL}/?bam=http://localhost/tmp/bamfile.bam')
notebook_access_url = ie_request.url_template('${PROXY_URL}/?')

#notebook_pubkey_url = ie_request.url_template('${PROXY_URL}/rstudio/auth-public-key')
#notebook_access_url = ie_request.url_template('${PROXY_URL}/rstudio/')
#notebook_login_url =  ie_request.url_template('${PROXY_URL}/rstudio/auth-do-sign-in')

root = h.url_for( '/' )

%>
<html>
<head>
${ ie.load_default_js() }
</head>
<body style="margin:0px">
<script type="text/javascript">

        ${ ie.default_javascript_variables() }
        var notebook_access_url = '${ notebook_access_url }';
        ${ ie.plugin_require_config() }

        requirejs(['interactive_environments', 'plugin/bam_iobio'], function(){
            display_spinner();
        });

        toastr.info(
            "Loading data into the App",
            "...",
            {'closeButton': true, 'timeOut': 5000, 'tapToDismiss': false}
        );

        var startup = function(){
            // Load notebook
          requirejs(['interactive_environments', 'plugin/bam_iobio'], function(){
           //    requirejs(['interactive_environments'], function(){
                load_notebook(notebook_access_url);
            });

        };
        // sleep 5 seconds
        // this is currently needed to get the vis right
        // plans exists to move this spinner into the container
        setTimeout(startup, 5000);

</script>
<div id="main">
</div>
</body>
</html>
