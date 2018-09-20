Implementing Profiles in FHIR
=============================

Profiling resources puts the resource / model in context through:
    1. Extentions
    2. Constraints

The suggested FHIR Profiling approach involves  the creation of helper classes
(Mixins) that implement common functionalities shared across resources. The list
of fuctions to be abstracted includes:
    - Common FieldTypes / DataTypes (Primitive types and Complex types)
    - A parser that translated python classes to ORM compliant class types.
    - Helper classes for common API requirements such as CREATE, SEARCH, UPDATE


Extentions
----------
The following is a code snippet of what a developer creating a new profile extension
is required to do.:

.. code-block:: python
   :linenos:

    /**
     * This is an example of a customized model class that takes the
     * built-in Organization resource class, and extends it with a custom extension.
     */

    import resources / Mixins etc

    @ResourceDef(name = "Organization")
    class SilOrganization(Organization):

        /* *****************************
         * Fields
         * *****************************/
        class EmergencyContact(BaseIdentifiableElement, SilExtension):
            /**
             * This is a primitive datatype extension
             */
            Fields.Description = {
                // "...some definition..."
                shortDefinition: "Should be set to true if the contact is active"
            }
            Fields.Extension(url = {
                url: "http://foo#emergencyContactActive",
                isModifier: false,
                definedLocally: true
            }
            Fields.Child = {
                name: "active"
            }
            Fields.Type = BooleanDt
            Fileds.name = silActive

            // The Mixins can be overriden for custom actions
            def setActive(BooleanDt, silActive):
                ...
                ...
                ...
                // do something


            /**
             * **************************************
             * *************** OR *******************
             *
             * A complex datatype extension
             */


        /**
         * Here the idea is that the method will pass an instance of itself to the
         * Extention definition Mixin.
         */
        Extension(<<this SilOrganization instance>>)


The code snippet above shows a simple class definition of the new resources to be
created and the base fhir resource to be extended. In this case a  *SilOrganization*
extends *Organization*.

A decorator here (@ResourceDef) is also used to show that this is a resource definition.
We can provide more decorators for other components as need arises e.g @FieldDef decorator
would denote extending a given field.

.. code-block:: python
   :linenos:

   @ResourceDef(name = "Organization")
   class SilOrganization(Organization):

        new org_field_params = {
            description: {
                long: ... ,
                short: ... ,
            },
            cardinality: {
                min: ... ,
                max: ... ,
            },
            type: {},
            extension_url: {
                url: "http://foo#emergencyContactActive",
                isModifier: false,
                definedLocally: true
            }
        }

        new org_field = Resources.Fields.addNew(org_field_params)


Each resources also requires a definition of the mothods that can be used to manipulate them.
The example below shows the ideal case for adding some of these classes to a resource instance.


.. code-block:: python
   :linenos:

    class SilOrganisationProviders(ResourceProvider):

        @Get
        def get(IdParam, ...):
            return null; // populate this

        @Create
        def create(ResourceParam, ...):
            // save the resource

        @Update
        def update(ResourceParam, ...):
            // update the resource

        @Search
        def search(searchParams, ...):
            searchFields = {
                // define the search fields
            }
            return null; // populate this