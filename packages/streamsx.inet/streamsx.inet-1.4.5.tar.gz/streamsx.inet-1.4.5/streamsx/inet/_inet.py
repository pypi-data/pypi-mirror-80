# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

import datetime
from tempfile import gettempdir
import streamsx.spl.op
import streamsx.spl.types
from streamsx.topology.schema import CommonSchema, StreamSchema
from streamsx.spl.types import rstring
import streamsx.spl.toolkit
from streamsx.toolkits import download_toolkit

_TOOLKIT_NAME = 'com.ibm.streamsx.inet'


HttpResponseSchema = StreamSchema('tuple<rstring status, int32 statusCode, rstring contentEncoding, rstring contentType, list<rstring> responseHeader, rstring responseData>')
"""Structured schema containing HTTP GET/PUT/POST/DELETE response values.

``'tuple<rstring status, int32 statusCode, rstring contentEncoding, rstring contentType, list<rstring> responseHeader, rstring responseData>'``
"""


def download_toolkit(url=None, target_dir=None):
    r"""Downloads the latest Inet toolkit from GitHub.

    Example for updating the Inet toolkit for your topology with the latest toolkit from GitHub::

        import streamsx.inet as inet
        # download Inet toolkit from GitHub
        inet_toolkit_location = inet.download_toolkit()
        # add the toolkit to topology
        streamsx.spl.toolkit.add_toolkit(topology, inet_toolkit_location)

    Example for updating the topology with a specific version of the Inet toolkit using a URL::

        import streamsx.inet as inet
        url310 = 'https://github.com/IBMStreams/streamsx.inet/releases/download/v3.1.0/streamsx.inet.toolkit-3.1.0-el6-amd64-70c49d5-20190320-1318.tgz'
        inet_toolkit_location = inet.download_toolkit(url=url310)
        streamsx.spl.toolkit.add_toolkit(topology, inet_toolkit_location)

    Args:
        url(str): Link to toolkit archive (\*.tgz) to be downloaded. Use this parameter to 
            download a specific version of the toolkit.
        target_dir(str): the directory where the toolkit is unpacked to. If a relative path is given,
            the path is appended to the system temporary directory, for example to /tmp on Unix/Linux systems.
            If target_dir is ``None`` a location relative to the system temporary directory is chosen.

    Returns:
        str: the location of the downloaded Inet toolkit

    .. note:: This function requires an outgoing Internet connection
    .. versionadded:: 1.2
    """
    _toolkit_location = streamsx.toolkits.download_toolkit (toolkit_name=_TOOLKIT_NAME, url=url, target_dir=target_dir)
    return _toolkit_location


def _add_toolkit_dependency(topo, version):
    # IMPORTANT: Dependency of this python wrapper to a specific toolkit version
    # This is important when toolkit is not set with streamsx.spl.toolkit.add_toolkit (selecting toolkit from remote build service)
    streamsx.spl.toolkit.add_toolkit_dependency(topo, _TOOLKIT_NAME, version)


