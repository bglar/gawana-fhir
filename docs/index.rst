Welcome to fhir-server's documentation
======================================

This is a documentation on FHIR, focusing majorly on Profiling.

What is FHIR?
-------------

Fast Healthcare Interoperability Resources (FHIR) is an interoperability
standard developed by Health Level Seven International (HL7) for electronic
exchange of healthcare information.

FHIR describes a set of base resources, frameworks and APIs that are used in
many different contexts in healthcare. However, there are variations across
different healthcare practices, jurisdictions etc. As a consequence, this
specification usually requires further adaptation to particular contexts of use.

Profiling in FHIR
-----------------

The standard base resources have very generic definitions. A FHIR profile allows
you to author and publish a customized, more specific resource definition, by
specifying a set of constraints and/or extensions on the base resource. Concrete
FHIR resources e.g. a Patient resource can express their conformance to a
specific profile. This allows a FHIR server to programmatically validate a given
resource against the associated profile definition.


A StructureDefinition Resource
------------------------------

This resource describes the underlying resources, data types defined in FHIR,
and also extensions, and constraints on these resources and data types.

The StructureDefinition resource describes a structure - a set of data element
definitions, and their associated rules of usage.

Slicing
-------



Contents
--------

.. toctree::
   :maxdepth: 2

   profiling
   parsers
   validation



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
