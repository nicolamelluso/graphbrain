package com.graphbrain.webapp

import com.graphbrain.hgdb.VertexStore
import com.graphbrain.hgdb.SimpleCaching


case class NodePage(nodeId: String) extends Page {
    val store = new VertexStore("gb") with SimpleCaching
    val gi = new GraphInterface(nodeId, store)
    val js = "var nodes = " + gi.nodesJSON + ";\n" +
        "var snodes = " + gi.snodesJSON + ";\n" +
        "var links = " + gi.linksJSON + ";\n" +
        "var error = '';\n"

	override def html = {

<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Graphbrain</title>
<link href="/css/main.css?040312" type="text/css" rel="Stylesheet" />
<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
<script src="/js/jquery-1.6.4.min.js" type="text/javascript" ></script>
<script src="/js/gb.js" type="text/javascript" ></script>
</head>

<body>
<div id="topDiv">
    <div id="logo">
        <a href="/"><img src="/images/GB_logo_M.png" alt="graphbrain"/></a>
    </div>
    <div id="inputArea">
        <form action="/search" method="post">
            <input type="text" name="input" id="inputField" size="50" />
            <input type="hidden" name="graph_id" value="{{ graph_id }}" />
            <input type="hidden" name="node_id" value="{{ node_id }}" />
            <button type="submit" id="inputFieldButton">Search</button>
        </form>
    </div>
    <div id="tip"></div>
</div>

<div id="nodesView">
    <div id="nodesDiv"></div>
</div>

<form action="/delink" method="post" id="delinkForm">
    <input type="hidden" name="link_orig" />
    <input type="hidden" name="link_targ" />
    <input type="hidden" name="link_type" />
</form>

<div class="overlay" id="overlay" style="display:none;"></div>
<div class="box" id="box">
    <a class="boxclose" id="boxclose"></a>
    <h1>Add Relationship</h1>
    <form action="/add" method="post" id="selbrainForm">
    <div class="dlabel">Origin:</div>
    <h2 id="dNode1"></h2>
    <input type="text" name="orig_text" id="dNode1In" size="40" />
    <div class="dlabel">Relationship:</div>
    <input type="text" name="rel" id="dRel" size="40" />
    <div class="dlabel">Target:</div>
    <h2 id="dNode2"></h2>
    <input type="text" name="targ_text" id="dNode2In" size="40" />
    <input type="hidden" name="orig_id" id="dNode1_id" />
    <input type="hidden" name="targ_id" id="dNode2_id" />
    <input type="hidden" name="graph_id" value="{{ graph_id }}" />
    <input type="hidden" name="node_id" value="{{ node_id }}" />
    <br />
    <input type="submit" value="Add" />
    </form>
</div>


<script language="javascript">

{scala.xml.Unparsed(js)}

</script>
</body>
</html>

  }
}