def request_delete(stream, url=None, url_attribute=None, extra_header_attribute=None, ssl_accept_all_certificates=False, name=None):
    """Issues HTTP DELETE requests. For each input tuple a DELETE request is issued and the response is on the returned stream. You can specifiy the URL either dynamic (part of input stream) or static (as parameter).

    Example with URL as part of the input stream of type ``CommonSchema.String``. The parameters ``url`` and ``url_attribute`` can be omitted in this case::

        import streamsx.inet as inet

        s = topo.source(['http://httpbin.org/delete']).as_string()
        result_http_del = inet.request_delete(s)
        result_http_del.print()

    Args:
        stream(streamsx.topology.topology.Stream): Stream of tuples containing the HTTP request url. Supports ``streamsx.topology.schema.StreamSchema`` (schema for a structured stream) or ``CommonSchema.String`` as input.
        url(str): String containing the URL to send HTTP requests to.
        url_attribute(str): Attribute name of the input stream containing the URL to send HTTP requests to. Use this as alternative to the 'url' parameter.
        extra_header_attribute(str): Attribute name of the input stream containing one extra header to send with the request, the attribute must contain a string in the form Header-Name: value. If the attribute value is an empty string, no additional header is send.
        ssl_accept_all_certificates(bool): Accept all SSL certificates, even those that are self-signed. Setting this option will allow potentially insecure connections. Default is false.
        name(str): Sink name in the Streams context, defaults to a generated name.

    Returns:
        :py:class:`topology_ref:streamsx.topology.topology.Stream`: Output Stream with schema :py:const:`~streamsx.inet.HttpResponseSchema`.
    """

    if url_attribute is None and url is None:
        if stream.oport.schema == CommonSchema.String:
            url_attribute = 'string'
        else:
            raise ValueError("Either url_attribute or url parameter must be set.")

    _op = _HTTPRequest(stream, schema=HttpResponseSchema, name=name)
    _op.params['fixedMethod'] = _op.expression('DELETE')
    if url_attribute is not None:
        _op.params['url'] = _op.attribute(stream, url_attribute)
    else:
        _op.params['fixedUrl'] = url
    # set output schema attribute names
    _op.params['outputBody'] = 'responseData'
    _op.params['outputStatus'] = 'status'
    _op.params['outputStatusCode'] = 'statusCode'
    _op.params['outputContentEncoding'] = 'contentEncoding'
    _op.params['outputContentType'] = 'contentType'
    _op.params['outputHeader'] = 'responseHeader'
    _op.params['sslAcceptAllCertificates'] = ssl_accept_all_certificates
    if extra_header_attribute is not None:
        _op.params['extraHeaderAttribute'] = _op.attribute(stream, extra_header_attribute)
        _add_toolkit_dependency(stream.topology, '[3.0.0,4.0.0)') # extraHeaderAttribute parameter has been introduced in v3.0

    return _op.outputs[0]


def request_get(stream, url=None, url_attribute=None, extra_header_attribute=None, ssl_accept_all_certificates=False, name=None):
    """Issues HTTP GET requests. For each input tuple a GET request is issued and the response is on the returned stream. You can specifiy the URL either dynamic (part of input stream) or static (as parameter).

    Example with URL as part of the input stream of type ``CommonSchema.String``. The parameters ``url`` and ``url_attribute`` can be omitted in this case::

        import streamsx.inet as inet

        s = topo.source(['http://httpbin.org/get']).as_string()
        result_http_get = inet.request_get(s)
        result_http_get.print()

    Args:
        stream(streamsx.topology.topology.Stream): Stream of tuples containing the HTTP request url. Supports ``streamsx.topology.schema.StreamSchema`` (schema for a structured stream) or ``CommonSchema.String`` as input.
        url(str): String containing the URL to send HTTP requests to.
        url_attribute(str): Attribute name of the input stream containing the URL to send HTTP requests to. Use this as alternative to the 'url' parameter.
        extra_header_attribute(str): Attribute name of the input stream containing one extra header to send with the request, the attribute must contain a string in the form Header-Name: value. If the attribute value is an empty string, no additional header is send.
        ssl_accept_all_certificates(bool): Accept all SSL certificates, even those that are self-signed. Setting this option will allow potentially insecure connections. Default is false.
        name(str): Sink name in the Streams context, defaults to a generated name.

    Returns:
        :py:class:`topology_ref:streamsx.topology.topology.Stream`: Output Stream with schema :py:const:`~streamsx.inet.HttpResponseSchema`.
    """

    if url_attribute is None and url is None:
        if stream.oport.schema == CommonSchema.String:
            url_attribute = 'string'
        else:
            raise ValueError("Either url_attribute or url parameter must be set.")

    _op = _HTTPRequest(stream, schema=HttpResponseSchema, name=name)
    _op.params['fixedMethod'] = _op.expression('GET')
    if url_attribute is not None:
        _op.params['url'] = _op.attribute(stream, url_attribute)
    else:
        _op.params['fixedUrl'] = url
    # set output schema attribute names
    _op.params['outputBody'] = 'responseData'
    _op.params['outputStatus'] = 'status'
    _op.params['outputStatusCode'] = 'statusCode'
    _op.params['outputContentEncoding'] = 'contentEncoding'
    _op.params['outputContentType'] = 'contentType'
    _op.params['outputHeader'] = 'responseHeader'
    _op.params['sslAcceptAllCertificates'] = ssl_accept_all_certificates
    if extra_header_attribute is not None:
        _op.params['extraHeaderAttribute'] = _op.attribute(stream, extra_header_attribute)
        _add_toolkit_dependency(stream.topology, '[3.0.0,4.0.0)') # extraHeaderAttribute parameter has been introduced in v3.0

    return _op.outputs[0]


