# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-31 13:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentRawData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ionTag', models.CharField(default='no tag', max_length=200)),
                ('sampleName', models.CharField(default='no sample name', max_length=200)),
                ('bam_path', models.CharField(default='no path', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Experiments',
            fields=[
                ('run_name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('ftpStatus', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('cnvFileName', models.CharField(default='no cnv', max_length=200)),
                ('resultsQuery', models.CharField(default='no results', max_length=200)),
                ('dateIonProton', models.CharField(default='no date', max_length=200)),
                ('dictionnary', models.TextField(default='no dict')),
            ],
        ),
        migrations.CreateModel(
            name='GalaxyJobs',
            fields=[
                ('tag_id', models.CharField(default='no_tag', max_length=200, primary_key=True, serialize=False)),
                ('resultsName', models.CharField(default='no_resultsName', max_length=200)),
                ('history_id', models.CharField(default='no_id', max_length=200)),
                ('history_name', models.CharField(default='no_name', max_length=200)),
                ('history_state', models.CharField(default='no_state', max_length=200)),
                ('history_today', models.CharField(default='no_day', max_length=200)),
                ('history_percent_complete', models.CharField(default='no_complete', max_length=200)),
                ('history_datasets_id', models.CharField(default='no_datasets', max_length=500)),
                ('history_download', models.BooleanField(default=False)),
                ('progression', models.CharField(default='suspendu', max_length=200)),
                ('galaxy_dictionnary', models.TextField(default='no dict')),
            ],
        ),
        migrations.CreateModel(
            name='GalaxyUsers',
            fields=[
                ('user_id', models.CharField(max_length=200)),
                ('user_email', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('user_aphid', models.CharField(max_length=200)),
                ('user_apikey', models.CharField(default='no_apikey', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Supportedfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataHandle', models.CharField(default='dataHandle', max_length=200)),
                ('dataDescription', models.CharField(default='dataDescription', max_length=200)),
                ('dataFormatEdamOntology', models.CharField(default='dataFormatEdamOntology', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Workflows',
            fields=[
                ('name', models.CharField(default='no_name', max_length=200, primary_key=True, serialize=False)),
                ('description', models.CharField(default='description', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowsTools',
            fields=[
                ('primary_name', models.CharField(default='no_name', max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(default='no_name', max_length=200)),
                ('version', models.CharField(default='version', max_length=200)),
                ('inputlist', models.ManyToManyField(related_name='inputlist', to='sequencer.Supportedfiles')),
                ('outputlist', models.ManyToManyField(related_name='outputlist', to='sequencer.Supportedfiles')),
            ],
        ),
        migrations.AddField(
            model_name='workflows',
            name='tools_list',
            field=models.ManyToManyField(to='sequencer.WorkflowsTools'),
        ),
        migrations.AddField(
            model_name='galaxyjobs',
            name='history_analyse_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sequencer.Workflows'),
        ),
        migrations.AddField(
            model_name='galaxyjobs',
            name='history_user_email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sequencer.GalaxyUsers'),
        ),
        migrations.AddField(
            model_name='galaxyjobs',
            name='list_experimentRawData',
            field=models.ManyToManyField(to='sequencer.ExperimentRawData'),
        ),
        migrations.AddField(
            model_name='experimentrawdata',
            name='experienceName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sequencer.Experiments'),
        ),
    ]