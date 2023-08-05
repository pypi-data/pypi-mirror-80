
dgenome
-----------

Dgenome is a Django app which handle the genome coordinates 

Quick start
-----------

1. Add "dgenome" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dgenome',
    ]

2. Include the dgenome URLconf in your project urls.py like this::

    url(r'^dgenome/', include((dgenome.urls, 'dgenome'), namespace='dgenome')),

3. Run `python manage.py makemigrations dgenome` to create the dgenome models.

4. Run `python manage.py migrate` to create the dgenome models.

5. Insert the genomic data using the UCSC GTF file and the script: bin/load_genome_ucsc.py

