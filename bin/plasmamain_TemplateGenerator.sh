#!/bin/sh
#WDN

#define parameters which are passed in.
GalaxyServer=$1
#define the template.
cat  << EOF
<!DOCTYPE html>
<html>
<title>Project</title>
	{% load static %}
	{% include "sequencer/header.html" %}    	
<body>
<div id="wrapper">
	{% include "sequencer/navigation_top.html" %}    	
	<!-- Page Content -->
	<div id="page-wrapper">
		<div class="container-fluid">
			<div class="row">
				<div class="col-lg-12">
					<h1 class="page-header">Plasma Mutation</h1>
					<div class="panel panel-green">
					{% if current_exp %}
						<div class="panel-heading">
						{% if user.is_authenticated  %}
						{% if experimentsDict %}
							<p><b>Analyse plasma pour le run {{ current_exp.run_name }}</b></p>
						</div>
						<div class="panel-body">
								<div class="alert alert-success">
									<p>Les résultats ont été envoyé à l'utilisateur  <font  color = "black">{{user.username}}</font> </p>
									<p>Un mail de suivi des opérations vous sera envoyé à votre adresse mail </p>
								</div>	
																						
								<div class="alert alert-success">
									<p><b>Détaille de vos analyses:  </b></p>								
									{% for bam in experimentsDict %}
										<p>{{bam }}</p>
										<p>---</p>
									{% endfor %}
									</div>																						
						</div>
						<div class="panel panel-primary">
						<div class="panel-heading" style="background-color: #669999;">
							<p><b>Retrouvez vos résultats en suivant le lien ci-dessous </b></p>
						</div>
						<div class="panel-body">
							<div class="alert alert-info">
						<center>
									<p> <a href="$GalaxyServer/history/view_multiple"><img src="{% static "sequencer/Galaxy_Project_resize.png" %}"  alt="retour à Galaxy"/></a></p>
						</center>

							</div>
						</div>															
					</div>
						{% if historyPlasma %}						
							<div class="alert alert-success">
							<p><b>Analyse plasma lancée le {{historyPlasma.today}} a été ajouté à l'historique galaxy nommé </b></p>								
								<p>{{historyPlasma.name}}</p>							
							</div>															
					</div>
						{% endif %}
					{% endif %}
					{% endif %}
				{% endif %}
                    <!-- /.panel-body -->
					</div>
				</div>
				<!-- /.col-lg-12 -->
			</div>
			<!-- /.row -->
		</div>
		<!-- /.container-fluid -->
	</div>
	<!-- /#page-wrapper -->	
	<!--Remaining section-->
</div>
	<!-- /#wrapper -->
 <!-- DataTables CSS -->
     <script src="{% static "bower_components/jquery/dist/jquery.min.js" %}" ></script>
    <!-- DataTables Responsive CSS -->
    <link href="{% static "bower_components/datatables-responsive/css/dataTables.responsive.css"  %}" rel="stylesheet">
    <link href="https://cdn.datatables.net/select/1.2.0/css/select.dataTables.min.css" rel="stylesheet">
    <!-- DataTables JavaScript -->
    <script src= "{% static "bower_components/datatables/media/js/jquery.dataTables.min.js"  %}" type="text/javascript"></script>
    <script src="{% static "bower_components/datatables-plugins/integration/bootstrap/3/dataTables.bootstrap.min.js"  %}" type="text/javascript"></script>
    <script src="{% static "bower_components/datatables-responsive/js/dataTables.responsive.js"  %}" type="text/javascript"></script>
    
    <!-- Custom Theme JavaScript -->
    <script src="{% static "dist/js/sb-admin-2.js"  %}" ></script>

    <!-- Page-Level Demo Scripts - Tables - Use for reference -->

    <script>
EOF
