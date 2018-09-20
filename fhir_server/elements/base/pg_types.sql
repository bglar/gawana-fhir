CREATE EXTENSION IF NOT EXISTS uri;

DROP TYPE fhir_operationoutcomeissue;
DROP TYPE fhir_patientlink;
DROP TYPE fhir_patientcontact;
DROP TYPE fhir_patientcommunication;
DROP TYPE fhir_patientanimal;
DROP TYPE fhir_practitionerqualification;
DROP TYPE fhir_practitionerpractitionerrole;
DROP TYPE fhir_healthcareservicenotavailable;
DROP TYPE fhir_healthcareserviceavailabletime;
DROP TYPE fhir_locationposition;
DROP TYPE fhir_valuesetexpansion;
DROP TYPE fhir_valuesetexpansionparameter;
DROP TYPE fhir_valuesetexpansioncontains;
DROP TYPE fhir_valuesetcontact;
DROP TYPE fhir_valuesetcompose;
DROP TYPE fhir_valuesetcomposeinclude;
DROP TYPE fhir_valuesetcomposeincludefilter;
DROP TYPE fhir_valuesetcomposeincludeconcept;
DROP TYPE fhir_valuesetcodesystem;
DROP TYPE fhir_valuesetcodesystemconcept;
DROP TYPE fhir_valuesetcodesystemconceptdesignation;
DROP TYPE fhir_structuredefinitionsnapshot;
DROP TYPE fhir_structuredefinitiondifferential;
DROP TYPE fhir_structuredefinitionmapping;
DROP TYPE fhir_structuredefinitioncontact;
DROP TYPE fhir_elementdefinition;
DROP TYPE fhir_elementdefinitiontype;
DROP TYPE fhir_elementdefinitionslicing;
DROP TYPE fhir_elementdefinitionmapping;
DROP TYPE fhir_elementdefinitionconstraint;
DROP TYPE fhir_elementdefinitionbinding;
DROP TYPE fhir_elementdefinitionbase;
DROP TYPE fhir_organizationcontact;
DROP TYPE fhir_meta;
DROP TYPE fhir_contactpoint;
DROP TYPE fhir_identifier;
DROP TYPE fhir_timing;
DROP TYPE fhir_timingrepeat;
DROP TYPE fhir_signature;
DROP TYPE fhir_sampleddata;
DROP TYPE fhir_ratio;
DROP TYPE fhir_extension;
DROP TYPE fhir_address;
DROP TYPE fhir_reference;
DROP TYPE fhir_annotation;
DROP TYPE fhir_attachment;
DROP TYPE fhir_coding;
DROP TYPE fhir_codeableconcept;
DROP TYPE fhir_humanname;
DROP TYPE fhir_narrative;
DROP TYPE fhir_quantity;
DROP TYPE fhir_age;
DROP TYPE fhir_money;
DROP TYPE fhir_count;
DROP TYPE fhir_distance;
DROP TYPE fhir_simplequantity;
DROP TYPE fhir_duration;
DROP TYPE fhir_range;
DROP TYPE fhir_period;


CREATE TYPE fhir_extension AS (url TEXT, value JSONB);

CREATE TYPE fhir_period AS (
    id TEXT, extension fhir_extension,
    "period_start" TIMESTAMP WITH TIME ZONE,
    "period_end" TIMESTAMP WITH TIME ZONE);

CREATE TYPE fhir_address AS (
    id TEXT, extension fhir_extension,
    city TEXT, country TEXT, district TEXT, line TEXT[],
    postalCode TEXT, state TEXT, text TEXT, use TEXT,
    "type" TEXT, period fhir_period);

CREATE TYPE fhir_reference AS (
    id TEXT, extension fhir_extension,
    display TEXT, reference TEXT);

CREATE TYPE fhir_annotation AS (
    id TEXT, extension fhir_extension, authorString TEXT,
    text TEXT, time TIMESTAMP WITH TIME ZONE,
    authorReference fhir_reference);

