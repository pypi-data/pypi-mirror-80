This is is the **ribofinder** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ project

:Overview: Simple parallele workflow to detect and report ribosomal content
:Input: FastQ files
:Output: HTML reports
:Status: draft
:Citation: Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI doi:10.21105/joss.00352


Installation
~~~~~~~~~~~~

You must install Sequana first::

    pip install sequana

Then, just install this package::

    pip install sequana_ribofinder


Usage
~~~~~

::

    sequana_pipelines_ribofinder --help
    sequana_pipelines_ribofinder --input-directory DATAPATH 

This creates a directory with the pipeline and configuration file. You will then need 
to execute the pipeline::

    cd ribofinder
    sh ribofinder.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can 
retrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::

    snakemake -s ribofinder.rules -c config.yaml --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- bowtie1

.. image:: https://raw.githubusercontent.com/sequana/sequana_ribofinder/master/sequana_pipelines/ribofinder/dag.png


Details
~~~~~~~~~

This pipeline runs **ribofinder** in parallel on the input fastq files (paired or not). 
A brief sequana summary report is also produced.


Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/sequana_ribofinder/master/sequana_pipelines/ribofinder/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 

Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.9.2     **First release.**
========= ====================================================================