def request_post(stream, url=None, url_attribute=None, body_attribute=None, content_type=None, content_type_attribute=None, extra_header_attribute=None, ssl_accept_all_certificates=False, name=None):
    """Issues HTTP POST requests. For each input tuple a POST request is issued and the response is on the returned stream. You can specifiy the URL either dynamic (part of input stream) or static (as parameter).

    Example with URL as part of the input stream of type ``CommonSchema.String``. The parameters ``url`` and ``url_attribute`` can be omitted in this case::

        import streamsx.inet as inet

        s = topo.source(['http://httpbin.org/post']).as_string()
        result_http_post = inet.request_post(s)
        result_http_post.print()

    Example with URL as part of the input stream and content type as parameter::

        import streamsx.inet as inet

        s = topo.source(['http://httpbin.org/post']).as_string()
        result_http_post = inet.request_post(s, content_type='application/x-www-form-urlencoded')
        result_http_post.print()

    Args:
        stream(streamsx.topology.topology.Stream): Stream of tuples containing the HTTP request url. Supports ``streamsx.topology.schema.StreamSchema`` (schema for a structured stream) or ``CommonSchema.String`` as input.
        url(str): String containing the URL to send HTTP requests to.
        url_attribute(str): Attribute name of the input stream containing the URL to send HTTP requests to. Use this as alternative to the 'url' parameter.
        body_attribute(str): Request body attribute for POST method that accepts an entity.
        content_type(str): MIME content type of entity for POST requests. If not specified the default 'application/json' is used.
        content_type_attribute(str): Attribute name of the input stream containing the MIME content type. Use this as alternative to the 'content_type' parameter.
        extra_header_attribute(str): Attribute name of the input stream containing one extra header to send with the request, the attribute must contain a string in the form Header-Name: value. If the attribute value is an empty string, no additional header is send.
        ssl_accept_all_certificates(bool): Accept all SSL certificates, even those that are self-signed. Setting this option will allow potentially insecure connections. Default is false.
        name(str): Sink name in the Streams context, defaults to a generated name.

    Returns:
        :py:class:`topology_ref:streamsx.topology.topology.Stream`: Output Stream with schema :py:const:`~streamsx.inet.HttpResponseSchema`.
    """

    if url_attribute is None and url is None:
        if stream.oport.schema == CommonSchema.String:
            url_attribute = 'string'
        else:
            raise ValueError("Either url_attribute or url parameter must be set.")

    _op = _HTTPRequest(stream, schema=HttpResponseSchema, name=name)
    _op.params['fixedMethod'] = _op.expression('POST')
    if url_attribute is not None:
        _op.params['url'] = _op.attribute(stream, url_attribute)
    else:
        _op.params['fixedUrl'] = url

    if body_attribute is not None:
        _op.params['requestBodyAttribute'] = _op.attribute(stream, body_attribute)

    if content_type_attribute is not None:
        _op.params['contentType'] = _op.attribute(stream, content_type_attribute)
    else:
        if content_type is not None:
            _op.params['fixedContentType'] = content_type

    # set output schema attribute names
    _op.params['outputBody'] = 'responseData'
    _op.params['outputStatus'] = 'status'
    _op.params['outputStatusCode'] = 'statusCode'
    _op.params['outputContentEncoding'] = 'contentEncoding'
    _op.params['outputContentType'] = 'contentType'
    _op.params['outputHeader'] = 'responseHeader'
    _op.params['sslAcceptAllCertificates'] = ssl_accept_all_certificates
    if extra_header_attribute is not None:
        _op.params['extraHeaderAttribute'] = _op.attribute(stream, extra_header_attribute)
        _add_toolkit_dependency(stream.topology, '[3.0.0,4.0.0)') # extraHeaderAttribute parameter has been introduced in v3.0

    return _op.outputs[0]