CREATE TYPE fhir_attachment AS (
    id TEXT, extension fhir_extension,
    contentType TEXT, creation TIMESTAMP WITH TIME ZONE,
    data TEXT, hash TEXT, language TEXT, size INTEGER,
    title TEXT, url TEXT);

CREATE TYPE fhir_coding AS (
    id TEXT, extension fhir_extension,
    code TEXT, display TEXT, system TEXT,
    userSelected BOOLEAN, version TEXT);

CREATE TYPE fhir_codeableconcept AS (
    id TEXT, extension fhir_extension,
    text TEXT, coding fhir_coding[]);

CREATE TYPE fhir_humanname AS (
    id TEXT, extension fhir_extension,
    family TEXT[], given TEXT[], prefix TEXT[],
    suffix TEXT[], text TEXT, use TEXT, period fhir_period);

CREATE TYPE fhir_narrative AS (
    id TEXT, extension fhir_extension,
    div TEXT, status TEXT);

CREATE TYPE fhir_quantity AS (
    id TEXT, extension fhir_extension,
    code TEXT, system TEXT,
    unit TEXT, value DECIMAL, comparator TEXT);

CREATE TYPE fhir_age AS (
    id TEXT, extension fhir_extension,
    code TEXT, system TEXT,
    unit TEXT, value DECIMAL, comparator TEXT);

CREATE TYPE fhir_money AS (
    id TEXT, extension fhir_extension,
    code TEXT, system TEXT,
    unit TEXT, value DECIMAL, comparator TEXT);

CREATE TYPE fhir_count AS (
    id TEXT, extension fhir_extension,
    code TEXT, system TEXT,
    value DECIMAL, comparator TEXT);

CREATE TYPE fhir_distance AS (
    id TEXT, extension fhir_extension,
    code TEXT, system TEXT,
    unit TEXT, value DECIMAL, comparator TEXT);

CREATE TYPE fhir_simplequantity AS (
    id TEXT, extension fhir_extension,
    code TEXT, system TEXT, unit TEXT, value DECIMAL);

CREATE TYPE fhir_duration AS (
    id TEXT, extension fhir_extension, code TEXT, system TEXT,
    unit TEXT, value DECIMAL, comparator TEXT);

CREATE TYPE fhir_range AS (
    id TEXT, extension fhir_extension,
    high fhir_simplequantity, low fhir_simplequantity);

CREATE TYPE fhir_ratio AS (
    id TEXT, extension fhir_extension,
    high fhir_quantity, low fhir_quantity);

CREATE TYPE fhir_sampleddata AS (
    id TEXT, extension fhir_extension, data TEXT, dimensions INTEGER,
    factor DECIMAL, lowerLimit DECIMAL, period DECIMAL,
    upperLimit DECIMAL, origin fhir_simplequantity);

CREATE TYPE fhir_signature AS (
    id TEXT, extension fhir_extension,
    blob TEXT, contentType TEXT, "when" TIMESTAMP WITH TIME ZONE,
    whoUri TEXT, whoReference fhir_reference, "type" fhir_coding[]);

CREATE TYPE fhir_timingrepeat AS (
    id TEXT, extension fhir_extension,
    count INTEGER, duration DECIMAL, durationMax DECIMAL,
    durationUnits TEXT, frequency INTEGER, frequencyMax INTEGER,
    period DECIMAL, perioMax DECIMAL, periodUnits TEXT,
    "when" TEXT, boundsPeriod fhir_period,
    boundsQuantity fhir_duration, boundsRange fhir_range);

CREATE TYPE fhir_timing AS (
    id TEXT, extension fhir_extension,
     event TIMESTAMP WITH TIME ZONE [], code fhir_codeableconcept,
     repeat fhir_timingrepeat);

CREATE TYPE fhir_identifier AS (
    id TEXT, extension fhir_extension,
    system TEXT, use TEXT, value TEXT, assigner fhir_reference,
    period fhir_period, "type" fhir_codeableconcept);

