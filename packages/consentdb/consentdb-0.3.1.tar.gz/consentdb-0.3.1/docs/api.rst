.. _api_definitions:

===============
API definitions
===============

Consent API definition
======================

.. openapi:: ../consentdb/consentdb_api.yaml

Full spec
---------
.. literalinclude:: ../consentdb/consentdb_api.yaml

Legacy API (opt-out)
====================

It is recommended to upgrade any application to use the API definition above. For older applications that cannot be
upgraded, this is the specification for the legacy (opt-out) API::

/opt-outs/?pid={pid}

return codes are all http 200, but content will tell you what the actual response was::

 'Not found'  -> data for this patient can be used
 'Objection'  -> data for this patient can not be used