def request_put(stream, url=None, url_attribute=None, body_attribute=None, content_type=None, content_type_attribute=None, extra_header_attribute=None, ssl_accept_all_certificates=False, name=None):
    """Issues HTTP PUT requests. For each input tuple a PUT request is issued and the response is on the returned stream. You can specifiy the URL either dynamic (part of input stream) or static (as parameter).

    Example with parameters ``url``, ``content_type`` and input stream containing the request body::

        import streamsx.inet as inet

        s = topo.source(['hello world']).as_string()
        result_http_put = inet.request_put(s, url='http://httpbin.org/put', content_type='text/plain')
        result_http_put.print()

    Args:
        stream(streamsx.topology.topology.Stream): Stream of tuples containing the HTTP request url. Supports ``streamsx.topology.schema.StreamSchema`` (schema for a structured stream) or ``CommonSchema.String`` as input.
        url(str): String containing the URL to send HTTP requests to.
        url_attribute(str): Attribute name of the input stream containing the URL to send HTTP requests to. Use this as alternative to the 'url' parameter.
        body_attribute(str): Request body attribute for PUT method that accepts an entity.
        content_type(str): MIME content type of entity for PUT requests. If not specified the default 'application/json' is used.
        content_type_attribute(str): Attribute name of the input stream containing the MIME content type. Use this as alternative to the 'content_type' parameter.
        extra_header_attribute(str): Attribute name of the input stream containing one extra header to send with the request, the attribute must contain a string in the form Header-Name: value. If the attribute value is an empty string, no additional header is send.
        ssl_accept_all_certificates(bool): Accept all SSL certificates, even those that are self-signed. Setting this option will allow potentially insecure connections. Default is false.
        name(str): Sink name in the Streams context, defaults to a generated name.

    Returns:
        :py:class:`topology_ref:streamsx.topology.topology.Stream`: Output Stream with schema :py:const:`~streamsx.inet.HttpResponseSchema`.
    """

    if url_attribute is None and url is None:
        if stream.oport.schema == CommonSchema.String:
            url_attribute = 'string'
        else:
            raise ValueError("Either url_attribute or url parameter must be set.")

    if body_attribute is None and url is not None:
        if stream.oport.schema == CommonSchema.String:
            body_attribute = 'string'

    _op = _HTTPRequest(stream, schema=HttpResponseSchema, name=name)
    _op.params['fixedMethod'] = _op.expression('PUT')
    if url_attribute is not None:
        _op.params['url'] = _op.attribute(stream, url_attribute)
    else:
        _op.params['fixedUrl'] = url

    if body_attribute is not None:
        _op.params['requestBodyAttribute'] = _op.attribute(stream, body_attribute)

    if content_type_attribute is not None:
        _op.params['contentType'] = _op.attribute(stream, content_type_attribute)
    else:
        if content_type is not None:
            _op.params['fixedContentType'] = content_type

    # set output schema attribute names
    _op.params['outputBody'] = 'responseData'
    _op.params['outputStatus'] = 'status'
    _op.params['outputStatusCode'] = 'statusCode'
    _op.params['outputContentEncoding'] = 'contentEncoding'
    _op.params['outputContentType'] = 'contentType'
    _op.params['outputHeader'] = 'responseHeader'
    _op.params['sslAcceptAllCertificates'] = ssl_accept_all_certificates
    if extra_header_attribute is not None:
        _op.params['extraHeaderAttribute'] = _op.attribute(stream, extra_header_attribute)
        _add_toolkit_dependency(stream.topology, '[3.0.0,4.0.0)') # extraHeaderAttribute parameter has been introduced in v3.0

    return _op.outputs[0]