CREATE TYPE fhir_contactpoint AS (
    id TEXT, extension fhir_extension,
    rank INTEGER, system TEXT, use TEXT,
    value TEXT, period fhir_period);

CREATE TYPE fhir_meta AS (
    id TEXT, extension fhir_extension,
    versionId TEXT, lastUpdated TIMESTAMP WITH TIME ZONE,
    profile TEXT[], security fhir_coding[], tag fhir_coding[]);


----------------------------------------------------------------------------
-------------- RESOURCE BACKBONE ELEMENTS START HERE -----------------------
----------------------------------------------------------------------------


------------------------ ORGANIZATION BACKBONE ELEMENTS --------------------
CREATE TYPE fhir_organizationcontact AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    purpose fhir_codeableconcept,
    name fhir_humanname, address fhir_address,
    telecom fhir_contactpoint[]);


------------------ ELEMENT DEFINITION ELEMENTS -----------------------------
CREATE TYPE fhir_elementdefinitionbase AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    "max" TEXT, "min" INTEGER, path TEXT);

CREATE TYPE fhir_elementdefinitionbinding AS (
    id TEXT, extension fhir_extension,
    description TEXT, strength TEXT,
    valueSetReference fhir_reference, valueSetUri TEXT);

CREATE TYPE fhir_elementdefinitionconstraint AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    human TEXT, key TEXT, requirements TEXT,
    severity TEXT, xpath TEXT);

CREATE TYPE fhir_elementdefinitionmapping AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    identity TEXT, language TEXT, map TEXT);

CREATE TYPE fhir_elementdefinitionslicing AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    description TEXT, discriminator TEXT[],
    ordered BOOLEAN, rules TEXT);

CREATE TYPE fhir_elementdefinitiontype AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    aggregation TEXT[], code TEXT, profile TEXT[]);

CREATE TYPE fhir_elementdefinition AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    path TEXT, representation TEXT[], name TEXT,
    label TEXT, short TEXT, definition TEXT, comments TEXT,
    requirements TEXT, alias TEXT[], "min" INTEGER, "max" TEXT,
    nameReference TEXT, meaningWhenMissing TEXT, maxLength INTEGER,
    condition TEXT[], mustSupport BOOLEAN, isModifier BOOLEAN[],
    isSummary BOOLEAN, defaultValue JSON, fixed JSON, pattern JSON,
    example JSON, minValue JSON, maxValue JSON, code JSON[],
    slicing fhir_elementdefinitionslicing,
    base fhir_elementdefinitionbase,
    "type" fhir_elementdefinitiontype[],
    "constraint" fhir_elementdefinitionconstraint[],
    binding fhir_elementdefinitionbinding,
    mapping fhir_elementdefinitionmapping[]);

----------------- STRUCTURE DEFINITION BACKBONE ELEMENTS -------------------

CREATE TYPE fhir_structuredefinitioncontact AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    name TEXT, telecom fhir_contactpoint);

CREATE TYPE fhir_structuredefinitionmapping AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    identity TEXT, uri TEXT, name TEXT, comments TEXT);

CREATE TYPE fhir_structuredefinitiondifferential AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    element fhir_elementdefinition);

CREATE TYPE fhir_structuredefinitionsnapshot AS (
    id TEXT, extension fhir_extension,
    element fhir_elementdefinition);


------------ VALUESET RESOURCE BACKBONE ELEMENTS -------------------------

CREATE TYPE fhir_valuesetcodesystemconceptdesignation AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    "language" TEXT, "value" TEXT, use TEXT);

CREATE TYPE fhir_valuesetcodesystemconcept AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    code TEXT, abstract BOOLEAN, display TEXT,
    definition TEXT, concept TEXT[],
    designation fhir_valuesetcodesystemconceptdesignation);

CREATE TYPE fhir_valuesetcodesystem AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    system TEXT, version TEXT, caseSensitive BOOLEAN,
    concept fhir_valuesetcodesystemconcept[]);

CREATE TYPE fhir_valuesetcomposeincludeconcept AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    code TEXT, display TEXT,
    designation fhir_valuesetcodesystemconceptdesignation[]);

CREATE TYPE fhir_valuesetcomposeincludefilter AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    op TEXT, property TEXT, "value" TEXT);

CREATE TYPE fhir_valuesetcomposeinclude AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    system TEXT, version TEXT,
    concept fhir_valuesetcomposeincludeconcept[],
    filter fhir_valuesetcomposeincludefilter[]);

CREATE TYPE fhir_valuesetcompose AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    compose_import TEXT[], include fhir_valuesetcomposeinclude[],
    exclude fhir_valuesetcomposeinclude[]);

CREATE TYPE fhir_valuesetcontact AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    name TEXT, telecom fhir_contactpoint[]);

CREATE TYPE fhir_valuesetexpansioncontains AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    abstract BOOLEAN, code TEXT, display TEXT,
    system TEXT, version TEXT, contains TEXT[]);

CREATE TYPE fhir_valuesetexpansionparameter AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    name TEXT, valueBoolean BOOLEAN, valueCode TEXT,
    valueDecimal DECIMAL, valueInteger INTEGER,
    valueString TEXT, valueUri TEXT);

CREATE TYPE fhir_valuesetexpansion AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    identifier TEXT[], "timestamp" TIMESTAMP WITH TIME ZONE,
    "offset" INTEGER, total INTEGER,
    parameter fhir_valuesetexpansionparameter,
    contains fhir_valuesetexpansioncontains);

------------ LOCATION RESOURCE BACKBONE ELEMENTS -------------------------

CREATE TYPE fhir_locationposition AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    longitude DECIMAL, latitude DECIMAL, altitude DECIMAL);

------------ LOCATION HEALTHCARESERVICE BACKBONE ELEMENTS ----------------

CREATE TYPE fhir_healthcareserviceavailabletime AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    daysOfWeek TEXT[], allDay BOOLEAN,
    availableStartTime TIME, availableEndTime TIME);

CREATE TYPE fhir_healthcareservicenotavailable AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    description TEXT, during fhir_period);

------------ PRACTITIONER RESOURCE BACKBONE ELEMENTS ---------------------

CREATE TYPE fhir_practitionerpractitionerrole AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    organization fhir_reference, role fhir_codeableconcept,
    specialty fhir_codeableconcept[], identifier fhir_identifier[],
    telecom fhir_contactpoint[], period fhir_period,
    location fhir_reference[], healthcareService fhir_reference[]);

CREATE TYPE fhir_practitionerqualification AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    identifier fhir_identifier[], code fhir_codeableconcept,
    period fhir_period, issuer fhir_reference);

----------------- PATIENT RESOURCE BACKBONE ELEMENTS ---------------------

CREATE TYPE fhir_patientanimal AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    breed fhir_codeableconcept,
    genderStatus fhir_codeableconcept,
    species fhir_codeableconcept);

CREATE TYPE fhir_patientcommunication AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    "language" fhir_codeableconcept,
    preferred BOOLEAN);

CREATE TYPE fhir_patientcontact AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    relationship fhir_codeableconcept[], name fhir_humanname,
    telecom fhir_contactpoint[], address fhir_address,
    gender TEXT, organization fhir_reference, period fhir_period);

CREATE TYPE fhir_patientlink AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    other fhir_reference, "type" TEXT);

-------------------- OPERATION OUTCOME BACKBONE ELEMENT -------------------
CREATE TYPE fhir_operationoutcomeissue AS (
    id TEXT, extension fhir_extension,
    modifierExtension fhir_extension[],
    code TEXT, severity TEXT, "diagnostics" TEXT,
    location TEXT, expression TEXT, details fhir_codeableconcept);