class _HTTPRequest(streamsx.spl.op.Invoke):
    def __init__(self, stream, schema=None, accessTokenAttribute=None, authenticationFile=None, authenticationProperties=None, authenticationType=None, connectionTimeout=None, contentType=None, disableAutomaticRetries=None, disableContentCompression=None, disableRedirectHandling=None, errorDiagnostics=None, extraHeaderAttribute=None, extraHeaders=None, fixedContentType=None, fixedMethod=None, fixedUrl=None, method=None, outputBody=None, outputBodyRaw=None, outputCharSet=None, outputContentEncoding=None, outputContentType=None, outputDataLine=None, outputHeader=None, outputStatus=None, outputStatusCode=None, proxy=None, proxyPort=None, redirectStrategy=None, requestAttributes=None, requestAttributesAsUrlArguments=None, requestBodyAttribute=None, requestUrlArgumentsAttribute=None, sslAcceptAllCertificates=None, sslTrustStoreFile=None, sslTrustStorePassword=None, tokenTypeAttribute=None, url=None, userAgent=None, vmArg=None, name=None):
        topology = stream.topology
        kind="com.ibm.streamsx.inet.http::HTTPRequest"
        inputs=stream
        schemas=schema
        params = dict()
        if vmArg is not None:
            params['vmArg'] = vmArg
        if accessTokenAttribute is not None:
            params['accessTokenAttribute'] = accessTokenAttribute
        if authenticationFile is not None:
            params['authenticationFile'] = authenticationFile
        if authenticationProperties is not None:
            params['authenticationProperties'] = authenticationProperties
        if authenticationType is not None:
            params['authenticationType'] = authenticationType
        if connectionTimeout is not None:
            params['connectionTimeout'] = connectionTimeout
        if contentType is not None:
            params['contentType'] = contentType
        if disableAutomaticRetries is not None:
            params['disableAutomaticRetries'] = disableAutomaticRetries
        if disableContentCompression is not None:
            params['disableContentCompression'] = disableContentCompression
        if disableRedirectHandling is not None:
            params['disableRedirectHandling'] = disableRedirectHandling
        if errorDiagnostics is not None:
            params['errorDiagnostics'] = errorDiagnostics
        if extraHeaderAttribute is not None:
            params['extraHeaderAttribute'] = extraHeaderAttribute
        if extraHeaders is not None:
            params['extraHeaders'] = extraHeaders
        if fixedContentType is not None:
            params['fixedContentType'] = fixedContentType
        if fixedMethod is not None:
            params['fixedMethod'] = fixedMethod
        if fixedUrl is not None:
            params['fixedUrl'] = fixedUrl
        if method is not None:
            params['method'] = method
        if outputBody is not None:
            params['outputBody'] = outputBody
        if outputBodyRaw is not None:
            params['outputBodyRaw'] = outputBodyRaw
        if outputCharSet is not None:
            params['outputCharSet'] = outputCharSet
        if outputContentEncoding is not None:
            params['outputContentEncoding'] = outputContentEncoding
        if outputContentType is not None:
            params['outputContentType'] = outputContentType
        if outputDataLine is not None:
            params['outputDataLine'] = outputDataLine
        if outputHeader is not None:
            params['outputHeader'] = outputHeader
        if outputStatus is not None:
            params['outputStatus'] = outputStatus
        if outputStatusCode is not None:
            params['outputStatusCode'] = outputStatusCode
        if proxy is not None:
            params['proxy'] = proxy
        if proxyPort is not None:
            params['proxyPort'] = proxyPort
        if redirectStrategy is not None:
            params['redirectStrategy'] = redirectStrategy
        if requestAttributes is not None:
            params['requestAttributes'] = requestAttributes
        if requestAttributesAsUrlArguments is not None:
            params['requestAttributesAsUrlArguments'] = requestAttributesAsUrlArguments
        if requestBodyAttribute is not None:
            params['requestBodyAttribute'] = requestBodyAttribute
        if requestUrlArgumentsAttribute is not None:
            params['requestUrlArgumentsAttribute'] = requestUrlArgumentsAttribute
        if sslAcceptAllCertificates is not None:
            params['sslAcceptAllCertificates'] = sslAcceptAllCertificates
        if sslTrustStoreFile is not None:
            params['sslTrustStoreFile'] = sslTrustStoreFile
        if sslTrustStorePassword is not None:
            params['sslTrustStorePassword'] = sslTrustStorePassword
        if tokenTypeAttribute is not None:
            params['tokenTypeAttribute'] = tokenTypeAttribute
        if url is not None:
            params['url'] = url
        if userAgent is not None:
            params['userAgent'] = userAgent

        super(_HTTPRequest, self).__init__(topology,kind,inputs,schema,params,name)


